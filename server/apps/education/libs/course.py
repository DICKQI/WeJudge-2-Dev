# -*- coding: utf-8 -*-
# coding:utf-8

import time
import xlrd
import xlwt
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.education.models as EducationModel
from .base import EducationBaseController

__author__ = 'lancelrq'


class EducationCourseController(EducationBaseController):

    def __init__(self, request, response, sid):
        super(EducationCourseController, self).__init__(request, response, sid)

    # 获取课程的作业信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_visit_validator
    def get_asgn_list(self, course=None):
        """
        获取课程的作业信息
        :param course:  如果不设置，默认用self.course
        :return:
        """

        course = course if course is not None else self.course
        user = self.session.account

        data = course.asgn_set.all()

        view_list = []

        for item in data:

            asgn = item.json(items=[
                "id", "title", "teacher", "teacher__id", "teacher__realname",
                "create_time", "full_score", "description"
            ])
            asgn["problems_count"] = item.problems.count()
            # -2：无权限； -1：未访问；0: 未完成； 1：已提交；2：已批改；3：教师模式，批改
            if user.role == 0:
                asgn["status"] = -1

                vreq = EducationModel.AsgnVisitRequirement.objects.filter(author=user, asgn=item)
                if vreq.exists():
                    vreq = vreq[0]
                    varg = EducationModel.AsgnAccessControl.objects.filter(
                        asgn=self.asgn, enabled=True, arrangement=vreq.arrangement
                    )
                    if varg.exists():
                        varg = varg[0]
                        asgn['deadline'] = varg.end_time

                if asgn.get('deadline', None) is None:
                    aacs = item.access_control.filter(arrangement__students__id__contains=user.id, enabled=True)
                    if not aacs.exists():
                        # 无权限
                        asgn["status"] = -2
                        continue
                    else:
                        asgn['deadline'] = aacs[0].end_time
                        for aac in aacs:
                            asgn['deadline'] = max(asgn['deadline'], aac.end_time)

                asgn['deadline'] = int(time.mktime(asgn['deadline'].timetuple()))
                asgn['nowtime'] = int(time.time())

                report = EducationModel.AsgnReport.objects.filter(asgn_id=item.id, author=user)
                if report.exists():
                    report = report[0]
                    asgn["status"] = 0
                    if report.impression is not None and report.impression.strip() != "":
                        asgn["status"] = 1
                    if report.teacher_check:
                        asgn["status"] = 2

            else:
                check_count = EducationModel.AsgnReport.objects.filter(asgn__id=asgn.get('id', 0), teacher_check=False).count()
                asgn["status"] = 3
                asgn["pending_check_count"] = check_count

            view_list.append(asgn)
        
        return {
            "data": view_list
        }

    # 创建作业
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def create_asgn(self):
        """
        创建作业
        :return:
        """
        parser = ParamsParser(self._request)
        title = parser.get_str("title", require=True, method="POST", errcode=3160)
        description = parser.get_str("description", default="", method="POST")
        full_score = parser.get_float("full_score", min=1.0, max=150.0, require=True, method="POST", errcode=3161)

        asgn = EducationModel.Asgn()

        asgn.course = self.course
        asgn.teacher = self.session.account
        asgn.title = title
        asgn.description = description
        asgn.full_score = full_score
        asgn.save()

        return asgn.id

    # 获取课程设置信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_visit_validator
    def get_course_settings_info(self):
        course = self.course.json(items=[
            'name', 'description', 'term', 'term__id', 'term__year', 'term__term',
            'academy', 'academy__id', 'academy__name', 'author', 'author__id', 'author__realname', 'author__username'
        ])
        teachers = [teacher.json(items=[
            'id', 'realname', 'nickname', 'username'
        ]) for teacher in self.course.teacher.all()]
        assistants = [assistant.json(items=[
            'id', 'realname', 'nickname', 'username'
        ]) for assistant in self.course.assistants.all()]

        return {
            "course": course,
            "teachers": teachers,
            "assistants": assistants,
            "education": {
                "academies": [academy.json(items=['id', 'name']) for academy in self.get_school_academies()],
                "yearterms": [term.json(items=['id', 'year', 'term']) for term in self.get_school_terms()]
            }
        }

    # 读取当前课程的排课信息列表
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_visit_validator
    def get_arrangements_list(self):
        """
        读取当前课程的排课信息列表
        :return:
        """
        arrangements = self.course.arrangements.all()
        view = []
        for arrangement in arrangements:
            ar = arrangement.json(items=[
                'id', 'name', 'day_of_week', 'start_week', 'end_week', 'odd_even', 'start_section',
                'end_section', 'start_time', 'end_time'
            ])
            ar['students_count'] = arrangement.students.count()
            view.append(ar)
        return view

    # 读取当前课程排课的选课情况
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_visit_validator
    def get_students_by_arrangements(self, arr_id):
        """
        读取当前课程排课的选课情况
        :param arr_id:
        :return:
        """
        arrangement = EducationModel.Arrangement.objects.filter(id=arr_id)
        if not arrangement.exists():
            raise WeJudgeError(3200)
        arrangement = arrangement[0]
        return [student.json(items=[
            'id', 'username', 'nickname', 'realname'
        ]) for student in arrangement.students.all()]

    # 增删改排课信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def change_arrangements(self):
        """
        增删改排课信息
        :return:
        """
        parser = ParamsParser(self._request)
        delete = parser.get_boolean("delete", False, method="POST")
        arr_id = parser.get_int("id", min=0, require=True, method="POST")

        if int(arr_id) > 0:
            arrangement = EducationModel.Arrangement.objects.filter(id=arr_id)
            if not arrangement.exists():
                raise WeJudgeError(3200)
            arrangement = arrangement[0]
        else:
            arrangement = None

        if delete and arrangement is not None:
            arrangement.delete()
            return True

        name = parser.get_str("name", "", method="POST")
        odd_even = parser.get_int("odd_even", 0, method="POST")
        start_week = parser.get_int("start_week", 1, min=1, max=52, method="POST")
        end_week = parser.get_int("end_week", 17, min=1, max=52, method="POST")
        day_of_week = parser.get_int("day_of_week", 0, min=0, max=7, method="POST")
        start_section = parser.get_int("start_section", 1, min=1, max=20, method="POST")
        end_section = parser.get_int("end_section", 2, min=1, max=20, method="POST")

        if arrangement is None:
            arrangement = EducationModel.Arrangement()

        arrangement.name = name
        arrangement.odd_even = odd_even
        arrangement.start_week = start_week
        arrangement.end_week = end_week
        arrangement.day_of_week = day_of_week
        arrangement.start_section = start_section
        arrangement.end_section = end_section
        arrangement.save()

        if int(arr_id) == 0:
            self.course.arrangements.add(arrangement)
            self.course.save()

        return True

    # 向排课添加/删除学生
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def toggle_student_to_arrangements(self):

        parser = ParamsParser(self._request)
        user_id = parser.get_str("user_id", require=True, method="POST", errcode=3211)
        remove = parser.get_boolean("remove", False, method="POST")
        arr_id = parser.get_int("id", min=0, require=True, method="POST")

        arrangement = EducationModel.Arrangement.objects.filter(id=arr_id)
        if not arrangement.exists():
            raise WeJudgeError(3200)
        arrangement = arrangement[0]

        account = EducationModel.EduAccount.objects.filter(school=self.school, username=user_id, role=0)
        if not account.exists():
            raise WeJudgeError(3005)
        account = account[0]

        if remove:
            if not arrangement.students.filter(id=account.id).exists():
                raise WeJudgeError(3202)
            arrangement.students.remove(account)
        else:
            if arrangement.students.filter(id=account.id).exists():
                raise WeJudgeError(3201)
            arrangement.students.add(account)

        arrangement.save(force_update=True)

        return True

    # 从XLS导入账户信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def xls_student_to_arrangements(self, arr_id):
        """
        从xls导入账户信息
        :return:
        """

        parser = ParamsParser(self._request)

        arrangement = EducationModel.Arrangement.objects.filter(id=arr_id)
        if not arrangement.exists():
            raise WeJudgeError(3200)
        arrangement = arrangement[0]

        file = parser.get_file("uploadFile", require=True)
        filename = "%s.xls" % tools.uuid4()
        # 写入上传的文件：
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.IMPORT_TEMP_DIR, 'education')
        fp = storage.open_file(filename, "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        msg = []
        try:
            import xlrd
            xls_sheet = xlrd.open_workbook(storage.get_file_path(filename))
            xls_table = xls_sheet.sheet_by_index(0)
            for i in range(2, xls_table.nrows):
                user_row = xls_table.row_values(i)
                user_id = user_row[0]
                if type(user_id) == float or type(user_id) == int:
                    user_id = str(int(user_id))
                if user_id.strip() == '':
                    continue
                user = EducationModel.EduAccount.objects.filter(school=self.school, username=user_id)
                if user.exists():
                    arrangement.students.add(user[0])
                else:
                    msg.append("用户不存在：%s" % user_id)
        except Exception as ex:
            msg.append("处理XLS失败 [%s] " % ex)

        return "<br />".join(msg)

    # 保存/新建课程设置信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def save_course_info(self):
        """
        保存/新建课程设置信息
        :return:
        """
        parser = ParamsParser(self._request)
        name = parser.get_str("name", require=True, method="POST", errcode=3160)
        description = parser.get_str("description", default="", method="POST")
        term = parser.get_int("term", 0, method="POST")
        academy = parser.get_int("academy", 0, method="POST")

        term = self.get_term(term)
        if term is None:
            raise WeJudgeError(3003)
        academy = self.get_academy(academy)
        if academy is None:
            raise WeJudgeError(3006)

        if self.course is None:
            user = self.session.account
            self.course = EducationModel.Course()
            self.course.school = self.school
            self.course.teacher.add(user)
            self.course.author = user
            self.course.save()

        self.course.name = name
        self.course.description = description
        self.course.term = term
        self.course.academy = academy
        self.course.save()

        return True

    # 向课程添加/删除学生助教
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def toggle_assistant_to_course(self):
        """
        向课程添加/删除学生助教
        :return:
        """
        parser = ParamsParser(self._request)
        user_id = parser.get_str("user_id", require=True, method="POST", errcode=3211)
        remove = parser.get_boolean("remove", False, method="POST")

        account = EducationModel.EduAccount.objects.filter(school=self.school, username=user_id, role=0)
        if not account.exists():
            raise WeJudgeError(3005)
        account = account[0]

        if remove:
            if not self.course.assistants.filter(id=account.id).exists():
                raise WeJudgeError(3204)
            self.course.assistants.remove(account)
        else:
            if self.course.assistants.filter(id=account.id).exists():
                raise WeJudgeError(3203)
            self.course.assistants.add(account)

        self.course.save(force_update=True)

        return True

    # 向课程添加/删除老师
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator(the_creater=True)
    def toggle_teacher_to_course(self):

        parser = ParamsParser(self._request)
        user_id = parser.get_str("user_id", require=True, method="POST", errcode=3211)
        remove = parser.get_boolean("remove", False, method="POST")

        account = EducationModel.EduAccount.objects.filter(school=self.school, username=user_id, role__gte=2)
        if not account.exists():
            raise WeJudgeError(3005)
        account = account[0]

        if account.id == self.course.author.id:
            raise WeJudgeError(3209)

        if remove:
            if not self.course.teacher.filter(id=account.id).exists():
                raise WeJudgeError(3208)
            self.course.teacher.remove(account)
        else:
            if self.course.teacher.filter(id=account.id).exists():
                raise WeJudgeError(3207)
            self.course.teacher.add(account)

        self.course.save(force_update=True)

        return True

    # 向课程添加/删除教学资源库关联
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def toggle_repository_to_course(self):

        parser = ParamsParser(self._request)
        repo_id = parser.get_int("repo_id", require=True, method="POST")

        repo = EducationModel.Repository.objects.filter(school=self.school, id=repo_id)
        if not repo.exists():
            raise WeJudgeError(3400)
        repo = repo[0]

        rpc = self.course.repositories.filter(id=repo_id)
        if rpc.exists():
            self.course.repositories.remove(repo)
        else:
            self.course.repositories.add(repo)

        self.course.save()

        return True

    # 删除作业
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator(the_creater=True)
    def delete_course(self):
        # 删除作业
        parser = ParamsParser(self._request)
        agree = parser.get_boolean("agree", False, method="POST")
        if not agree:
            raise WeJudgeError(7)
        self.course.delete()

        return self.school.id

    # 作业成绩统计
    @EducationBaseController.login_validator
    @EducationBaseController.check_course_manager_validator()
    def asgn_score_counter(self):

        parser = ParamsParser(self._request)
        export_type = parser.get_str("type", 'all', method="POST")
        asgn_ids = parser.get_list('asgn_ids', method="POST")
        try:
            asgn_ids = [int(aid) for aid in asgn_ids]
        except:
            raise WeJudgeError(1)

        student_ids_include = []

        if export_type == "student_codes":
            # TODO
            student_ids_include = []
            xls_file = parser.get_file('fileupload')
            pass

        else:
            student_ids_include = None

        result = self._asgn_score_count(asgn_ids, student_ids_include)
        xls_result = self._export_score_to_xls(asgn_ids, **result)

        return xls_result


    #作业成绩统计提供
    def _asgn_score_count(self, asgn_ids, student_ids_include):
        asgn_ratios = {}
        asgn_total_ratio = 100
        asgn_total_cnt = len(asgn_ids)
        parser = ParamsParser(self._request)
        # 获取每个作业对应的占分比例
        for aid in asgn_ids:
            ratio = parser.get_float('ratio_%s' % aid ,0, method="POST", errcode=1)
            if ratio < 0 or ratio > 100:
                ratio = 0
            if ratio != 0:
                asgn_total_ratio -= ratio
                asgn_total_cnt -= 1
                asgn_ratios[aid] = ratio


        # 处理剩余未分配百分比的值
        if asgn_total_cnt > 0:
            t_avg  = asgn_total_ratio / asgn_total_cnt
            for aid in asgn_ids:
                if aid not in asgn_ratios.keys():
                    asgn_ratios[aid] = t_avg

        students_ids = []
        students_scores = {}


        asgn_set = {asgn.id: asgn for asgn in self.course.asgn_set.filter(id__in=asgn_ids)}
        asgn_names = {key:val.title for key, val in asgn_set.items()}
        for aid in asgn_ids:
            asgn  = asgn_set.get(aid,None)
            ratio = asgn_ratios.get(aid, 0)
            if asgn is None:
                continue

            reports = asgn.asgnreport_set.all()
            for report in reports:
                if student_ids_include is not None and report.author_id not in student_ids_include:
                    continue

                author_id = report.author_id
                if author_id not in students_ids:
                    students_ids.append(author_id)
                    sc = students_scores.get(author_id, {})
                    avg = sc.get('avg' , 0)
                    avg += report.finally_score * (ratio / 100.0)
                    t_asgn = sc.get('asgn',{})
                    t_asgn[aid] = report.finally_score
                    sc['asgn'] = t_asgn
                    sc['avg'] = avg
                    students_scores[report.author_id] = sc


        student_infos = {
            student.id:student.json(items=['username', 'realname'])
            for student in EducationModel.EduAccount.objects.filter(id__in=students_ids)
        }

        return {
            "students_scores": students_scores,
            "students_ids": students_ids,
            "student_infos": student_infos,
            "asgn_names": asgn_names
        }


    def _export_score_to_xls(self, asgn_ids, students_scores, students_ids, student_infos, asgn_names):
        """
        导出成绩到xls
        :param asgn_ids: 
        :param students_scores: 
        :param students_ids: 
        :param student_infos: 
        :param asgn_names: 
        :return: 
        """


        filename = "%s.xls" % tools.uuid4()
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.EXPORT_TEMP_DIR , 'course_score_count')
        filepath = storage.get_file_path(filename)

        xlsfile = xlwt.Workbook()
        table = xlsfile.add_sheet(u'成绩统计')
        i = 1
        j = 2
        table.write(0,0,u"学号")
        table.write(0,1,u"姓名")
        for aid in asgn_ids:
            table.write(0 , j , asgn_names[aid])
            j += 1
        table.write(0,j,u"加权平均分")

        if students_ids is None:
            for key , score in students_scores.itemns():
                table.write(i , 0 , key)
                table.write(i , 1 , student_infos.get(key, {}).get('realname',''))
                j = 2
                for asgn_id in asgn_ids:
                    table.write(i , j , score.get(asgn_id , 0))
                    j += 1
                table.write(i , j , score.get('avg' , 0))
                i += 1
        else:
            for sid in students_ids:
                score = students_scores.get(sid , 0)
                table.write(i , 0 , sid)
                table.write(i , 1 , student_infos.get(sid, {}).get('realname',''))
                j = 2
                for asgn_id in asgn_ids:
                    table.write(i , j , score.get(asgn_id , 0))
                    j += 1
                table.write(i , j , score.get('avg' , 0))
                i += 1

        xlsfile.save(filepath)
        return filepath.replace("/data", "")



        # return storage.get_file_path(filename).replace("/data/resource/", "/resource")