# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from wejudge.utils import tools
import apps.education.models as EducationModel
import apps.problem.models as ProblemModel

__author__ = 'lancelrq'


class EducationBaseController(WeJudgeControllerBase):

    def __init__(self, request, response, sid):
        """
        初始化
        :param request:
        :param response:
        :param sid: School ID
        """
        super(EducationBaseController, self).__init__(request, response)

        self.school = None
        self.term = None
        self.course = None
        self.asgn = None
        self.asgn_problem_item = None
        self.problem = None
        self.problem_set = None
        self.problem_set_item = None
        self.status = None
        self.repository = None

        self.get_school(sid)

        # 设置学校信息
        self.session.set_school_id(self.school.id)
        # 载入登录会话
        self.session.load_session()

        # 自动挂起子账户的功能
        auto_login = request.session.get('ONCE_AUTO_LOGIN_IF_ENTER_EDUCATION', False)
        if auto_login and self.session.master_logined:
            edu_acc = EducationModel.EduAccount.objects.filter(school=self.school, master=self.session.master)
            if edu_acc.exists():
                edu_acc = edu_acc[0]
                from apps.account.libs import session
                session.EducationAccountSessionManager(request, response).login_by_system(edu_acc)
                self.session.load_session()
            request.session.pop('ONCE_AUTO_LOGIN_IF_ENTER_EDUCATION')

        # 从学校记录或者Session获取学期信息（Session优先）
        tid = self._request.session.get(system.WEJUDGE_EDUCATION_TERM_KEY % sid, None)
        if (tid == 0) or (tid is None):
            self.term = self.school.now_term
        else:
            if tid is None:
                tid = 0
            self.get_term(tid)

    # 获取学期信息
    def get_term(self, tid):
        """
        获取学期信息
        :param tid: Team ID
        :return:
        """
        term = EducationModel.EduYearTerm.objects.filter(school=self.school, id=tid)
        if term.exists():
            self.term = term[0]
            return term[0]
        else:
            self.term = None
            return None

    # 获取学期信息
    def get_academy(self, aid):
        """
        获取学期信息
        :param aid: Academy ID
        :return:
        """
        academy = EducationModel.EduAcademy.objects.filter(school=self.school, id=aid)
        if academy.exists():
            return academy[0]
        else:
            return None

    # 获取学校记录
    def get_school(self, sid):
        """
        获取学校记录
        :return:
        """
        school = EducationModel.EduSchool.objects.filter(id=sid)
        if school.exists():
            self.school = school[0]
            return True
        else:
            raise WeJudgeError(3000)

    # 获取课程信息
    def get_course(self, cid):
        """
        获取课程信息
        :return:
        """
        course = EducationModel.Course.objects.filter(id=cid)
        if course.exists():
            self.course = course[0]
            return True
        else:
            raise WeJudgeError(3004)

    # 读取作业信息
    def get_asgn(self, aid):
        """
        读取作业信息
        :param aid: 作业id
        :return:
        """
        asgn = EducationModel.Asgn.objects.filter(id=aid)
        if asgn.exists():
            self.asgn = asgn[0]
            self.course = self.asgn.course
            return True
        else:
            raise WeJudgeError(3004)

    # 获取Status信息
    def get_status(self, sid):
        """
        获取Status信息
        :param sid:
        :return:
        """
        status_item = EducationModel.JudgeStatus.objects.filter(id=sid)
        if status_item.exists():
            self.status = status_item[0]
        else:
            raise WeJudgeError(3301)

    # 获取当前学校内的学院数据
    def get_school_academies(self):
        academies = self.school.eduacademy_set.all()
        return academies

    # 获取当前学校的学期信息
    def get_school_terms(self):
        eduyearterms = self.school.eduyearterm_set.all()
        return eduyearterms

    # 获取用户信息（不抛异常）
    def get_account(self, user_id):
        """
        获取用户信息（不抛异常）
        :param user_id: 用户ID
        :return: 用户信息对象
        """
        account = EducationModel.EduAccount.objects.filter(school=self.school, id=user_id)
        if account.exists():
            return account[0]
        else:
            return None

    # 检查助教权限并且提权
    def check_assistant(self):
        """
        检查助教权限并且提权
        :return:
        """
        if not self.session.is_logined():
            return
        author = self.session.account
        course = self.course
        if course is None:
            return
        if author.role >= 2:
            return
        if course.assistants.filter(id=author.id).exists():
            self.session.account_manager.entity.role = 1
            # self.session.account.role = 1     这句可以有，不过没必要，毕竟直接改manager来的直接

    # 登录检查器(教学系统专用)
    def login_check(self, throw=True):
        """
        登录检查器(教学系统专用)
        :param throw: 是否抛出异常
        :return:
        """
        if self.session is None or not self.session.is_logined():
            if throw:
                raise WeJudgeError(3010)
            else:
                return False
        else:
            return True

    # 通过当前用户角色来检查是否拥有权限(作业）
    def check_user_privilege(self, role=0, throw=True):
        """
        通过当前用户信息来检查是否拥有权限(这里并不检查是否登录！之前没检查出事自己负责
        :param role: 用户角色请求（mixed）
        :param throw: 是否抛出异常
        :return:
        """
        user = self.session.account
        if user.role >= role:
            return True
        else:
            if throw:
                raise WeJudgeError(3120)
            else:
                return False

    # 检查作业的访问权限
    def check_asgn_visit(self, throw=True):
        """
        检查作业的访问权限
        :param throw:
        :return: (signal, dec): (-2无权限；[-1, 0, 1]不同时间段；2管理权限 ， 剩余秒；不存在则为-1 )
        """

        user = self.session.account

        if user.role == 0:

            # 排课检查
            flag, st, et = self._get_students_arrangment()
            if flag is False:
                if throw:
                    raise WeJudgeError(3101)
                return -2, -1  # 无权限
            # 时间检查
            flag, dec = tools.check_time_passed(st, et)

            # 已有实验报告的可以进入
            if EducationModel.AsgnReport.objects.filter(asgn=self.asgn, author=user).exists():
                return flag, dec.total_seconds()

            else:       # 没有实验报告的，没开始就不能进
                if flag < 0:
                    raise WeJudgeError(3112)
            return flag, dec.total_seconds()

        elif user.role == 1:
            if self.asgn.course.assistants.filter(id=user.id).exists():
                return 2, -1    # 管理访问
            else:
                if throw:
                    raise WeJudgeError(3101)
                return -2, -1

        elif user.role == 2:
            # 该作业非当前教师发布
            if user.id != self.asgn.teacher_id:
                if throw:
                    raise WeJudgeError(3101)
                return -2, -1   # 无权限
            else:
                return 2, -1  # 管理访问

        elif user.role == 3:
            return 2, -1        # 教务老师有全部权限

        else:
            if throw:
                raise WeJudgeError(3101)
            return -2, -1       # 无权限

    # 检查课程访问的权限
    def check_course_visit(self, throw=True):
        """
        检查课程访问的权限
        :param throw:
        :return:
        """

        user = self.session.account

        if user.role == 2:
            if self.course.teacher.filter(id=user.id).exists():
                return True
            if user.id == self.course.author_id:
                return True
            if throw:
                raise WeJudgeError(3215)
            else:
                return False

        elif user.role == 3:
            return True        # 教务老师有全部权限
        elif user.role == 1:
            return True        # 由于这个角色只能通过提权实现，所以直接返回True就好了

        else:

            for arr in self.course.arrangements.all():
                if arr.students.filter(id=user.id).exists():
                    return True

            if throw:
                raise WeJudgeError(3215)
            else:
                return False

    # 检查课程管理的权限
    def check_course_manager(self, the_creater=False, throw=True):
        """
        检查课程管理的权限
        :param throw:
        :param the_creater:
        :return:
        """

        user = self.session.account

        if user.role == 2:
            if not the_creater:
                if self.course.teacher.filter(id=user.id).exists():
                    return True
                if user.id == self.course.author_id:
                    return True
                if throw:
                    raise WeJudgeError(3205)
                else:
                    return False
            else:
                if user.id == self.course.author_id:
                    return True
                else:
                    if throw:
                        raise WeJudgeError(3206)
                    else:
                        return False

        elif user.role == 3:
            return True  # 教务老师有全部权限

        if throw:
            raise WeJudgeError(3205)
        else:
            return False

    # 学生的选课检查
    def _get_students_arrangment(self):
        """
        学生的选课检查
        :return:
        """
        user = self.session.account
        vreq = EducationModel.AsgnVisitRequirement.objects.filter(author=user, asgn=self.asgn)
        if vreq.exists():
            vreq = vreq[0]
            varg = self.asgn.access_control.filter(enabled=True, arrangement=vreq.arrangement)
            if varg.exists():
                varg = varg[0]
                return True, varg.start_time, varg.end_time

        access_list = self.asgn.access_control.filter(enabled=True)

        start_time = None
        end_time = None

        if not access_list.exists():
            return False, None, None

        for access in access_list:

            # 返回第一条选课记录（理论上是，排课系统会剔除重复选课记录）
            stus = access.arrangement.students.filter(id=user.id)
            if stus.exists():
                if start_time is None:
                    start_time = access.start_time
                if end_time is None:
                    end_time = access.end_time

                start_time = min(start_time, access.start_time)
                end_time = max(end_time, access.end_time)

        if start_time is None or end_time is None:
            return False, None, None
        else:
            return True, start_time, end_time

    # 题目访问和管理权限检查实现（在别的地方可以重写！）
    def check_problem_privilege(self, privilege_code=1, throw=True):
        """
        题目访问和管理权限检查实现
        :param throw:
        :param privilege_code: 权限请求值，定义如下：
        > 0 == 不请求权限
        > 1 == read    访问题目内容，查看统计
        > 2 == judge   提交评测
        > 4 == data    访问题目示例代码、测试数据、设置等，同时也运行访问所有此题目的评测历史详情
        > 8 == write   修改题目内容、示例代码、测试数据、设置等
        :return:
        """
        # 获取主账户信息
        # 子系统账号不用检查是否登录，因为只有登录了才能访问题目！
        user = self.session.account
        master = self.session.master
        if master is None:
            master = self.session.account.master

        if self.problem is not None:
            # 题目发布者、系统管理员 拥有无限权限
            if master is not None and (master == self.problem.author or master.permission_administrator):
                return True
            else:
                if privilege_code == 0:
                    return True
                if privilege_code > 0:
                    if privilege_code > 2:
                        # 如果是助教、老师、或者是教务，才检查高级权限
                        if user.role > 1:
                            if tools.check_privilege(privilege_code, self.problem.permission):
                                # 检查混合权限请求
                                return True
                    else:
                        # 这一步不需要检查管理权限
                        if tools.check_privilege(privilege_code, self.problem.permission):
                            # 检查混合权限请求
                            return True
        # 不支持在作业系统增加题目
        else:
            pass

        if throw:
            raise WeJudgeError(3203)
        else:
            return False

    # 通过当前用户角色来检查是否拥有权限（装饰器）
    @staticmethod
    def check_user_privilege_validator(role):
        """
        通过当前用户角色来检查是否拥有权限（装饰器）
        :param role:
        :return:
        """
        def d(func):
            def wrapper(*args, **kwargs):
                self = args[0]
                self.check_user_privilege(role=role)
                return func(*args, **kwargs)
            return wrapper
        return d

    # 检查作业的访问权限（装饰器）
    @staticmethod
    def check_asgn_visit_validator(flag_enable=(-1, 0, 1), roles=(0,)):
        """
        检查作业的访问权限（装饰器）
        :param flag_enable: -1: 未开始, 0：运行中, 1：已结束
        :param roles: 需要判定的角色
        :return:
        """
        def d(func):
            def wrapper(*args, **kwargs):
                self = args[0]
                flag, dec = self.check_asgn_visit()

                if flag not in flag_enable:
                    if self.session.account.role in roles:
                        if flag == -1:
                            raise WeJudgeError(3195)
                        elif flag == 0:
                            raise WeJudgeError(3196)        # 这个似乎很少会用到
                        elif flag == 1:
                            raise WeJudgeError(3197)

                return func(*args, **kwargs)

            return wrapper
        return d

    # 检查课程管理的权限（装饰器）
    @staticmethod
    def check_course_manager_validator(the_creater=False):
        """
        检查课程管理的权限
        :param the_creater:
        :return:
        """
        def d(func):
            def wrapper(*args, **kwargs):
                self = args[0]
                self.check_course_manager(the_creater=the_creater)
                return func(*args, **kwargs)
            return wrapper
        return d

    # 检查课程访问的权限（装饰器）
    @staticmethod
    def check_course_visit_validator(func):
        """
        检查课程访问的权限
        :return:
        """
        def wrapper(*args, **kwargs):
            self = args[0]
            self.check_course_visit()
            return func(*args, **kwargs)
        return wrapper

    # 评测历史访问权限鉴定（重写）
    def judge_status_privilege(self, throw=True):
        """
        评测历史访问权限鉴定（重写）
        :param throw:
        :return:
        """
        user = self.session.account
        status = self.status
        if status.author == user:
            # 学生本人可以看自己的评测详情
            return True
        else:
            # 助教以上可以看
            if user.role >= 1:
                return True

        if throw:
            raise WeJudgeError(3110)
        else:
            return False

    # 检查访问仓库的权限
    def check_repo_visit_privilege(self, manager=False, throw=True):
        """
        检查访问仓库的权限
        :param throw:
        :param manager: 请求管理权限
        :return:
        """
        user = self.session.account
        if user is not None:
            # 教务无限制权限
            if user.role == 3:
                return True

        if manager:
            # 如果请求的是管理权限
            if user is not None and user == self.repository.author:
                return True

            if throw:
                raise WeJudgeError(3402)
            else:
                return False

        else:

            if self.repository.public_level == 0:
                # 私有
                if self.course is None:
                    if user == self.repository.author:
                        return True
                else:
                    # 如果是从课程页面进去的
                    if self.course.repositories.filter(id=self.repository.id).exists():
                        return True

            elif self.repository.public_level == 1:
                # 学校内访问
                if user is not None:
                    return True
            else:
                # 游客访问
                return True

            if throw:
                raise WeJudgeError(3401)
            else:
                return False

    # 检查访问仓库的权限（装饰器）
    @staticmethod
    def check_repo_visit_validator(manager=False):
        """
        检查访问仓库的权限
        :param manager:
        :return:
        """
        def d(func):
            def wrapper(*args, **kwargs):
                self = args[0]
                self.check_repo_visit_privilege(manager=manager)
                return func(*args, **kwargs)

            return wrapper
        return d