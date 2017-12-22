# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from wejudge.utils import tools
import apps.contest.models as ContestModel
import apps.problem.models as ProblemModel
from django.utils.timezone import localtime

__author__ = 'lancelrq'


class ContestBaseController(WeJudgeControllerBase):

    def __init__(self, request, response, cid):
        """
        初始化
        :param request:
        :param response:
        """
        super(ContestBaseController, self).__init__(request, response)

        self.contest = None
        self.contest_problem_item = None
        self.problem = None
        self.status = None

        self.get_contest(cid)

        # 设置比赛信息
        self.session.set_contest_id(self.contest.id)
        # 载入登录会话
        self.session.load_session()

        # if self.session.master_logined:
        #     cnt_acc = ContestModel.ContestAccount.objects.filter(contest=self.contest, master=self.session.master)
        #     if cnt_acc.exists():
        #         cnt_acc = cnt_acc[0]
        #         from apps.account.libs import session
        #         session.ContestAccountSessionManager(request, response).login_by_system(cnt_acc)
        #         self.session.load_session()

    # 获取比赛记录
    def get_contest(self, cid):
        """
        获取比赛记录
        :return:
        """
        contest = ContestModel.Contest.objects.filter(id=cid)
        if contest.exists():
            self.contest = contest[0]
            return True
        else:
            raise WeJudgeError(5000)

    # 获取Status信息
    def get_status(self, sid):
        """
        获取Status信息
        :param sid:
        :return:
        """
        status_item = self.contest.judge_status.filter(id=sid)
        if status_item.exists():
            self.status = status_item[0]
        else:
            raise WeJudgeError(5202)

    # 获取题目信息
    def get_problem(self, pid):
        """
        获取problem信息
        :param pid:
        :return:
        """
        contest = self.contest

        problem_item = contest.problems.filter(id=pid)
        if not problem_item.exists():
            raise WeJudgeError(5200)  # 找不到题目信息
        problem_item = problem_item[0]
        self.contest_problem_item = problem_item

        self.problem = problem_item.entity

    # 读取或创建当前用户的解决问题信息
    def get_contest_solution(self):
        """
        读取或创建当前用户的解决问题信息
        :return:
        """
        contest = self.contest
        author = self.session.account

        apv = ContestModel.ContestSolution.objects.filter(contest=contest, author=author, problem=self.contest_problem_item)
        if not apv.exists():
            apv = ContestModel.ContestSolution()
            apv.problem = self.contest_problem_item
            apv.author = author
            apv.contest = contest
            apv.save()
        else:
            apv = apv[0]

        return apv

    # 获取比赛的文件系统
    def get_contest_storage(self):
        """
        获取比赛的文件系统
        :return:
        """
        return WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CONTEST_STORAGE, str(self.contest.id))

    # 检测封榜
    def check_rank_stop(self):
        """
        检测封榜
        :return: False：不封，True：封
        """

        if self.session.account.role in (1, 2):
            return False

        if self.contest.rank_list_stop_at is None:
            return False

        from django.utils.timezone import now
        now_time = now()

        # 超出封榜时间
        if self.contest.rank_list_stop_at < now_time < self.contest.end_time:
            return True
        else:
            return False

    # 登录检查器(重写父类方法)
    def login_check(self, throw=True):
        """
        登录检查器(教学系统专用)
        :param throw: 是否抛出异常
        :return:
        """
        if self.session is None or not isinstance(self.session, WeJudgeContestSession) or not self.session.is_logined():
            if throw:
                raise WeJudgeError(5010)
            else:
                return False
        else:
            return True

    # 通过当前用户角色来检查是否拥有权限
    def check_privilege(self, role=0, throw=True):
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
                raise WeJudgeError(5001)
            else:
                return False

    # 题目访问和管理权限检查实现（重写！）
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

        # 如果是修改和管理题目
        if self.problem is not None:
            # 题目发布者、系统管理员 拥有无限权限
            if master is not None and (master == self.problem.author or master.permission_administrator):
                return True
            else:
                if privilege_code == 0:
                    return True
                if privilege_code > 0:
                    if privilege_code > 2:
                        # 至少是裁判身份，才检查更高的权限（一般用到的是看数据
                        if user.role >= 1:
                            if tools.check_privilege(privilege_code, self.problem.permission):
                                # 检查混合权限请求
                                return True
                    else:
                        # 这一步不需要检查管理权限
                        if tools.check_privilege(privilege_code, self.problem.permission):
                            # 检查混合权限请求
                            return True
        else:
            # 不支持在比赛里发布题目
            pass

        if throw:
            raise WeJudgeError(2201)
        else:
            return False

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
            # 参赛者本人可以看自己的评测详情
            return True
        else:
            # 裁判和发起人可以看评测详情
            if user.role in [1, 2]:
                return True

        if throw:
            raise WeJudgeError(5203)
        else:
            return False

    # 检查比赛状态(仅参赛者可用）
    def check_timepassed(self, throw=True, **kwargs):
        """
        检查比赛状态
        :param status: 状态，取值-1， 0， 1
        :param throw: 是否抛出异常
        :return:
        """
        if self.session.is_logined():
            user = self.session.account
            if kwargs.get('ignore_admin', True) and user.role in [1, 2]:
                return True

        flag, delta = tools.check_time_passed(self.contest.start_time, self.contest.end_time)
        if 'status' in kwargs.keys():
            if flag == kwargs.get('status', -1):
                return True
        elif 'status__gt' in kwargs.keys():
            if flag > kwargs.get('status__gt', -1):
                return True
        elif 'status__lt' in kwargs.keys():
            if flag < kwargs.get('status__lt', -1):
                return True

        if throw:
            raise WeJudgeError(kwargs.get('errcode', 5002))
        else:
            return False

    # 检验数据令牌
    def check_readonly_access_token(self, throw=True):
        access_token = self._request.GET.get('access_token', '')
        if access_token.strip() != "":
            if self.contest.access_token == access_token:
                return True

        if throw:
            raise WeJudgeError(5218)
        else:
            return False

    # 通过当前用户角色来检查是否拥有权限（装饰器）
    @staticmethod
    def check_privilege_validator(role):
        """
        通过当前用户角色来检查是否拥有权限（装饰器）
        :param role:
        :return:
        """
        def d(func):
            def wrapper(*args, **kwargs):
                self = args[0]
                self.check_privilege(role=role)
                return func(*args, **kwargs)
            return wrapper
        return d

    # 检查比赛状态(仅参赛者可用）（装饰器）
    @staticmethod
    def check_timepassed_validator(*a, **k):
        """
        检查比赛状态(仅参赛者可用）（装饰器）
        :param k:
        :return:
        """
        def d(func):
            def wrapper(*args, **kwargs):
                self = args[0]
                self.check_timepassed(*a, **k)
                return func(*args, **kwargs)
            return wrapper
        return d

    # 检验数据令牌（装饰器）
    @staticmethod
    def check_readonly_access_token_validator(func):
        """
        检验数据令牌（装饰器）
        :return:
        """
        def wrapper(*args, **kwargs):
            self = args[0]
            self.check_readonly_access_token()
            return func(*args, **kwargs)
        return wrapper
