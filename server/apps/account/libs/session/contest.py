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
import apps.contest.models as ContestModel
from .wejudge import WeJudgeAccountSessionManager

__author__ = 'lancelrq'


# 比赛系统账号 会话功能控制类
class ContestAccountSessionManager(WeJudgeAccountSessionManager):

    def __init__(self, request, response):
        super(ContestAccountSessionManager, self).__init__(request, response)
        if not isinstance(self.session, WeJudgeContestSession):
            raise WeJudgeError(2)

    # 检查Master账户的登录情况
    def check_master_login(self):
        """
        检查Master账户的登录情况
        :return:
        """
        if not self.session.is_master_logined():
            return None
        else:
            master = self.session.master
            user = ContestModel.ContestAccount.objects.filter(contest_id=self.session.get_contest_id(), master=master)
            if not user.exists():
                return None
            user = user[0]
            return {
                "user": user.json(items=[
                    'id', 'username', 'nickname', 'headimg'
                ]),
                "master": master.json(items=[
                    'id', 'username', 'nickname', 'headimg'
                ])
            }

    # 使用Master账户的登录信息挂起关联账户的登录状态
    def login_use_master(self):
        # 检查账户关联
        if not self.session.is_master_logined():
            raise WeJudgeError(1011)
        else:
            master = self.session.master
            user = ContestModel.ContestAccount.objects.filter(contest_id=self.session.get_contest_id(), master=master)
            if not user.exists():
                raise WeJudgeError(1011)
            user = user[0]
        # 挂起登录会话
        self._create_login_session(user, remember_me=False, login_master=False)

    # 通过用户名字段找到用户信息
    def _find_by_username(self, username):

        # 判断是否无内容
        if username.strip() == '':
            return False, -1  # 用户名或密码为空

        # 通用账户
        user = ContestModel.ContestAccount.objects.filter(contest_id=self.session.get_contest_id(), username=username)
        if user.exists():
            user = user[0]
            return True, user

        return False, -2  # 用户名或密码错误

    # 写入登录会话
    def _create_login_session(self, user, remember_me=False, login_master=True):
        _contest_id = str(self.session.get_contest_id())
        # 创建登录manager
        _account = WeJudgeContestAccount(user, _contest_id)

        # 写入登录会话
        _session_raw = self._request.session.get(system.WEJUDGE_CONTEST_ACCOUNT_SESSION, {})
        _session_raw[_contest_id] = _account.dump_session_data()
        self._request.session[system.WEJUDGE_CONTEST_ACCOUNT_SESSION] = _session_raw

        token_signature = tools.token_hmac_sha512_singature(_session_raw)
        self._response.set_cookie(system.WEJUDGE_CONTEST_ACCOUNT_SESSION_SIGNATURE_KEY, token_signature,
                                  expires=system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME)

        # 挂起主账户的登录状态，如果已经登录，则复写
        if hasattr(user, 'master') and user.master is not None and login_master:
            super(ContestAccountSessionManager, self)._create_login_session(user.master, remember_me,
                                                                              login_master)

    # 登出操作不会干涉到主账户！
    def logout(self):
        # 清除Session
        _contest_id = str(self.session.get_contest_id())
        _session_raw = self._request.session.get(system.WEJUDGE_CONTEST_ACCOUNT_SESSION, {})
        _session_raw[_contest_id] = None
        self._request.session[system.WEJUDGE_CONTEST_ACCOUNT_SESSION] = _session_raw
    #
    # # 写入登录会话
    # def _create_login_session(self, user, remember_me=False, login_master=True):
    #
    #     _contest_id = str(self.session.get_contest_id())
    #     # 创建登录manager
    #     _account = WeJudgeContestAccount(user, _contest_id)
    #     # 写入登录会话
    #     _session_raw = self._request.COOKIES.get(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_TOKEN_KEY, "{}")
    #     try:
    #         _session_raw = json.loads(_session_raw)
    #     except:
    #         _session_raw = {}
    #
    #     _session_raw[str(_contest_id)] = _account.dump_session_data()
    #     # 过期时间
    #     _session_raw["expire_at"] = int(time.time()) + system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME
    #     login_token = json.dumps(_session_raw)
    #     token_signature = tools.token_hmac_sha512_singature(login_token)
    #
    #     # 写Cookie(需要传入Response对象)
    #     self._response.set_cookie(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_TOKEN_KEY, login_token,
    #                               expires=system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME)
    #     self._response.set_cookie(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_SIGNATURE_KEY, token_signature,
    #                               expires=system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME)
    #
    #     # 挂起主账户的登录状态，如果已经登录，则复写
    #     if hasattr(user, 'master') and user.master is not None and login_master:
    #         super(ContestAccountSessionManager, self)._create_login_session(user.master, remember_me, login_master)
    #
    # # 登出操作不会干涉到主账户！
    # def logout(self):
    #     _contest_id = str(self.session.get_contest_id())
    #     _session_raw = self._request.COOKIES.get(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_TOKEN_KEY, "{}")
    #     try:
    #         _session_raw = json.loads(_session_raw)
    #     except:
    #         _session_raw = {}
    #     _session_raw[_contest_id] = None
    #
    #     # 过期时间
    #     _session_raw["expire_at"] = int(time.time()) + system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME
    #     login_token = json.dumps(_session_raw)
    #     token_signature = tools.token_hmac_sha512_singature(login_token)
    #
    #     # 写Cookie(需要传入Response对象)
    #     self._response.set_cookie(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_TOKEN_KEY, login_token,
    #                               expires=system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME)
    #     self._response.set_cookie(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_SIGNATURE_KEY, token_signature,
    #                               expires=system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME)