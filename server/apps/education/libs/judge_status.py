# -*- coding: utf-8 -*-
# coding:utf-8
import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.problem.models as ProblemModel
import apps.education.models as EduModel
from .asgn import EducationAsgnController
from apps.problem.libs.judge_status import JudgeStatusController

__author__ = 'lancelrq'


class AsgnJudgeStatusController(EducationAsgnController, JudgeStatusController):

    def __init__(self, request, response, sid):
        super(AsgnJudgeStatusController, self).__init__(request, response, sid)
        self.prefix = 'education'

    def testcase_high_privilege(self):
        """
        测试数据高级权限检查器（可重写）

        通过这个检查器，则可以查看测试数据
        如果不能通过这个检查器，则看测试数据是否隐藏，如果隐藏，则不能查看测试数据，否则可以。
        :return:
        """
        user = self.session.account             # Edu Account
        master = user.master                    # Master Account
        problem = self.status.problem           # Problem Entity

        if problem.author == master:
            return True
        else:
            if user.role >= 1:             # 对于当前作业，只要是助教以上用户就可以看
                return True

        return False

    # 获取评测状态信息（用于管理）
    @EducationAsgnController.login_validator
    @EducationAsgnController.check_user_privilege_validator(1)
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

    # 编辑评测状态
    @EducationAsgnController.login_validator
    @EducationAsgnController.check_user_privilege_validator(1)
    def edit(self):
        """
        编辑评测状态
        :return:
        """
        problem = self.status.virtual_problem

        parser = ParamsParser(self._request)
        flag = parser.get_int("flag",  require=True, min=-2, method="POST")
        if flag not in system.WEJUDGE_JUDGE_STATUS_DESC.keys():
            raise WeJudgeError(3111)
        self.status.flag = flag
        self.status.save(force_update=True)

        # 刷新
        from .judge import AsgnJudgeProcesser

        # 获取实验报告
        report = EduModel.AsgnReport.objects.filter(asgn=self.asgn, author=self.status.author)
        if report.exists():
            report = report[0]
        else:
            report = None

        processer = AsgnJudgeProcesser(self.asgn, problem)
        processer.proc_problem()
        if report is not None:
            processer.proc_solution(report)
            processer.proc_report(report)

    # 删除评测状态
    @EducationAsgnController.login_validator
    @EducationAsgnController.check_user_privilege_validator(1)
    def delete(self):
        """
        删除评测状态
        :return:
        """
        self.status.delete()

    @EducationAsgnController.login_validator
    def get_judge_detail(self):
        """
        获取评测详情（覆写）
        :return:
        """
        detail = super(AsgnJudgeStatusController, self).get_judge_detail()
        if self.asgn.hide_student_code and self.session.account.role == 0:
            detail['result']['finally_code'] = "根据相关法律法规和政策，老师没有开放学生查看代码的权限 _(:зゝ∠)_"
        return detail

    # 重判单个评测记录
    @EducationAsgnController.login_validator
    @EducationAsgnController.check_user_privilege_validator(1)
    def rejudge(self):
        """
        重判单个评测记录
        :return:
        """
        from .workers import asgn_judge

        problem = self.status.virtual_problem
        asgn_judge.delay(problem.entity.id, self.status.id, self.asgn.id, problem.strict_mode)
