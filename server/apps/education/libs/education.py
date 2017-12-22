# -*- coding: utf-8 -*-
# coding:utf-8

from django.db.models import Q
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.education.models as EducationModel
import apps.account.models as AccountModel
from .base import EducationBaseController

__author__ = 'lancelrq'


class EducationController(EducationBaseController):

    def __init__(self, request, response, sid):
        super(EducationController, self).__init__(request, response, sid)

    # 获取学校列表
    @staticmethod
    def get_schools_list():
        """
        获取学校列表
        :return:
        """
        return EducationModel.EduSchool.objects.all()

    # 通过学校简称获取学校信息
    @staticmethod
    def get_school_by_short_name(sn, throw=True):
        school = EducationModel.EduSchool.objects.filter(short_name=sn)
        if school.exists():
            return school[0]
        else:
            if throw:
                raise WeJudgeError(3000)
            else:
                return False

    # 教学系统首页接口组
    @EducationBaseController.login_validator
    def get_education_course_asgn_datas(self):
        """
        教学系统首页接口组
        :return:
        """
        id_list = []
        course_list = []
        course_finally_list = []
        asgn_finally_list = []

        # 获取课程列表
        def get_course_list(model):
            for course in model.filter(school=self.school, term=self.term):
                if course.id in id_list:
                    continue
                else:
                    id_list.append(course.id)

                course_list.append(course)
                c = course.json(items=[
                    "id", "name", "term__str", "academy", "academy__name",
                    "description", 'author', 'author__id', 'author__realname'
                ])
                c['student_count'] = course.students.count()
                course_finally_list.append(c)

        # 获取作业列表
        def get_asgn_list(user):
            for course in course_list:
                asgn_set = course.asgn_set.all()
                for item in asgn_set:

                    asgn = item.json(items=[
                        "id", "title", "teacher", "teacher__id", "teacher__realname",
                        "create_time", "full_score", "description"
                    ])
                    asgn["problems_count"] = item.problems.count()

                    # -1：未访问；0: 未完成； 1：已提交； 2：已批改；3：待批改;
                    if user.role == 0:
                        asgn["status"] = -1
                        if not item.access_control.filter(
                                arrangement__students__id__contains=user.id, enabled=True
                        ).exists():
                            asgn["status"] = -2
                        else:
                            report = EducationModel.AsgnReport.objects.filter(asgn__id=item.id, author=user)
                            if report.exists():
                                report = report[0]
                                asgn["status"] = 0
                                if report.impression is not None and report.impression.strip() != "":
                                    asgn["status"] = 1
                                if report.teacher_check:
                                    asgn["status"] = 2
                        if asgn['status'] in [0, -1]:
                            asgn_finally_list.append(asgn)

                    else:
                        check_count = EducationModel.AsgnReport.objects.filter(asgn__id=asgn.get('id', 0),
                                                                               teacher_check=False).count()
                        if check_count > 0:
                            asgn["status"] = 3
                            asgn["pending_check_count"] = check_count
                            asgn_finally_list.append(asgn)

        views = {}

        if self.term is not None:

            if self.session.account.role == 0:
                # 学生
                for arr in self.session.account.arrangement_set.all():
                    get_course_list(arr.course_set)
                get_course_list(self.session.account.course_assistants)
                get_asgn_list(self.session.account)

            elif self.session.account.role == 2:
                # 老师
                get_course_list(self.session.account.course_teacher)
                get_asgn_list(self.session.account)

            elif self.session.account.role == 3:
                get_course_list(EducationModel.Course.objects.filter(school=self.school))

            views["courses_list"] = course_finally_list
            views["asgns_list"] = asgn_finally_list
        else:
            views["courses_list"] = []
            views["asgns_list"] = []

        return views

    # 获取当前学校的所有课程信息
    def get_courses_list(self):
        """
        获取当前学校的所有课程信息
        :return:
        """
        course_list = []
        for course in EducationModel.Course.objects.filter(school=self.school, term=self.term):
            c = course.json(items=[
                "id", "name", "term__str", "academy", "academy__name",
                "description", 'author', 'author__id', 'author__realname'
            ])
            c['student_count'] = course.students.count()
            course_list.append(c)

        return {
            "courses_list": course_list
        }

    # 通过学校ID获取学校信息
    @staticmethod
    def get_school_by_school_id(sid, throw=True):
        school = EducationModel.EduSchool.objects.filter(id=sid)
        if school.exists():
            return school[0]
        else:
            if throw:
                raise WeJudgeError(3000)
            else:
                return False

    # 获取当前学校的学年学期列表
    def get_terms_list(self):
        """
        获取当前学校的学年学期列表
        :return:
        """
        return EducationModel.EduYearTerm.objects.filter(school=self.school)

    # 设置切换的学期信息
    def set_term_to_session(self, term):
        """
        设置切换的学期信息
        :param term:
        :return:
        """
        if term:
            self._request.session[system.WEJUDGE_EDUCATION_TERM_KEY % self.school.id] = self.term.id
        else:
            self._request.session[system.WEJUDGE_EDUCATION_TERM_KEY % self.school.id] = 0

    # 创建课程
    @EducationBaseController.login_validator
    @EducationBaseController.check_user_privilege_validator(2)
    def create_course(self):
        """
        创建课程
        :return:
        """
        parser = ParamsParser(self._request)
        teacher = parser.get_str("teacher", require=True, method="POST")
        cname = parser.get_str("name", require=True, method="POST", errcode=3210)
        academy = parser.get_int("academy", require=True, method="POST", errcode=3006)
        description = parser.get_str("description", '', method="POST")

        academy = self.school.eduacademy_set.filter(id=academy)
        if not academy.exists():
            raise WeJudgeError(3006)
        academy = academy[0]

        account = EducationModel.EduAccount.objects.filter(school=self.school, username=teacher, role__gte=2)
        if not account.exists():
            raise WeJudgeError(3005)
        account = account[0]

        course = EducationModel.Course()

        if self.term is None:
            # 如果当前没有选择学期信息，则使用学校默认学期
            if self.school.now_term is None:
                raise WeJudgeError(3007)
            course.term = self.school.now_term
        else:
            course.term = self.term

        course.school = self.school
        course.academy = academy
        course.name = cname
        course.author = account
        course.description = description
        course.save()

        course.teacher.add(account)
        course.save()

        return True

    # 获取教学账户列表
    @EducationBaseController.login_validator
    @EducationBaseController.check_user_privilege_validator(3)
    def get_account_list(self):

        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', 50)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        @WeJudgePagination(
            model_object=self._account_list_filter(EducationModel.EduAccount.objects.filter(school=self.school)),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 50),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_item(_account):
            account = _account.json(items=[
                'id', 'role', 'username', 'nickname', 'academy', 'academy_id',
                'realname', 'sex', 'locked', 'master', 'master__username'
            ])
            return account

        account_view = proc_item()
        return account_view

    # 新增或编辑用户信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_user_privilege_validator(3)
    def edit_account(self):
        """
        新增或编辑用户信息
        :return:
        """
        parser = ParamsParser(self._request)
        uid = parser.get_int('id', require=True, method="POST")
        username = parser.get_str('username', require=True, method="POST", errcode=3022)
        password = parser.get_str('password', "", method="POST")
        nickname = parser.get_str('nickname', require=True, method="POST", errcode=3023)
        realname = parser.get_str('realname', require=True, method="POST", errcode=3024)
        role = parser.get_int('role', require=True, method="POST")
        sex = parser.get_int('sex', -1, method="POST")
        academy = parser.get_int('academy', 0, method="POST")
        lock = parser.get_boolean('lock', False, method="POST")
        unbind = parser.get_boolean('unbind', False, method="POST")

        academy = self.get_academy(academy)

        if username[:len(self.school.short_name)] == self.school.short_name:
            raise WeJudgeError(3025)

        uca = EducationModel.EduAccount.objects.filter(school=self.school, username=username)

        # 新建
        if uid == 0:
            if uca.exists():
                raise WeJudgeError(3011)
            user = EducationModel.EduAccount()
            user.school = self.school

            if password.strip() == "":
                password = "%s12345678" % username
                user.password = tools.gen_passwd(password)

        else:
            user = EducationModel.EduAccount.objects.filter(school=self.school, id=uid)
            if not user.exists():
                raise WeJudgeError(1000)

            user = user[0]

            if uca.exists() and uca[0] != user:
                raise WeJudgeError(3011)

            suser = self.session.account
            if user == suser:
                if role != suser.role:
                    raise WeJudgeError(3012)
                if lock:
                    raise WeJudgeError(3013)

            if password.strip() != "":
                user.password = tools.gen_passwd(password)

            user.locked = lock

        user.username = username
        user.nickname = nickname
        user.realname = realname
        user.academy = academy
        user.role = role
        user.sex = sex

        user.save()

        # 刷新主账户密码
        if user.master is not None:
            user.master.password = user.password
            user.master.save()

        if role >= 2 and user.master is None:
            # 如果是教师角色，并且不存在主账户信息，那么创建主账户
            master_account = AccountModel.Account()
            master_account.password = user.password
            master_account.username = "%s%s" % (self.school.short_name, username)
            master_account.nickname = nickname
            master_account.realname = realname
            master_account.sex = sex
            # 允许创建比赛
            master_account.permission_create_contest = True
            # 允许发布题目
            master_account.permission_publish_problem = True
            # 允许创建题目集
            master_account.permission_create_problemset = True
            master_account.save()
            user.master = master_account
            user.save()
        if user.role == 0 and unbind:
            user.master = None
            user.save()

        # 新增或编辑用户信息

    # 从xls导入账户信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_user_privilege_validator(3)
    def xls_import_account(self):
        """
        从xls导入账户信息
        :return:
        """

        from django.db import transaction

        parser = ParamsParser(self._request)
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
                user_name = user_row[1]
                user_role = user_row[2]
                if user_id.strip() == '':
                    continue
                if user_name.strip() == "":
                    msg.append("用户[%s]缺少姓名，跳过" % user_id)
                    continue
                if user_role == "教务老师":
                    user_role = 3
                elif user_role == "教师":
                    user_role = 2
                else:
                    user_role = 0
                password = "%s12345678" % user_id
                user = EducationModel.EduAccount.objects.filter(school=self.school, username=user_id)
                if user.exists():
                    msg.append("用户已存在：%s" % user_id)
                else:
                    try:
                        user = EducationModel.EduAccount()
                        user.school = self.school
                        user.username = user_id
                        user.role = user_role
                        user.sex = -1
                        user.nickname = user_name
                        user.realname = user_name
                        user.password = tools.gen_passwd(password)
                        user.save()
                    except:
                        msg.append("处理失败：%s" % user_id)
                        transaction.rollback()
                        continue
        except Exception as ex:
            msg.append("处理XLS失败 [%s] " % ex)

        return "<br />".join(msg)

    # 删除用户
    @EducationBaseController.login_validator
    @EducationBaseController.check_user_privilege_validator(3)
    def delete_account(self):
        """
        删除用户
        :return:
        """

        parser = ParamsParser(self._request)
        uid = parser.get_int("id", require=True, method="GET")

        user = EducationModel.EduAccount.objects.filter(school=self.school, id=uid)
        if not user.exists():
            raise WeJudgeError(3005)

        if user[0] == self.session.account:
            raise WeJudgeError(3014)

        user[0].delete()

    # 获取学校的设置信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_user_privilege_validator(3)
    def get_schools_info(self):
        """
        获取学校的设置信息
        :return:
        """
        school = self.school.json(items=[
            'name', 'short_name', 'logo', 'description', 'now_term',
            'now_term_id', 'max_week', 'sections'
        ])
        terms = [term.json(items=[
            'id', 'year', 'term'
        ]) for term in self.school.eduyearterm_set.order_by('-id')]
        return {
            "school": school,
            "terms": terms
        }

    # 保存学校的设置信息
    def save_school_info(self):
        """
        保存学校的设置信息
        :return:
        """
        parser = ParamsParser(self._request)
        name = parser.get_str("name", require=True, method="POST", errcode=3016)
        short_name = parser.get_str("short_name", require=True, method="POST", errcode=3017)
        yearterm = parser.get_int("yearterm", require=True, method="POST", errcode=3018)
        description = parser.get_str("description", '', method="POST")
        max_week = parser.get_int("max_week", require=True, min=1, max=52, method="POST", errcode=3019)

        yearterm = self.school.eduyearterm_set.filter(id=yearterm)
        if not yearterm.exists():
            raise WeJudgeError(3003)
        yearterm = yearterm[0]

        self.school.now_term = yearterm
        self.school.name = name
        self.school.short_name = short_name
        self.school.description = description
        self.school.max_week = max_week
        self.school.save()

        return True

    # 增加/删除学年学期
    def change_year_terms(self):
        """
        增加/删除学年学期
        :return:
        """
        parser = ParamsParser(self._request)

        ytid = parser.get_int("id", min=0, method="POST")

        if ytid == 0:
            year = parser.get_int("year", min=1970, require=True, method="POST")
            term = parser.get_int("term", min=1, max=5, require=True, method="POST")
            yt = EducationModel.EduYearTerm()
            yt.school = self.school
            yt.year = year
            yt.term = term
            yt.save()

        else:
            remove = parser.get_boolean('remove', False, method='POST')
            if not remove:      # 反熊孩子保护机制
                return
            yt = self.school.eduyearterm_set.filter(id=ytid)
            if not yt.exists():
                raise WeJudgeError(3202)
            yt = yt[0]
            yt.delete()

    # 保存上课时间信息
    @EducationBaseController.login_validator
    @EducationBaseController.check_user_privilege_validator(3)
    def save_sections_data(self):
        """
        保存上课时间信息
        :return:
        """
        parser = ParamsParser(self._request)
        datas = parser.get_str("datas", require=True, method='POST')
        try:
            import json
            json.loads(datas)
        except:
            raise WeJudgeError(3015)

        self.school.sections = datas
        self.school.save()

    # 注册或者绑定WeJudge主账户
    @EducationBaseController.login_validator
    def master_register_or_bind(self):
        """
        注册或者绑定WeJudge主账户
        :return:
        """
        # 检查是否先前绑定过
        if self.session.account.master is not None:
            raise WeJudgeError(3020)

        parser = ParamsParser(self._request)
        mode = parser.get_str('mode', require=True, method='POST')
        if mode == 'register':
            nickname = parser.get_str('nickname', '', method='POST')
            password = parser.get_str('password', require=True, method='POST', errcode=1006)
            repassword = parser.get_str('repassword', require=True, method='POST', errcode=1008)
            if password != repassword:
                raise WeJudgeError(1007)

            username = "%s%s" % (self.school.short_name, self.session.account.username)
            uca = AccountModel.Account.objects.filter(username=username)
            if uca.exists():
                username = "%s%s " % (self.school.short_name, tools.gen_handle())
            uca = AccountModel.Account.objects.filter(nickname=nickname)
            if uca.exists():
                raise WeJudgeError(1108)

            if nickname.strip() == "":
                nickname = self.session.account.nickname

            account = AccountModel.Account()
            account.username = username
            account.nickname = nickname
            account.realname = self.session.account.realname
            account.password = tools.gen_passwd(password)
            account.save()
            self.session.account.master = account
            self.session.account.save()
            return "账号激活成功！请使用新的密码登录系统。"

        elif mode == 'login':

            username = parser.get_str('username', require=True, method='POST', errcode=1005)
            password = parser.get_str('password', require=True, method='POST', errcode=1006)
            user = AccountModel.Account.objects.filter(username=username)
            if not user.exists():
                raise WeJudgeError(1002)
            user = user[0]
            if user.locked:
                raise WeJudgeError(1003)

            if EducationModel.EduAccount.objects.filter(school=self.school, master=user).exists():
                raise WeJudgeError(3021)

            remote_pwd = str(user.password)
            now_pwd = str(tools.gen_passwd(password))
            if remote_pwd == now_pwd:
                self.session.account.master = user
                self.session.account.save()
            else:
                raise WeJudgeError(1002)

            return "账号关联成功！"

    @staticmethod
    # 搜索用户
    def search_user(keyword, sid, role=0):
        accounts = EducationModel.EduAccount.objects.filter(
            (Q(username__contains=keyword) | Q(realname__contains=keyword) | Q(nickname__contains=keyword)),
            role=role, school__id=sid
        )[:10]
        return accounts

    # 账户过滤器
    def _account_list_filter(self, alist):
        """
        账户过滤器
        :param alist: Account List
        :return:
        """

        parser = ParamsParser(self._request)
        keyword = parser.get_str('keyword', '')             # 用户名（或者真名、昵称
        role = parser.get_int('role', -1)                   # 用户角色
        academy = parser.get_int('academy', -1)             # 学院ID
        desc = parser.get_boolean('desc', default=False)    # 倒序排序

        if role > -1:
            alist = alist.filter(role=role)
        if academy > -1:
            alist = alist.filter(academy_id=academy)

        if (keyword is not None) and (keyword.strip() != ""):
            alist = alist.filter(
                Q(username__contains=keyword) |
                Q(nickname__contains=keyword) |
                Q(realname__contains=keyword)
            )

        if desc:
            alist = alist.order_by('-role', '-id')
        else:
            alist = alist.order_by('-role', 'id')

        return alist.all()
