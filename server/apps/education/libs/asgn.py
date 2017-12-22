# -*- coding: utf-8 -*-
# coding:utf-8

import os
import json
import zipfile
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
from apps.education.libs import education
import apps.education.models as EducationModel
import apps.problem.models as ProblemModel
from .base import EducationBaseController
from .education import EducationController
from apps.problem.libs.base import ProblemBaseController
from django.http.response import HttpResponseNotFound

__author__ = 'lancelrq'


class EducationAsgnController(EducationBaseController, ProblemBaseController):

    def __init__(self, request, response, sid):
        super(EducationAsgnController, self).__init__(request, response, sid)

    # 获取作业的题目列表
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator(flag_enable=(0, 1))
    def get_asgn_problems(self):
        """
        获取作业的题目列表
        :return:
        """
        view_list = []

        user = self.session.account

        problems_list = self.asgn.problems.order_by('index')

        field_list = [
            "id", "entity", "entity__id", "entity__title", "entity__difficulty", "index", "accepted", "submission",
            "require", "score", "lang", "strict_mode", "max_score_for_wrong", "hidden_answer"
        ]
        if self.asgn.hide_problem_title:
            field_list.remove("entity__title")
        if user.role == 0:
            field_list.remove("entity__id")

        for problem in problems_list:
            pitem = problem.json(items=field_list)
            if user.role == 0:
                sol = EducationModel.Solution.objects.filter(asgn=self.asgn, author=user, problem=problem)
                if sol.exists():
                    sol = sol[0]
                    if sol.accepted > 0:
                        pitem["status"] = 2
                    else:
                        pitem["status"] = 1
                    pitem['status_count'] = "%s/%s" % (sol.accepted, sol.submission)
                    pitem['status_score'] = int((sol.score / 100.0) * problem.score)
                else:
                    pitem["status"] = 0
                    pitem['status_score'] = -1
                    pitem['status_count'] = ""
            view_list.append(pitem)

        return {
            "data": view_list
        }

    # 获取实验报告信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    def get_asgn_report_detail(self, rid=None):
        """
        获取实验报告信息
        :param rid: 非必须，获取指定detail
        :return:
        """

        report = self.get_asgn_report(rid)

        author = report.author

        v_soluctions = {}
        v_asgn_problems = []
        score_list = {}

        problems_list = self.asgn.problems.order_by('index')
        p_field_list = ["id", "entity",  "entity__title", "score", 'index']
        if self.asgn.hide_problem_title:
            p_field_list.remove("entity__title")

        for ap in problems_list:
            v_asgn_problems.append(ap.json(items=p_field_list))
            score_list[ap.id] = ap.score

        solutions = self.asgn.solution_set.filter(author=author)

        for sol in solutions:
            vdata = sol.json(items=[
                'first_visit_time', 'submission', 'accepted', 'penalty',
                'first_ac_time', 'best_memory', 'best_time', 'best_code_size'
            ], timestamp=True)
            pid = sol.problem.id
            vdata["finally_score"] = int(int(score_list.get(pid, 0)) * (sol.score / 100.0))
            v_soluctions[pid] = vdata

        return {
            "soluctions": v_soluctions,
            "problems": v_asgn_problems,
            "report": report.json(items=[
                "id", "judge_score", "finally_score", "ac_counter", "submission_counter",
                "solved_counter", "public_code","impression", "create_time", "modify_time",
                "teacher_check", "teacher_remark", "excellent", 'attachment'
            ]),
            "author": author.json(items=[
                "username", "realname"
            ])
        }

    # 保存当前学生的实验感想信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator(flag_enable=(0,))
    def save_asgn_report_impression(self):
        """
        保存当前学生的实验感想信息（注意，是当前，因为不可能给别人弄实验报告的别想了。）
        :return:
        """
        report = self.get_asgn_report()
        if report is None:
            raise WeJudgeError(3102)

        if report.teacher_check:
            raise WeJudgeError(3107)

        parser = ParamsParser(self._request)
        impression = parser.get_str("impression", require=True, method="POST", errcode=3104)

        report.impression = impression
        report.save()

    # 实验报告上传附件
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator(flag_enable=(0,))
    def upload_asgn_report_attchment(self):
        """
        实验报告上传附件
        :return:
        """
        report = self.get_asgn_report()
        if report is None:
            raise WeJudgeError(3102)
        if report.teacher_check:
            raise WeJudgeError(3107)

        parser = ParamsParser(self._request)
        # file = parser.get_file("uploadFile", require=True, max_size=233*1024*1024, type=[
        #     "image/pjpeg", "image/jpeg", "image/png", "image/x-png", "image/gif", "image/bmp",
        #     "application/msword", "application/vnd.ms-excel", "application/vnd.ms-powerpoint", "application/pdf",
        #     "application/x-gzip", "application/zip", "text/plain",
        #     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        #     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        #     "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        # ])
        file = parser.get_file("uploadFile", require=True, max_size=233 * 1024 * 1024)
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.EDUCATION_ASGN_ATTACHMENT, str(self.asgn.id))
        fname = "%s.attacment" % (str(report.id))
        destination = storage.open_file(fname, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        report.attachment = json.dumps({
            "filename": file.name,
            "source": fname
        })
        report.save()

    # 下载实验报告的附件
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    def download_asgn_report_attchment(self, rid):
        """
        下载实验报告的附件
        :return:
        """
        if rid == "0":
            report = self.get_asgn_report()
        else:
            report = self.get_asgn_report(rid)

        if report is None:
            raise WeJudgeError(3102)
        if rid is not None and self.session.account.role < 1 and report.author != self.session.account:
            raise WeJudgeError(3103)

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.EDUCATION_ASGN_ATTACHMENT, str(self.asgn.id))

        attachment = None
        try:
            if report.attachment is not None:
                attachment = json.loads(report.attachment)
        except:
            attachment = None

        if attachment is not None:
            fp = storage.open_file(attachment.get("source"), 'rb')

            def read_file(buf_size=8192):  # 大文件下载，设定缓存大小
                while True:  # 循环读取
                    c = fp.read(buf_size)
                    if c:
                        yield c
                    else:
                        break
                fp.close()

            response = HttpResponse(
                read_file(),
                content_type="application/octet-stream"
            )  # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
            response['Content-Length'] = os.path.getsize(storage.get_file_path(attachment.get("source")))
            response['Content-Disposition'] = "attachment; filename=%s" % attachment.get('filename')
            return response
        else:
            return HttpResponseNotFound()

    # 读取当前作业的所有评测历史
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    def get_judge_status(self):
        """
        读取当前作业的所有评测历史
        :return:
        """
        asgn = self.asgn
        model_obj = self._judge_status_filter(asgn.judge_status)

        return self._get_judge_status(model_obj)

    # 排行信息获取
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    def get_ranklist(self):
        """
        排行信息获取
        :return:
        """
        accounts_solutions = {}
        count = 1

        parser = ParamsParser(self._request)
        arrid = parser.get_int('arrangement_id', 0)
        students_filter_ids = None
        if arrid > 0:
            arr = EducationModel.Arrangement.objects.filter(id=arrid)
            if arr.exists():
                arr = arr[0]
                students_filter_ids = [stu.id for stu in arr.students.all()]

        # 对于这种可预知的大量查询，Django不会处理组合查询的，所以还是先查出来再走一次循环以节省与数据库交互的时间
        solutions = EducationModel.Solution.objects.filter(asgn=self.asgn)
        for sol in solutions:
            a = accounts_solutions.get(sol.author_id, {})
            a[sol.problem_id] = sol.json(items=[
                'accepted', 'submission', 'penalty', 'best_memory',
                'best_time', 'best_code_size', 'first_ac_time',
                'used_time', 'used_time_real'
            ])
            accounts_solutions[sol.author_id] = a

        account_view = []
        if students_filter_ids is not None:
            rank_model = EducationModel.AsgnReport.objects.filter(
                asgn=self.asgn, author__id__in=students_filter_ids
            ).order_by('-rank_solved', 'rank_timeused')
        else:
            rank_model = EducationModel.AsgnReport.objects.filter(
                asgn=self.asgn
            ).order_by('-rank_solved', 'rank_timeused')

        for _account in rank_model:
            account = _account.json(items=[
                'id', 'author', 'author__id', 'author__username', 'author__nickname',
                'author__realname', 'author__sex', 'rank_solved', 'rank_timeused'
            ])
            account['solutions'] = accounts_solutions.get(_account.author_id, {})
            account['rank'] = count
            count += 1
            account_view.append(account)

        return {
            "data": account_view,
            "problems": [x.json(items=[
                "id", "index"
            ]) for x in self.asgn.problems.order_by('index')],
        }

    # 获取滚榜数据
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    def get_rank_board_datas(self):
        """
        获取滚榜数据（比赛服阉割版）
        :return:
        """
        import time
        from django.utils.timezone import datetime
        asgn = self.asgn
        # 获取题目数据
        aproblem_list = asgn.problems.order_by("index")
        # 题目索引参照表
        apindex_list = {}
        for aproblem in aproblem_list:
            apindex_list[aproblem.entity.id] = aproblem.index
        parser = ParamsParser(self._request)

        # 获取最后一次刷新的时间
        last_time = parser.get_float('time', 0)
        try:
            last_time = datetime.fromtimestamp(last_time)
        except Exception as ex:
            last_time = 0

        user_list = {}

        if type(last_time) is datetime:
            # 设置了时间，就是弹时间线
            judge_status = asgn.judge_status.filter(create_time__gt=last_time).order_by("id")
        else:
            # 没有，就是弹初始化数据
            judge_status = asgn.judge_status.filter(create_time__lte=datetime.now())

        reports = EducationModel.AsgnReport.objects.filter(asgn=asgn)
        for report in reports:
            user_list[str(report.author.id)] = report.json(items=[
                'id', 'author', 'author__id', 'author__nickname', 'author__username',
                'author__realname', 'author__headimg', 'author__sex', 'start_time'
            ])

        judge_status_list = [{
            "id": status.id,
            "problem_id": status.problem_id,
            "user_id": status.author_id,
            "flag": status.flag,
            "timestamp": int(status.create_time.timestamp())
        } for status in judge_status]

        return {
            "problem_indexs": apindex_list,
            "problem_list": [aproblem.entity.id for aproblem in aproblem_list],
            "judge_status": judge_status_list,
            "user_list": user_list,
            "nowtime": time.time()
        }

    # 获取作业参考答案
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator(flag_enable=(0, 1))
    def get_answer(self):
        if self.session.account.role == 0 and self.asgn.public_answer_at is None:
            raise WeJudgeError(3106)

        from django.utils.timezone import now
        now_time = now()
        if self.session.account.role == 0 and now_time < self.asgn.public_answer_at:
            return {
                "status": "本次开放作业时间为: %s" % self.asgn.public_answer_at
            }
        else:
            return self._get_answer()


    # ====== Management ======

    # 保存题目的设置信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def save_asgn_problem_setting(self):
        """
        保存题目的设置信息
        :return:
        """
        parser = ParamsParser(self._request)
        lang_list = parser.get_list("lang", method="POST")
        score = parser.get_int("score", require=True, min=0, method="POST", errcode=3151)
        max_score_for_wrong = parser.get_int(
            "max_score_for_wrong", require=True, max=100, min=0, method="POST", errcode=3152
        )
        strict_mode = parser.get_boolean("strict_mode", False, method="POST")
        require = parser.get_boolean("require", True, method="POST")
        hidden_answer = parser.get_boolean("hidden_answer", False, method="POST")

        lang = 0
        for item in lang_list:
            if system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(item):
                lang = (lang | int(item))

        sc = 0
        for ap in self.asgn.problems.all():
            if ap.id != self.asgn_problem_item.id:
                sc += ap.score
        if (sc + score) > self.asgn.full_score:
            raise WeJudgeError(3150)

        self.asgn_problem_item.score = score
        self.asgn_problem_item.strict_mode = strict_mode
        self.asgn_problem_item.max_score_for_wrong = max_score_for_wrong
        self.asgn_problem_item.require = require
        self.asgn_problem_item.lang = lang
        self.asgn_problem_item.hidden_answer = hidden_answer
        self.asgn_problem_item.save()

        return True

    # 保存作业选题
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def save_problem_choosing(self):
        """
        保存作业选题
        :return:
        """
        parser = ParamsParser(self._request)
        problem_ids = parser.get_list("problem_ids", method="POST")
        result = {}

        for pid in problem_ids:
            problem = ProblemModel.Problem.objects.filter(id=pid)
            if not problem.exists():
                result[pid] = 1
                continue
            problem = problem[0]
            if self.asgn.problems.filter(entity=problem).exists():
                result[pid] = 2
                continue
            # 检查如果题目被移除，那把该题目的信息再刷关联回去
            old_choose = EducationModel.AsgnProblem.objects.filter(asgn=self.asgn, entity=problem)
            if old_choose.exists():
                old_choose = old_choose[0]
                self.asgn.problems.add(old_choose)
            else:
                # 新建AProblem信息
                ap = EducationModel.AsgnProblem()
                ap.entity = problem
                ap.asgn = self.asgn
                ap.index = self.asgn.problems.count() + 1
                ap.lang = self.asgn.lang
                ap.require = True
                ap.save()
                self.asgn.problems.add(ap)

            self.asgn.save()
            result[pid] = 3

        self._recalc_problems_index()
        return result

    # 获取作业的已选择题目
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def get_problems_choosed(self):
        """
        获取作业的已选择题目
        :return:
        """
        course = self.asgn.course
        problem_ids = []
        for asgn in course.asgn_set.all():
            for ap in asgn.problems.all():
                problem_ids.append(ap.entity_id)

        problem_ids = list(set(problem_ids))
        return problem_ids

    # 移除题目
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def remove_asgn_problem(self):
        self.asgn.problems.remove(self.asgn_problem_item)
        self._recalc_problems_index()
        return True

    # 获取作业设置信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(1)
    def get_asgn_settings(self):
        """
        获取作业设置信息
        :return:
        """
        asgn_info = self.asgn.json(items=[
            "title", "full_score", "lang", "description",
            "hide_problem_title", 'public_answer_at', 'hide_student_code'
        ])
        access_info = {x.arrangement.id: x.json(items=[
            "id", "start_time", "end_time", "enabled"
        ], timestamp=False) for x in self.asgn.access_control.all()}
        arrangements = self.asgn.course.arrangements.all()
        arrangements_list = []
        for arr in arrangements:
            d = arr.json(items=(
                "id", "name", "day_of_week", "start_week", "end_week",
                "odd_even", "start_section", "end_section", "start_time", "end_time"
            ))
            d['full_name'] = arr.toString()
            if d.get("id") in access_info.keys():
                d['access_info'] = access_info.get(d.get("id"))
            else:
                a = EducationModel.AsgnAccessControl()
                a.arrangement = arr
                a.enabled = False
                a.save()
                self.asgn.access_control.add(a)
                d['access_info'] = a.json(items=[
                    "id", "start_time", "end_time", "enabled"
                ], timestamp=False)
            arrangements_list.append(d)

        sections = {}
        try:
            import json
            sections = json.loads(self.school.sections)
            sections = sections.get('sections', {})
        except:
            pass

        return {
            "sections": sections,
            "asgn": asgn_info,
            "arrangements": arrangements_list
        }

    # 保存作业设置信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def save_asgn_setting(self):
        """
        保存作业设置信息
        :return:
        """
        parser = ParamsParser(self._request)
        lang_list = parser.get_list("lang", method="POST")
        title = parser.get_str("title", require=True, method="POST", errcode=3160)
        description = parser.get_str("description", default="", method="POST")
        full_score = parser.get_float("full_score", min=1.0, max=150.0, require=True, method="POST", errcode=3161)
        hide_problem_title = parser.get_boolean("hide_problem_title", False, method="POST")
        hide_student_code = parser.get_boolean("hide_student_code", False, method="POST")

        arrangement_ids = parser.get_list("arrangements", method="POST")

        lang = 0
        for item in lang_list:
            if system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(item):
                lang = (lang | int(item))

        self.asgn.title = title
        self.asgn.lang = lang
        self.asgn.description = description
        self.asgn.full_score = full_score
        self.asgn.hide_problem_title = hide_problem_title
        self.asgn.hide_student_code = hide_student_code

        access_controls = self.asgn.access_control.all()
        for ac in access_controls:
            if str(ac.id) not in arrangement_ids:
                ac.enabled = False
                ac.save()
            else:
                start_at = parser.get_datetime(
                    "start_time_%s" % str(ac.id), require=True, method="POST", errcode=3163
                )
                end_at = parser.get_datetime(
                    "end_time_%s" % str(ac.id), require=True, method="POST", errcode=3163
                )
                ac.enabled = True
                ac.start_time = start_at
                ac.end_time = end_at
                ac.save()

        last_time = access_controls[0].end_time
        for ac in access_controls:
            if ac.end_time is not None and last_time is not None:
                last_time = max(ac.end_time, last_time)
        self.asgn.public_answer_at = last_time
        self.asgn.save()

        return True

    # 重算作业的数据
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def refresh_asgn_datas(self):
        """
        重算作业的数据
        :return:
        """
        if self.asgn.archive_lock:
            raise WeJudgeError(3199)
        from .workers import refresh_asgn_datas
        refresh_asgn_datas.delay(self.asgn.id)

    # 重判题目
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def rejudge_problems(self):
        """
        重判题目
        :return:
        """

        from .workers import asgn_judge

        problem = self.asgn_problem_item
        status_list = self.asgn.judge_status.filter(virtual_problem=problem)
        for status in status_list:
            asgn_judge.delay(problem.entity.id, status.id, self.asgn.id, problem.strict_mode)

        return True

    # 获取实验报告列表
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(1)
    def get_reports_list(self):
        """
        获取实验报告列表
        :return:
        """
        reports = EducationModel.AsgnReport.objects.filter(asgn=self.asgn).order_by('teacher_check')
        return {
            "data": [report.json(items=[
                'id', 'author', 'author__id', 'author__realname', 'author__username', 'author__nickname',
                'judge_score', 'finally_score', 'ac_counter', 'submission_counter', 'solved_counter',
                'modify_time', 'teacher_check', 'excellent', 'public_code'
            ]) for report in reports]
        }

    # 保存作业的批改信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(1)
    def save_asgn_report_checkup(self, report_id):
        """
        保存作业的批改信息
        :return:
        """
        report = self.get_asgn_report(report_id)

        parser = ParamsParser(self._request)
        finally_score = parser.get_float(
            "finally_score", min=0, max=self.asgn.full_score, require=True, method="POST", errcode=3164
        )
        remark = parser.get_str("remark", "", method="POST")
        public_code = parser.get_boolean("public_code", False, method="POST")
        excellent = parser.get_boolean("excellent", False, method="POST")

        report.teacher_check = True
        report.finally_score = finally_score
        report.teacher_remark = remark
        report.public_code = public_code
        report.excellent = excellent
        report.save()

        return True

    # 批量保存作业的批改信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(1)
    def save_asgn_report_checkup_batch(self):
        """
        批量保存作业的批改信息
        :return:
        """

        parser = ParamsParser(self._request)
        report_ids = parser.get_list('report_ids', method='POST', require=True)
        use_judge_score = parser.get_boolean('use_judge_score', True, method='POST')
        if not use_judge_score:
            finally_score = parser.get_float(
                "finally_score", min=0, max=self.asgn.full_score, require=True, method="POST", errcode=3164
            )
        else:
            finally_score = 0

        remark = parser.get_str("remark", "", method="POST")

        for report_id in report_ids:
            report = self.get_asgn_report(report_id)
            report.teacher_check = True
            if use_judge_score:
                report.finally_score = report.judge_score
            else:
                report.finally_score = finally_score
            report.teacher_remark = remark
            report.save()

        return True

    # 获取调课记录信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(1)
    def get_visit_requirement(self):
        """
        获取实验报告列表
        :return:
        """
        visits = EducationModel.AsgnVisitRequirement.objects.filter(asgn=self.asgn)
        return {
            "data": [visit.json(items=[
                'id', 'author', 'author__id', 'author__realname', 'author__username', 'author__nickname',
                'arrangement', "arrangement__id", "arrangement__name", "arrangement__day_of_week",
                "arrangement__start_week", "arrangement__end_week", "arrangement__odd_even", "arrangement__end_time",
                "arrangement__start_section", "arrangement__end_section", "arrangement__start_time", 'create_time'
            ], timestamp=False) for visit in visits]
        }

    # 创建调课信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def add_visit_requirement(self):
        """
        创建调课信息
        :return:
        """
        parser = ParamsParser(self._request)
        user_id = parser.get_str("user_id", require=True, method="POST", errcode=3211)
        arrangement_id = parser.get_int("arrangement_id", require=True, method="POST", errcode=3165)

        account = EducationModel.EduAccount.objects.filter(school=self.school, username=user_id, role=0)
        if not account.exists():
            raise WeJudgeError(3005)
        account = account[0]

        arrangement = self.course.arrangements.filter(id=arrangement_id)
        if not arrangement.exists():
            raise WeJudgeError(3200)
        arrangement = arrangement[0]

        if EducationModel.AsgnVisitRequirement.objects.filter(asgn=self.asgn, author=account):
            raise WeJudgeError(3166)

        avr = EducationModel.AsgnVisitRequirement()
        avr.arrangement = arrangement
        avr.asgn = self.asgn
        avr.author = account
        avr.save()

    # 删除调课请求信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def delete_visit_requirement(self):
        """
        删除调课请求信息
        :return:
        """
        parser = ParamsParser(self._request)
        vrid = parser.get_int("id", require=True, method="POST")

        avr = EducationModel.AsgnVisitRequirement.objects.filter(asgn=self.asgn, id=vrid)
        if not avr.exists():
            raise WeJudgeError(3167)

        avr = avr[0]
        avr.delete()

    # 删除作业
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def delete_asgn(self):
        # 删除作业
        parser = ParamsParser(self._request)
        agree = parser.get_boolean("agree", False, method="POST")
        if not agree:
            raise WeJudgeError(7)
        course = self.asgn.course
        self.asgn.delete()

        return course.id

    # ====== Asgn Statistic ======

    # 获取统计用的原始数据
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def get_statistic_data(self):
        """
        获取统计用的原始数据
        :return:
        """
        # 作业数据
        asgn = self.asgn.json(items=[
            'title', 'create_time', 'full_score'
        ])
        asgn['problems'] = [ap.json(items=[
            'id', 'entity', 'entity__id', 'entity__title', 'index', 'accepted', 'submission', 'require',
            'lang', 'score', 'strict_mode', 'max_score_for_wrong'
        ])for ap in self.asgn.problems.all()]
        # 实验报告数据
        report_list = [report.json(items=[
            'author', 'author__id', 'author__username', 'author__nickname', 'author__realname',
            'judge_score', 'finally_score', 'ac_counter', 'submission_counter', 'solved_counter',
            'create_time', 'start_time', 'modify_time', 'teacher_check', 'excellent', 'rank_solved', 'rank_timeused'
        ], timestamp=True, timestamp_msec=True) for report in self.asgn.asgnreport_set.all()]
        # Solutions数据
        solution_list = [solution.json(items=[
            'author_id', 'problem_id', 'score', 'accepted', 'submission', 'penalty', 'best_memory', 'best_time',
            'best_code_size', 'create_time', 'first_ac_time', 'used_time', 'used_time_real'
        ], timestamp=True, timestamp_msec=True) for solution in self.asgn.solution_set.all()]
        # JudgeStatus数据
        judge_status_list = [js.json(items=[
            'problem_id', 'virtual_problem_id', 'author_id', 'flag', 'lang', 'create_time', 'exe_time',
            'exe_mem', 'code_len'
        ], timestamp=True, timestamp_msec=True) for js in self.asgn.judge_status.all()]
        return {
            "asgn": asgn,
            "reports": report_list,
            "solutions": solution_list,
            "judge_status": judge_status_list
        }

    #代码打包实现
    @EducationBaseController.login_validator
    @EducationBaseController.check_asgn_visit_validator()
    @EducationBaseController.check_user_privilege_validator(2)
    def asgn_zip_the_codes(self , asgn_id):
        """
        代码打包实现
        :param asgn_id: 
        :return: 
        """

        asgn = self.asgn
        parser = ParamsParser(self._request)
        encoding = parser.get_str('encoding', 'gbk', method='POST')
        separators = self._request.POST.get('separators' , '\\')
        if separators != '\\' and separators !='/':
            separators = '\\'

        filename = "%s.zip" % tools.uuid4()
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.EXPORT_TEMP_DIR , 'asgn_pack')
        zf = zipfile.ZipFile(storage.get_file_path(filename), "w", zipfile.zlib.DEFLATED)
        judge_status = asgn.judge_status.filter(flag=0)
        for status in judge_status:
            if not storage.exists(status.code_path):
                return
            upload_code = storage.get_file_path(status.code_path)
            stor_name = u"%s_%s%c%s_%s.%s" % (
                status.author.username, status.author.realname,
                separators, status.problem.id, status.id,
                system.WEJUDGE_CODE_FILE_EXTENSION.get(status.lang)
            )
            # if encoding == 'utf-8':
            zf.write(upload_code, stor_name)
            # else:
            #     zf.write(upload_code, stor_name.decode('utf-8').encode('gbk'))
        zf.close()

        fp = storage.open_file(filename , 'rb')

        def read_file(buf_size = 8192):
            while True:
                c = fp.read(buf_size)
                if c:
                    yield c
                else:
                    break
            fp.close()

        response = HttpResponse(
            read_file(),
            content_type = "application/octet-stream"
        )

        response['Content-Length'] = os.path.getsize(storage.get_file_path(filename))
        response['Content-Disposition'] = "attachment; filename = %s" % filename

        return response




    # ====== Provider =======

    # 读取或者创建作业报告(非VIEW)
    def get_asgn_report(self, report_id=None):
        """
        读取或者创建作业报告
        :param report_id: 如果为None则是自动处理学生的，否则视作教师访问
        :return:
        """
        asgn = self.asgn
        author = self.session.account

        if report_id is None:

            # 非学生不可生成实验报告
            if author.role >= 1:
                return None

            arp = EducationModel.AsgnReport.objects.filter(asgn=asgn, author=author)
            if not arp.exists():
                # 获取当前学生的排课情况
                flag, st, et = self._get_students_arrangment()
                if not flag:
                    raise WeJudgeError(3105)
                arp = EducationModel.AsgnReport()
                arp.author = author
                arp.asgn = asgn
                # 把排课时间写入到start_time字段，作为排行的计时器判定依据，不随排课改变
                arp.start_time = st
                arp.save()
            else:
                arp = arp[0]

            return arp

        else:

            arp = EducationModel.AsgnReport.objects.filter(id=report_id)
            if arp.exists():
                arp = arp[0]
                # 非己访问
                if author.role == 0 and arp.author != author:
                    raise WeJudgeError(3103)
                return arp
            else:
                raise WeJudgeError(3102)

    # 读取或创建当前用户的解决问题信息(非VIEW)
    def get_asgn_solution(self):
        """
        读取或创建当前用户的解决问题信息
        :return:
        """
        asgn = self.asgn
        author = self.session.account

        apv = EducationModel.Solution.objects.filter(asgn=asgn, author=author, problem=self.asgn_problem_item)
        if not apv.exists():
            apv = EducationModel.Solution()
            apv.problem = self.asgn_problem_item
            apv.author = author
            apv.asgn = asgn
            apv.save()
        else:
            apv = apv[0]

        return apv

    # 通过作业信息获取题目信息（或者根据题库信息）(非VIEW)
    def get_problem(self, pid):
        """
        获取problem信息
        :param pid:
        :return:
        """
        asgn = self.asgn
        if asgn is None:
            return
        problem_item = asgn.problems.filter(id=pid)
        if not problem_item.exists():
            raise WeJudgeError(3201)  # 找不到题目信息
        problem_item = problem_item[0]
        self.asgn_problem_item = problem_item
        self.problem = problem_item.entity

    # 获取作业的排课权限信息(非VIEW)
    def get_asgn_arrangements(self):
        access_control = self.asgn.access_control.all()
        return [{
                    "id": access.arrangement.id,
                    'name': access.arrangement.name,
                    'toString': access.arrangement.toString()
        } for access in access_control]

    # 获取作业参考答案 (主体实现)(非VIEW)
    def _get_answer(self):
        # 要输出的内容：每道题的不同语言的代码、优秀学生的代码（如果公开的话）
        problems_codes = []
        problems = self.asgn.problems.order_by('index')
        for problem in problems:
            if problem.hidden_answer:
                continue
            problem_entity = problem.entity
            judge_config = self._get_judge_config(problem_entity)
            problems_codes.append({
                "id": problem.id,
                "datas": {
                    "judge_type": judge_config.get('judge_type', {}),
                    "demo_cases": judge_config.get('demo_cases', {}),
                    "demo_answer_cases": judge_config.get('demo_answer_cases', {}),
                    "demo_code_cases": judge_config.get('demo_code_cases', {}),
                    "answer_cases": judge_config.get('answer_cases', {})
                }
            })
        reports_codes = []
        reports = EducationModel.AsgnReport.objects.filter(asgn=self.asgn, public_code=True)
        for report in reports:
            judge_status = self.asgn.judge_status.filter(author=report.author, flag=0)
            status_list = []
            for status in judge_status:
                try:
                    result_content = JudgeResult(status.result)
                except Exception as ex:
                    continue
                status_info = status.json(items=[
                    "id", "virtual_problem_id", "lang", "exe_time", "exe_mem", "code_len"
                ])
                status_info["finally_code"] = result_content.finally_code
                status_list.append(status_info)
            reports_codes.append({
                "author": report.author.json(items=['id', 'realname', 'username']),
                "judge_status": status_list
            })
        return {
            "status": "ok",
            "problems": {problem.id: problem.json(items=[
                "id", "index", "entity", "entity__id", "entity__title"
            ])for problem in problems},
            "problems_codes": problems_codes,
            "reports_codes": reports_codes
        }

    # 重计算题目的索引
    def _recalc_problems_index(self):
        """
        重计算题目的索引
        :return:
        """
        problems = self.asgn.problems.order_by('index')
        count = 1
        for problem in problems:
            problem.index = count
            problem.save()
            count += 1
        return True
