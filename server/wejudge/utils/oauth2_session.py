# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import time
import datetime
import json
import hashlib


class WeJudgeOauth2Session(object):
    """
    WeJudge 主账户系统管理器
    """

    def __init__(self, request):
        """
        初始化
        :param request: django request 对象
        :return:
        """

        self._request = request                  # HTTP请求对象

        if not hasattr(self, 'dont_init'):
            self.dont_init = False

        self._is_logined = False
        self._is_master_logined = False
        self._account_manager = None
        self._master_account_manager = None

        from wejudge.core.error import Oauth2Error
        from .params import ParamsParser
        parser = ParamsParser(request, exception_privider=Oauth2Error)
        self.appid = parser.get_str('appid', require=True, errcode=40000)
        self.openid = parser.get_str('openid', require=True, errcode=40001, method='POST')
        self.access_token = parser.get_str('access_token', require=True, errcode=40004, method='POST')
        if not self.dont_init:
            self.init_context()
            # 初始化主账户系统
            self.load_session()

    def __getattr__(self, item):
        # 子账户登录状态
        if 'logined' == str(item):
            return self._is_logined

        # 主账户登录状态
        if 'master_logined' == str(item):
            return self._is_master_logined

        # 子账户实体
        elif 'account' == str(item):
            if self._account_manager is None:
                return None
            return self._account_manager.entity

        # 主账户实体
        elif 'master' == str(item):
            if self._master_account_manager is None:
                return None
            return self._master_account_manager.entity

        # 子账户管理器
        elif 'account_manager' == str(item):
            return self._account_manager

        # 主账户管理器
        elif 'master_account_manager' == str(item):
            return self._master_account_manager

        else:
            return object.__getattribute__(self, item)

    # 判断是否已经登录
    def is_logined(self):
        """
        判断是否已经登录
        :return:
        """
        return self._is_logined

    # 判断主账户是否登录
    def is_master_logined(self):
        """
        判断主账户是否登录
        :return:
        """
        return self._is_master_logined

    # 初始化会话上下文
    def init_context(self):
        """
        初始化会话上下文
        :return:
        """
        self._is_logined = False                    # 子账户是否登录
        self._is_master_logined = False             # 主账户是否登录
        self._account_manager = None                # 子账户管理器（也可以存储主账户管理器）
        self._master_account_manager = None         # 主账户管理器

    # 从Session里读取登录信息
    def load_session(self):
        """
        从Session里读取登录信息
        :param request:
        :return:
        """
        from .account import WeJudgeAccount
        from wejudge.core.error import Oauth2Error
        import apps.oauth2.models as Oauth2Model

        # 检查Client
        client = Oauth2Model.Client.objects.filter(app_id=self.appid)
        if not client.exists():
            raise Oauth2Error(40000)
        client = client[0]
        # 通过OpenID获取用户信息
        uu = Oauth2Model.OauthUser.objects.filter(client=client, open_id=self.openid, account_type="wejudge")
        if not uu.exists():
            raise Oauth2Error(40001)
        oauth_user = uu[0]
        # 判断AccessToken是否有效
        at = oauth_user.tokens.filter(access_token=self.access_token)
        if at.exists():
            at = at[0]
            if at.expires_at <= int(time.time()):
                at.delete()
                raise Oauth2Error(40004)
        else:
            raise Oauth2Error(40004)

        # 使用Session信息构造账户管理器
        account = WeJudgeAccount(json.dumps({
            "user_id": oauth_user.account_id
        }))
        if account is None or account.entity.locked:
            return False

        # 表达登录状态
        self._is_logined = True
        self._is_master_logined = True
        self._account_manager = account
        self._master_account_manager = account
        return True

#
#
# class WeJudgeContestSession():
#
#     """
#     比赛子账户系统管理器
#
#     :description 这里其实会出现一种情况，就是子账户属于未登录状态，主账户属于登录状态，这是合法的
#     """
#
#     def __init__(self, request, contest_id=None):
#         """
#         初始化
#         :param request: django request 对象
#         :param contest_id: Contest_id，弱校验，但是确保传入的没问题，这个由controllerbase决定
#         :return:
#         """
#         self.contest_id = contest_id
#         super(WeJudgeContestSession, self).__init__(request)
#
#     def set_contest_id(self, contest_id):
#         """
#         设置Contest Id
#         :param contest_id:
#         :return:
#         """
#         self.contest_id = contest_id
#
#     def get_contest_id(self):
#         """
#         获取Contest ID
#         :return:
#         """
#         return self.contest_id
#
#     def load_session(self):
#         """
#         （重写）载入Session
#         :return:
#         """
#         from wejudge.core.error import WeJudgeError
#
#         if self.contest_id is None:
#             raise WeJudgeError(100)
#
#         from wejudge.const import system
#         from .account import WeJudgeContestAccount
#
#         # 调用父级方法，拉取主账户登录信息
#         super(WeJudgeContestSession, self)._load_session()
#
#         # 清理子账户管理器
#         # 由于要处理子账户的上下文了所以一定要初始化不然的话会出事的。
#         self._is_logined = False                    # 子账户是否登录
#         self._account_manager = None                # 子账户管理器（也可以存储主账户管理器）
#
#         _session_key = system.WEJUDGE_CONTEST_ACCOUNT_SESSION % self.contest_id
#         # 载入子账户系统的session
#         _session_data = self._request.session.get(_session_key, None)
#         # 如果无法访问session，再见吧您嘞
#         if _session_data is None:
#             return False
#
#         account = WeJudgeContestAccount(_session_data, self.contest_id)
#         if account is None or account.entity.locked:
#             # 如果Session信息未能成功构造或者账户被锁(子账户），则删除并且返回未登录状态
#             # 注意，不需要再检查主账户了，反正调用父方法的时候已经确认了主账户没有被锁定了
#             self._request.session[_session_key] = None
#             del self._request.session[_session_key]
#             return False
#
#         # 表达登录状态
#         self._is_logined = True
#         self._account_manager = account
#         return True


class WeJudgeEducationOauth2Session(WeJudgeOauth2Session):
    """
    教学子账户系统管理器

    :description 这里其实会出现一种情况，就是子账户属于未登录状态，主账户属于登录状态，这是合法的
    """

    def __init__(self, request, school_id=None):
        """
        初始化
        :param request: django request 对象
        :param school_id: school_id，弱校验，但是确保传入的没问题，这个由controllerbase决定
        :return:
        """
        self.dont_init = True
        self.school_id = school_id
        super(WeJudgeEducationOauth2Session, self).__init__(request)

    def set_school_id(self, school_id):
        """
        设置School Id
        :param school_id:
        :return:
        """
        self.school_id = school_id

    def get_school_id(self):
        """
        获取School ID
        :return:
        """
        return self.school_id

    def load_session(self):
        """
        （重写）载入Session
        :return:
        """
        from wejudge.core.error import WeJudgeError

        if self.school_id is None:
            raise WeJudgeError(100)

        self._is_logined = False
        self._account_manager = None

        from wejudge.const import system
        from .account import WeJudgeEducationAccount, WeJudgeAccount
        from wejudge.core.error import Oauth2Error
        import apps.oauth2.models as Oauth2Model

        # 检查Client
        client = Oauth2Model.Client.objects.filter(app_id=self.appid)
        if not client.exists():
            raise Oauth2Error(40000)
        client = client[0]
        # 通过OpenID获取用户信息
        uu = Oauth2Model.OauthUser.objects.filter(client=client, open_id=self.openid, account_type="education")
        if not uu.exists():
            raise Oauth2Error(40001)
        oauth_user = uu[0]
        # 判断AccessToken是否有效
        at = oauth_user.tokens.filter(access_token=self.access_token)
        if at.exists():
            at = at[0]
            if at.expires_at <= int(time.time()):
                at.delete()
                raise Oauth2Error(40004)
        else:
            raise Oauth2Error(40004)

        account = WeJudgeEducationAccount(json.dumps({
            "user_id": oauth_user.account_id
        }), self.school_id)

        if account is None or account.entity.locked:
            return False

        # 表达登录状态
        self._is_logined = True
        self._account_manager = account
        if account.entity.master is not None:
            self._is_master_logined = True
            self._master_account_manager = WeJudgeAccount(account.entity.master)
        return True
