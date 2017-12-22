# -*- coding: utf-8 -*-
# coding:utf-8

import json
import time
import datetime
from django.utils.timezone import now
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.account.models as AccountModel
import apps.education.models as EducationModel
import apps.problem.models as ProblemModel
from django.db.models import Q

from .wejudge import WeJudgeAccountSpace

__author__ = 'lancelrq'


# 教学中心子账户个人空间 控制类
class EducationAccountSpace(WeJudgeAccountSpace):

    def __init__(self, request, response, school_id, account_id):
        """
        初始化
        :param request: django request 对象
        :param response: django response 对象
        :param school_id: 学校ID
        :param account_id: 账号ID
        :return:
        """
        self.school = None
        self.get_school(school_id)
        super(EducationAccountSpace, self).__init__(request, response, account_id)
        # 设置学校信息
        self.session.set_school_id(self.school.id)
        # 载入登录会话
        self.session.load_session()
        self.headimg_storage_dir = 'education'

    # 获取用户的展示信息
    @WeJudgeControllerBase.login_validator
    def get_account_info(self):
        """
        获取用户的展示信息
        :return:
        """
        account_info = self.account.json(items=[
            'id', 'username', 'nickname', 'realname', 'sex', 'headimg', 'role',
            'motto', 'create_time', 'last_login_time', 'master', 'master__id',
            'master__nickname', 'master__username', 'master_heading'
        ])
        if self.account.master is not None:
            if self.account.master.last_login_time is not None:
                account_info['last_login_time'] = self.account.master.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                account_info['last_login_time'] = ""
        sv = {
            'total': self.account.solution_set.count(),
            'solved': self.account.solution_set.filter(accepted__gt=0).count()
        }
        account_info['solution_visited'] = sv
        return account_info

    # 读取用户的做题信息
    @WeJudgeControllerBase.login_validator
    def get_user_problem_solutions(self):
        """
        读取用户的做题信息
        :return:
        """
        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        solutions = EducationModel.Solution.objects.filter(author=self.account)

        @WeJudgePagination(
            model_object=self._solutions_filter(solutions),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_solutions_item(sol):
            view_item = sol.json(items=[
                'id', 'problem', 'problem__entity', 'problem__entity__title', 'problem__entity__id',
                'asgn', 'asgn__id', 'asgn__title', 'accepted', 'submission', 'penalty',
                'best_memory', 'best_time', 'best_code_size', 'score', 'used_time_real', 'used_time'
            ])
            return view_item

        result = proc_solutions_item()
        return result

    # 保存用户信息
    @WeJudgeControllerBase.login_validator
    @WeJudgeAccountSpace.self_account_validator
    def save_account_infos(self):
        """
        保存用户信息
        :return:
        """

        parser = ParamsParser(self._request)
        password = parser.get_str('password', require=True, method="POST", errcode=1104)
        newpassword = parser.get_str('newpassword', "", method="POST")
        renewpassword = parser.get_str('renewpassword', "", method="POST")
        nickname = parser.get_str('nickname', require=True, method="POST", errcode=1102)
        motto = parser.get_str('motto', '', method="POST")
        sex = parser.get_int('sex', -1, method="POST")

        # # 如果有master的话就不能改密码了
        # if self.account.master is None:
        #     if tools.gen_passwd(password) != self.account.master.password:
        #         raise WeJudgeError(1104)
        #
        #     if newpassword.strip() != "":
        #         if newpassword == renewpassword:
        #             self.account.password = tools.gen_passwd(newpassword)
        #         else:
        #             raise WeJudgeError(1105)
        # else:
        #     if tools.gen_passwd(password) != self.account.password:
        #         raise WeJudgeError(1104)

        if tools.gen_passwd(password) != self.account.master.password:
            raise WeJudgeError(1104)

        if newpassword.strip() != "":
            if newpassword == renewpassword:
                self.account.password = tools.gen_passwd(newpassword)
                # 自动刷新主账户密码
                if self.account.master is not None:
                    self.account.master.password = self.account.password
                    self.account.master.save()
            else:
                raise WeJudgeError(1105)

        if self.account.nickname != nickname:
            uca = EducationModel.EduAccount.objects.filter(school=self.school, nickname=nickname)
            if uca.exists() and uca[0] != self.account:
                raise WeJudgeError(1108)

        self.account.nickname = nickname

        self.account.sex = sex
        if self.account.master is not None:
            self.account.master.sex = sex
            self.account.master.save()

        self.account.motto = motto

        self.account.save()

    # 读取账号
    def get_account(self, account_id):
        """
        获取账户信息
        :return:
        """
        account = EducationModel.EduAccount.objects.filter(id=account_id, school=self.school)
        if account.exists():
            self.account = account[0]
        else:
            raise WeJudgeError(3005)

    # 读取账号（静态）
    @staticmethod
    def get_account_static(account_id, school_id):
        """
        读取账号
        :return:
        """
        school = EducationAccountSpace.get_school_static(school_id)
        if school is None:
            return None
        account = EducationModel.EduAccount.objects.filter(id=account_id, school=school)
        if account.exists():
            return account[0]
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

    # 获取学校记录
    @staticmethod
    def get_school_static(sid):
        """
        获取学校记录
        :return:
        """
        school = EducationModel.EduSchool.objects.filter(id=sid)
        if school.exists():
            return school[0]
        else:
            return None

    # 解决方案过滤器
    def _solutions_filter(self, solist):
        """
        解决方案过滤器
        :param solist:
        :return:
        """

        parser = ParamsParser(self._request)
        keyword = parser.get_str('keyword', '')             # 关键字(problem id）

        if (keyword is not None) and (keyword.strip() != ""):
            if tools.is_numeric(keyword):
                solist = solist.filter(problem__entity__id__contains=keyword)
        return solist.order_by('-id')
