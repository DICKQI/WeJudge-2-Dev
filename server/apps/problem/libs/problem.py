# -*- coding: utf-8 -*-
# coding:utf-8
import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.problem.models as ProblemModel
from .workers import judge
from .base import ProblemBaseController
from django.db import transaction

__author__ = 'lancelrq'


class ProblemBodyController(ProblemBaseController):

    def __init__(self, request, response):
        super(ProblemBodyController, self).__init__(request, response)

    # 代码格式化功能
    def code_indent(self):
        """
        代码格式化功能
        :return:
        """
        try:
            parser = ParamsParser(self._request)
            code = parser.get_str('code', require=True, method="POST")

            import subprocess

            ps = subprocess.Popen(
                "indent -bad -bap -bbb -bbo -nbc -bl -bli0 -bls -c33 -cd33 -ncdb -ncdw -nce "
                "-cli0 -cp33 -cs -d0 -nbfda -nfc1 -nfca -hnl -ip5 -l75 -lp -npcs -nprs -saf "
                "-sai -saw -nsc -nsob -nss -i4 -ts4 -ut -npsl",
                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
            )

            code = code.replace("\r\n", "\n").replace("\r", "\n")
            ps.stdin.write(code.encode("utf-8"))
            ps.stdin.flush()
            ps.stdin.close()
            output = ps.stdout.read()
            if len(output) == 0:
                raise WeJudgeError(1)

            return output.decode("utf-8")
        except:
            raise WeJudgeError(1)

    # 获取当前用户的草稿代码(内部检查登录)
    def get_code_drafts(self):
        """
        获取当前用户的草稿代码
        :return:
        """
        if not self.session.is_master_logined():
            raise WeJudgeError(2012)
        account = self.session.account
        code_drafts = ProblemModel.CodeDrafts.objects.filter(
            author=account, problem=self.problem
        ).order_by("-create_time")
        return [draft.json(items=[
            "id", "content", 'lang', 'create_time'
        ]) for draft in code_drafts]

    # 保存当前用户的草稿代码
    @ProblemBaseController.login_validator
    def save_code_draft(self):
        """
        保存当前用户的草稿代码
        :return:
        """
        if not self.session.is_master_logined():
            raise WeJudgeError(2012)

        parser = ParamsParser(self._request)
        lang = parser.get_int("lang", require=True, method="POST")

        ptype = self.problem.problem_type

        if ptype == system.WEJUDGE_JUDGE_TYPE_FILL:
            handles = parser.get_str("handles", "", method="POST")
            handles = handles.split(",")
            code = {}
            for handle in handles:
                code[handle] = parser.get_str("code_%s" % handle, "", method="POST")
            code = json.dumps(code)
        else:
            code = parser.get_str("code", require=True, method="POST", errcode=2011)

        account = self.session.account
        cds = ProblemModel.CodeDrafts.objects.filter(author=account, problem=self.problem).order_by("create_time")
        while cds.count() >= 3:
            # 如果有3条记录或者以上，则删除最旧的
            cds[0].delete()
            cds = ProblemModel.CodeDrafts.objects.filter(author=account, problem=self.problem).order_by("create_time")

        cd = ProblemModel.CodeDrafts()
        cd.author = account
        cd.problem = self.problem
        cd.content = code
        cd.lang = lang
        cd.save()

        return True

    # 获取题目信息
    @ProblemBaseController.problem_privilege_validator(1)
    def get_problem_body(self):
        """
        获取题目信息
        :return:
        """
        entity = self.problem
        view_body = entity.json([
            "title", "author", "author__id", "author__nickname", "author__sex",
            "difficulty", "create_time", "update_time", "description",
            "input", "output", "sample_input", "sample_output",
            "hint", "source", "problem_type", "lang",
            "pause_judge", "author__realname", "author__headimg",
        ])

        rules = []
        judge_config = JudgeConfig(entity.judge_config or "{}")
        time_limit = judge_config.time_limit
        mem_limit = judge_config.mem_limit

        if entity.lang > 0:
            language_allow = {x: True if (x & entity.lang) else False for x in [1, 2, 4, 8, 16]}
        else:
            language_allow = {1: True, 2: True, 4: True, 8: True, 16: True}

        for key in [1, 2, 4, 8, 16]:
            if language_allow.get(key, False):
                rules.append({
                    "lang": key,
                    "name": system.WEJUDGE_PROGRAM_LANGUAGE_CALLED.get(key),
                    "time_limit": time_limit.get(str(key)),
                    "mem_limit": mem_limit.get(str(key))
                })

        view_body['rules'] = rules

        view_config = self._get_judge_config(self.problem)

        return {
            "body": view_body,
            "judge_config":  view_config
        }

    # 提交代码
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(2)
    def submit_code(self):
        """
        提交代码
        :return:
        """

        if self.problem.pause_judge:
            raise WeJudgeError(2006)

        ptype = self.problem.problem_type

        parser = ParamsParser(self._request)
        lang = parser.get_int("lang", 1, method="POST")

        uid = parser.get_int("user_id", method="POST",require=True)
        if uid != self.session.account.id:
            raise WeJudgeError(8)

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

        if (self.problem.lang != 0) and (lang & self.problem.lang == 0):
            raise WeJudgeError(2002)

        author = self.session.account

        try:
            with transaction.atomic():
                status = ProblemModel.JudgeStatus()
                status.lang = lang
                status.author = author
                status.problem = self.problem
                status.virtual_problem = self.problem_set_item
                status.code_len = code_len
                status.code_path = code_path
                status.save(force_insert=True)
        except:
            raise WeJudgeError(8)       # 事务异常

        # 单题目访问统计(用户）
        apv = ProblemModel.AccountProblemVisited.objects.filter(author=author, problem=self.problem)
        if not apv.exists():
            apv = ProblemModel.AccountProblemVisited()
            apv.problem = self.problem
            apv.author = author
        else:
            apv = apv[0]
        apv.submission = ProblemModel.JudgeStatus.objects.filter(problem=self.problem, author=author).count()
        apv.save()

        if self.problem_set is not None and self.problem_set_item is not None:
            # 加入到题目集合
            self.problem_set.judge_status.add(status)
            # (题目)
            self.problem_set_item.submission = ProblemModel.JudgeStatus.objects.filter(
                virtual_problem=self.problem_set_item
            ).count()
            self.problem_set_item.save()

            # 题目访问统计(用户）
            sol = ProblemModel.ProblemSetSolution.objects.filter(author=author, virtual_problem=self.problem_set_item)
            if not sol.exists():
                sol = ProblemModel.ProblemSetSolution()
                sol.problem = self.problem
                sol.problemset = self.problem_set
                sol.virtual_problem = self.problem_set_item
                sol.author = author
            else:
                sol = sol[0]
            sol.submission = ProblemModel.JudgeStatus.objects.filter(
                virtual_problem=self.problem_set_item, author=author
            ).count()
            sol.save()

            # 发送评测信号
            judge.delay(self.problem.id, status.id, self.problem_set_item.id)
        else:
            # 发送评测信号
            judge.delay(self.problem.id, status.id)

        return status.id

    # 获取当前题目的评测信息
    def _get_judge_config(self, problem):
        """
        获取当前题目的评测信息
        :return:
        """
        config = self._load_judge_configuation(problem)
        config_content = config.dump()

        # 脱敏
        config_content['special_judger_program'] = ""
        config_content['library_cases'] = ""

        config_content['pause_judge'] = problem.pause_judge
        config_content['lang'] = problem.lang

        # 填空模式
        if problem.problem_type == system.WEJUDGE_JUDGE_TYPE_FILL:

            code_storage = self._get_problem_storage(problem, "code_cases")

            dc_list = config.dump_demo_cases()
            demo_code_list = {}

            for k, v in dc_list.items():
                # k 是编译语言的代码，通过此代码获取到该语言的.demo文件，以及.demo.answer文件
                # v 是表示测试用例的列表，是一个列表！（这里也不怎么需要这个参数，放着先）
                fn_demo = "%s.demo" % k

                if code_storage.exists(fn_demo):
                    fp = code_storage.open_file(fn_demo)
                    demo_code_list[k] = fp.read()
                    fp.close()

            # DemoCases的答案映射列表
            config_content["demo_code_cases"] = demo_code_list

        return config_content

    # 读取题目的评测历史
    @ProblemBaseController.login_validator
    def get_judge_status(self):
        """
        读取题目的评测历史（当前题目集内）
        :return:
        """
        pset = self.problem_set
        problem = self.problem
        user = self.session.account
        if pset is None:
            model_obj = ProblemModel.JudgeStatus.objects.filter(problem=problem, author=user).order_by("-id")
        else:
            model_obj = pset.judge_status.filter(problem=problem, author=user).order_by("-id")

        return self._get_judge_status(model_obj)

    # 获取题目分析统计信息
    def get_statistics(self):
        """
        获取题目分析统计信息
        :return:
        """

        import apps.education.models as EducationModel
        import apps.contest.models as ContestModel

        edu_status = EducationModel.JudgeStatus.objects.filter(problem=self.problem)
        contest_status = ContestModel.JudgeStatus.objects.filter(problem=self.problem)
        wejudge_status = ProblemModel.JudgeStatus.objects.filter(problem=self.problem)

        judge_counter = {
            "education": {},
            "contest": {},
            "wejudge": {},
            "total": {}
        }
        langs_counter = {
            "education": {},
            "contest": {},
            "wejudge": {},
            "total": {}
        }

        flags = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        langs = [1, 2, 4, 8, 16]

        for flag in flags:
            e = edu_status.filter(flag=flag).count()
            c = contest_status.filter(flag=flag).count()
            w = wejudge_status.filter(flag=flag).count()
            judge_counter['education'][flag] = e
            judge_counter['contest'][flag] = c
            judge_counter['wejudge'][flag] = w
            judge_counter['total'][flag] = e + c + w

        for lang in langs:
            e = edu_status.filter(lang=lang).count()
            c = contest_status.filter(lang=lang).count()
            w = wejudge_status.filter(lang=lang).count()
            langs_counter['education'][lang] = e
            langs_counter['contest'][lang] = c
            langs_counter['wejudge'][lang] = w
            langs_counter['total'][lang] = e + c + w

        return {
            "language": langs_counter,
            "judge": judge_counter
        }

