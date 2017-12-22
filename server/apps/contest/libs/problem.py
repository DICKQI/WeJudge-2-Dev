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
from .workers import contest_judge
from apps.problem.libs.problem import ProblemBodyController, ProblemBaseController
from apps.problem.libs.problem_manager import ProblemManagerController
from wejudge.judger.utils import get_java_class_name
from django.db import transaction

__author__ = 'lancelrq'


class ContestProblemController(ContestBaseController, ProblemBodyController):

    def __init__(self, request, response, cid):
        super(ContestProblemController, self).__init__(request, response, cid)

    # 读取题目信息
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    @ProblemBaseController.problem_privilege_validator(1)
    def get_problem_body(self):
        content = super(ContestProblemController, self).get_problem_body()
        return content

    # 提交代码
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status=0, errcode=5004)
    @ProblemBaseController.problem_privilege_validator(2)
    def submit_code(self):
        """
        提交代码
        :return:
        """
        contest = self.contest

        # 暂停评测提示
        if self.contest.pause or self.problem.pause_judge:
            raise WeJudgeError(2006)

        ptype = self.problem.problem_type

        parser = ParamsParser(self._request)
        lang = parser.get_int("lang", 1, method="POST")

        uid = parser.get_int("user_id", method="POST", require=True)
        if uid != self.session.account.id:
            raise WeJudgeError(8)

        if not system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(lang):
            raise WeJudgeError(2002)  # 不支持的评测语言

        if (self.contest_problem_item.lang != 0) and (lang & self.contest_problem_item.lang == 0):
            raise WeJudgeError(2002)

        if ptype == system.WEJUDGE_JUDGE_TYPE_FILL:
            handles = parser.get_str("handles", "", method="POST")
            handles = handles.split(",")
            code = {}
            code_len = 0
            for handle in handles:
                code[handle] = parser.get_str("code_%s" % handle, "", method="POST")
                code_len += len(code[handle])
            code_path = self._save_code_upload(lang, json.dumps(code))

        else:

            code = parser.get_str("code", "", method="POST")
            if len(code) < 20:
                raise WeJudgeError(2003)  # 提交代码至少要输入20个字符
            if lang == system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.JAVA:
                if not get_java_class_name(code):
                    raise WeJudgeError(2010)

            code_len = len(code)
            code_path = self._save_code_upload(lang, code)

        author = self.session.account
        try:
            with transaction.atomic():
                status = ContestModel.JudgeStatus()
                status.lang = lang
                status.author = author
                status.problem = self.problem
                status.virtual_problem = self.contest_problem_item
                status.code_len = code_len
                status.code_path = code_path
                status.save()
                # 加入到题目集合
                self.contest.judge_status.add(status)
        except:
            raise WeJudgeError(8)  # 事务异常

        # 题目访问统计(用户）
        apv = self.get_contest_solution()
        apv.judge_status.add(status)
        apv.submission = apv.judge_status.count()
        apv.save()
        # (题目)
        self.contest_problem_item.submission = contest.judge_status.filter(
            virtual_problem=self.contest_problem_item
        ).count()
        self.contest_problem_item.save()

        # 如果是自动或半自动模式
        if self.contest_problem_item.judger_mode in [0, 1]:
            # 发送评测信号
            contest_judge.delay(self.problem.id, status.id, contest.id)
        elif self.contest_problem_item.judger_mode == 2:
            status.flag = 20      # 等待人工评测
            status.save()

        return status.id

    # 获取当前题目的评测信息
    def _get_judge_config(self, problem):
        """
        获取当前题目的评测信息
        :return:
        """
        config_content = super(ContestProblemController, self)._get_judge_config(problem)

        if self.contest_problem_item is not None:
            config_content['lang'] = self.contest_problem_item.lang
        else:
            config_content['lang'] = self.problem.lang

        return config_content

    # 读取题目的评测历史
    @ContestBaseController.login_validator
    def get_judge_status(self):
        """
        读取题目的评测历史
        :return:
        """
        contest = self.contest
        problem = self.contest_problem_item
        user = self.session.account
        model_obj = contest.judge_status.filter(virtual_problem=problem, author=user).order_by("-id")

        return self._get_judge_status(model_obj)
