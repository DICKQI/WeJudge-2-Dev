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
from .workers import asgn_judge
from apps.problem.libs.problem import ProblemBodyController, ProblemBaseController
from django.db import transaction

__author__ = 'lancelrq'


class AsgnProblemController(EducationAsgnController, ProblemBodyController):

    def __init__(self, request, response, sid):
        super(AsgnProblemController, self).__init__(request, response, sid)

    # 读取题目信息
    @EducationAsgnController.login_validator
    @ProblemBaseController.problem_privilege_validator(1)
    @EducationAsgnController.check_asgn_visit_validator(flag_enable=(0, 1))
    def get_problem_body(self):
        return super(AsgnProblemController, self).get_problem_body()

    # 提交代码
    @EducationAsgnController.login_validator
    @ProblemBaseController.problem_privilege_validator(2)
    @EducationAsgnController.check_asgn_visit_validator(flag_enable=(0,))
    def submit_code(self):
        """
        提交代码
        :return:
        """
        asgn = self.asgn

        # 暂停评测提示
        if self.problem.pause_judge:
            raise WeJudgeError(2006)

        ptype = self.problem.problem_type

        parser = ParamsParser(self._request)
        lang = parser.get_int("lang", 1, method="POST")

        # uid = parser.get_int("user_id", method="POST", require=True)
        # if uid != self.session.author.id:
        #     raise WeJudgeError(8)

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
            code_len = len(code)
            code_path = self._save_code_upload(lang, code)

        if not system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(lang):
            raise WeJudgeError(2002)    # 不支持的评测语言

        if (self.asgn_problem_item.lang != 0) and (lang & self.asgn_problem_item.lang == 0):
            raise WeJudgeError(2002)

        author = self.session.account
        try:
            with transaction.atomic():
                status = EduModel.JudgeStatus()
                status.lang = lang
                status.author = author
                status.problem = self.problem
                status.virtual_problem = self.asgn_problem_item
                status.code_len = code_len
                status.code_path = code_path
                status.save(force_insert=True)
                # 加入到题目集合
                self.asgn.judge_status.add(status)
        except:
            raise WeJudgeError(8)       # 事务异常

        # 题目访问统计(用户）
        apv = self.get_asgn_solution()
        apv.judge_status.add(status)
        apv.submission = apv.judge_status.count()
        apv.save()
        # (题目)
        self.asgn_problem_item.submission = asgn.judge_status.filter(
            virtual_problem=self.asgn_problem_item).count()
        self.asgn_problem_item.save()

        # 发送评测信号
        asgn_judge.delay(self.problem.id, status.id, asgn.id, self.asgn_problem_item.strict_mode)
        return status.id

    # 读取题目的评测历史（当前作业内）
    @EducationAsgnController.login_validator
    @EducationAsgnController.check_asgn_visit_validator()
    def get_judge_status(self):
        """
        读取题目的评测历史（当前作业内）
        :return:
        """
        asgn = self.asgn
        problem = self.asgn_problem_item
        user = self.session.account
        model_obj = asgn.judge_status.filter(virtual_problem=problem, author=user).order_by("-id")

        return self._get_judge_status(model_obj)

    # 获取当前题目的评测信息
    def _get_judge_config(self, problem):
        """
        获取当前题目的评测信息
        :return:
        """
        config_content = super(AsgnProblemController, self)._get_judge_config(problem)

        if self.asgn_problem_item is not None:
            config_content['lang'] = self.asgn_problem_item.lang
            config_content['strict_mode'] = self.asgn_problem_item.strict_mode
        else:
            config_content['lang'] = self.problem.lang
            config_content['strict_mode'] = False

        return config_content
