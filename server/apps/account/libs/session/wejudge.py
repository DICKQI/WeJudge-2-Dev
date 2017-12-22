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

__author__ = 'lancelrq'


# WeJudge主账户 会话功能控制类
class WeJudgeAccountSessionManager(WeJudgeControllerBase):

    def __init__(self, request, response):
        """
        初始化
        :param request: django request 对象
        :param response: django response 对象
        :return:
        """
        super(WeJudgeAccountSessionManager, self).__init__(request, response)

    # 通过用户名字段找到用户信息（子系统应该继承重写）
    def _find_by_username(self, username):
        """
        通过用户名字段找到用户信息（子系统继承重写）
        :param username: 用户输入的用户名/Email
        :return: 是否找到，找到的用户/错误代码
        """

        # 判断是否无内容
        if username.strip() == '':
            return False, -1  # 用户名或密码为空

        # 通用账户
        user = AccountModel.Account.objects.filter(username=username)
        if user.exists():
            user = user[0]
        else:
            # 通过email来查询
            user = AccountModel.Account.objects.filter(email=username, email_validated=True)
            if user.exists():
                user = user[0]
            else:
                return False, -2  # 用户名或密码错误

        return True, user

    # 写入登录会话（子系统应该继承重写）
    def _create_login_session(self, user, remember_me=False, login_master=True):
        """
        写入登录会话（子系统继承重写）
        :param user:  账户实体
        :param login_master:
        :return:
        """
        # 创建登录manager
        _account = WeJudgeAccount(user)
        # 写入登录会话
        self._request.session[system.WEJUDGE_ACCOUNT_SESSION] = _account.dump_session_data()
        # 处理记住登录
        if remember_me:
            self._create_login_cookie(_account.dump_session_data())

    # 账号检查（不建议重写）
    def _check(self, username, password):
        """
        账号检查（不建议重写）
        :param username:
        :param password:
        :return: 检查是否通过, 错误代码（正数表示重试密码锁定剩余时间，0表示通过）, 用户实体（子账户也返回它自己而不是返回主账户
        """

        _rel, _msg = self._find_by_username(username)
        if not _rel:
            return False, _msg, None

        user = _msg
        master = user.master if (hasattr(user, 'master') and user.master is not None) else None

        # 检查用户是否锁定
        if user.locked:
            return False, -4, None
        # 检查主账户是否锁定
        if master is not None and master.locked:
            return False, -4, None

        # 这个是后续用来操作密码检查的账户变量
        account = user if master is None else master

        # 密码策略：如果账户拥有主账户，则一致使用主账户的密码，而不会去使用它的密码，统一为了更好的管理

        # 检查是否因为重复输入密码而锁定
        _rel, _sec, _user = self.__check_login_retry_lock(account)
        if _rel is False:
            return False, _sec, None   # 尝试过多, 剩余时间

        # 计算密码
        remote_pwd = str(account.password)
        now_pwd = str(tools.gen_passwd(password))

        # 校验密码
        if remote_pwd == now_pwd:
            if account.passwd_retry_counter != system.WEJUDGE_ACCOUNT_LOGIN_RETRY_TOTAL:
                # 如果密码错重试次数不为重置密码重试次数
                self.__clean_login_retry_counter(account)

            # 检查通过
            return True, 0, user

        else:
            # 设置密码错误计数
            self.__set_login_retry_counter(account)
            # 重复输入密码次数过多, 锁定
            if user.passwd_retry_counter <= 0:
                return self.__check_login_retry_lock(account)  # 锁定, 剩余时间
            else:
                return False, -2, None  # 用户名或密码错误

    # 登录操作（不建议重写）
    def login(self):
        """
        登录操作
        :param username: 输入的用户名
        :param password: 输入的密码
        :param remember_me: 是否记住登录（仅用于主账户，子账户的话，必须是login_master=True才有效果）
        :param login_master: 登录子账户的同时登录主账户
        :return:
        """
        parser = ParamsParser(self._request)
        username = parser.get_str("username", require=True, method="POST", errcode=1005)
        password = parser.get_str("password", require=True, method="POST", errcode=1006)
        remember_me = parser.get_boolean("remember_me", False, method="POST")
        login_master = parser.get_boolean("login_master", True, method="POST")

        rel, msg, user = self._check(username, password)

        if rel:
            # 登录检查成功
            master = user.master if (hasattr(user, 'master') and user.master is not None) else None
            # 创建登录状态业务逻辑
            self._create_login_session(user, remember_me, login_master)
            # 写入最后登录时间
            user.last_login_time = datetime.datetime.now()
            user.save()
            if master is not None:
                # 刷新最后登录时间
                master.last_login_time = datetime.datetime.now()
                master.save()

        else:
            # 登录检查失败
            msg_convert = {
                "-1": 1001,
                "-2": 1002,
                "-3": 1002,
                "-4": 1003,
            }
            if msg > 0:
                raise WeJudgeError(1004)
            else:
                raise WeJudgeError(msg_convert.get(str(msg), 0))

    # 系统挂起登录
    def login_by_system(self, account):
        """
        系统挂起登录
        :param account: 输入特定的账号模型，自动挂起登录信息
        :return:
        """
        self._create_login_session(account, False, False)

    def register(self):
        """
        注册主账户
        :return: 返回新的账户实体
        """
        parser = ParamsParser(self._request)
        username = parser.get_str('username', require=True, method="POST", errcode=1005)
        password = parser.get_str('password', require=True, method="POST", errcode=1006)
        repassword = parser.get_str('repassword', require=True, method="POST", errcode=1008)
        nickname = parser.get_str('nickname', require=True, method="POST", errcode=1102)
        email = parser.get_str('email', require=True, method="POST", errcode=1106)

        if password.strip() != "":
            if password != repassword:
                raise WeJudgeError(1007)

        uca = AccountModel.Account.objects.filter(username=username)
        if uca.exists():
            raise WeJudgeError(1103)
        uca = AccountModel.Account.objects.filter(nickname=nickname)
        if uca.exists():
            raise WeJudgeError(1108)

        account = AccountModel.Account()
        account.username = username
        account.nickname = nickname
        account.realname = ""
        account.password = tools.gen_passwd(password)
        account.emalil = email
        account.save()

        return account

    # 写登录记住Cookie
    def _create_login_cookie(self, session_info):
        """
        写登录记住Cookie
        :param response: django response对象
        :param user: User Entity
        :return:
        """
        session_info["expire_at"] = int(time.time()) + system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME
        login_token = json.dumps(session_info)
        token_signature = tools.token_hmac_sha512_singature(login_token)

        # 写Cookie(需要传入Response对象)
        self._response.set_cookie(system.WEJUDGE_ACCOUNT_COOKIE_TOKEN_KEY, login_token,
                                   expires=system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME)
        self._response.set_cookie(system.WEJUDGE_ACCOUNT_COOKIE_SIGNATURE_KEY, token_signature,
                                   expires=system.WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME)

    # 清除用户登录记录
    def _clean_login_cookie(self):
        """
        清除用户登录记录
        :param user:
        :return:
        """
        self._response.set_cookie(system.WEJUDGE_ACCOUNT_COOKIE_TOKEN_KEY, '', expires=-1)
        self._response.set_cookie(system.WEJUDGE_ACCOUNT_COOKIE_SIGNATURE_KEY, '', expires=-1)

    # 登出操作（子系统应该重写！）
    def logout(self):
        """
        登出操作
        :return:
        """
        if self._response.session.is_logined():
            # 清除Session
            if system.WEJUDGE_ACCOUNT_SESSION in self._request.session:
                self._request.session.pop(system.WEJUDGE_ACCOUNT_SESSION)
            if system.WEJUDGE_EDU_ACCOUNT_SESSION in self._request.session:
                self._request.session.pop(system.WEJUDGE_EDU_ACCOUNT_SESSION)
            if system.WEJUDGE_CONTEST_ACCOUNT_SESSION in self._request.session:
                self._request.session.pop(system.WEJUDGE_CONTEST_ACCOUNT_SESSION)
            # 清除Cookie
            self._clean_login_cookie()

    # 设置密码错误重试次数
    def __set_login_retry_counter(self, user):
        """
        设置密码错误重试次数
        :return:
        """
        c = user.passwd_retry_counter - 1
        if c <= 0:
            self._request.session[
                system.WEJUDGE_ACCOUNT_LOGIN_SESSION_RETRY_TIME
            ] = int(time.time()) + system.WEJUDGE_ACCOUNT_LOGIN_RETRY_WAIT_TIME
        user.passwd_retry_counter = c
        user.save(force_update=True)

    # 清除密码错误重试次数
    def __clean_login_retry_counter(self, user):
        """
        清除密码错误重试次数
        :return:
        """
        self._request.session[
            system.WEJUDGE_ACCOUNT_LOGIN_SESSION_RETRY_TIME
        ] = 0
        user.passwd_retry_counter = system.WEJUDGE_ACCOUNT_LOGIN_RETRY_TOTAL
        user.save(force_update=True)

    # 检查是否锁定
    def __check_login_retry_lock(self, user):
        """
        检查是否锁定
        :return:
        """
        if system.WEJUDGE_ACCOUNT_LOGIN_SESSION_RETRY_TIME in self._request.session:
            login_allow_time = int(self._request.session.get(system.WEJUDGE_ACCOUNT_LOGIN_SESSION_RETRY_TIME))
            now = int(time.time())
            # 判断是否超出锁定时间
            if login_allow_time > now:
                p = login_allow_time - now
                return False, p, None
            else:
                user.passwd_retry_counter = system.WEJUDGE_ACCOUNT_LOGIN_RETRY_TOTAL
                user.save()
        return True, 0, user
