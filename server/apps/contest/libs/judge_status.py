# -*- coding: utf-8 -*-
# coding:utf-8
import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.problem.models as ProblemModel
import apps.contest.models as ContestModel
from .base import ContestBaseController
from apps.problem.libs.judge_status import JudgeStatusController

__author__ = 'lancelrq'


class ContentJudgeStatusController(ContestBaseController, JudgeStatusController):

    def __init__(self, request, response, cid):
        super(ContentJudgeStatusController, self).__init__(request, response, cid)
        self.prefix = 'contest'

    def testcase_high_privilege(self):
        """
        测试数据高级权限检查器（可重写）

        通过这个检查器，则可以查看测试数据
        如果不能通过这个检查器，则看测试数据是否隐藏，如果隐藏，则不能查看测试数据，否则可以。
        :return:
        """
        user = self.session.account             # Contest Account
        master = user.master                    # Master Account
        problem = self.status.problem           # Problem Entity

        if problem.author == master:
            return True
        else:
            if user.role in [1, 2]:         # 对于当前比赛，只要是裁判就可以查看
                return True

        return False

    # 获取评测状态信息
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=1)
    def get_status_body(self):
        """
        获取评测状态信息
        :return:
        """
        status_view = self.status.json(items=[
            'id', 'problem_id', 'virtual_problem_id', 'flag', 'lang',
            'create_time', 'exe_time', 'exe_mem', 'code_len'
        ])
        return {
            "status": status_view,
            "description": system.WEJUDGE_JUDGE_STATUS_DESC
        }

    # 删除评测状态
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=1)
    def delete(self):
        """
        删除评测状态
        :return:
        """
        self.status.delete()

    # 编辑评测状态
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=1)
    def edit(self):
        """
        编辑评测状态
        :return:
        """
        problem = self.status.virtual_problem
        # 全自动模式不支持修改评测结果！
        if problem.judger_mode == 0:
            raise WeJudgeError(5264)

        parser = ParamsParser(self._request)
        flag = parser.get_int("flag",  require=True, min=-2, method="POST")
        if flag not in system.WEJUDGE_JUDGE_STATUS_DESC.keys():
            raise WeJudgeError(5265)
        self.status.flag = flag
        self.status.save(force_update=True)

        # 刷新排行榜
        from .judge import ContestJudgeProcesser
        processer = ContestJudgeProcesser(self.contest, problem)
        processer.proc_problem()
        processer.proc_solution(self.status.author)
        processer.proc_rank(self.status.author)

    # 获取评测详情（覆写）
    @ContestBaseController.login_validator
    def get_judge_detail(self):
        """
        获取评测详情（覆写）
        :return:
        """
        detail = super(ContentJudgeStatusController, self).get_judge_detail()
        if self.session.account.role == 0:
            detail['result']['finally_code'] = "根据相关法律法规和政策，选手代码不能显示 _(:зゝ∠)_"
        return detail

    # 重判单个评测记录
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    def rejudge(self):
        """
        重判单个评测记录
        :return:
        """
        from .workers import contest_judge

        problem = self.status.virtual_problem
        contest_judge.delay(problem.entity.id, self.status.id, self.contest.id)