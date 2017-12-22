# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import time
import datetime
import json
import hashlib


class WeJudgeSession(object):
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

        self._is_logined = False  # 子账户是否登录
        self._is_master_logined = False  # 主账户是否登录
        self._account_manager = None  # 子账户管理器（也可以存储主账户管理器）
        self._master_account_manager = None  # 主账户管理器

        self._init_context()
        # 初始化主账户系统
        self._load_session()

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
    def _init_context(self):
        """
        初始化会话上下文
        :return:
        """
        self._is_logined = False                    # 子账户是否登录
        self._is_master_logined = False             # 主账户是否登录
        self._account_manager = None                # 子账户管理器（也可以存储主账户管理器）
        self._master_account_manager = None         # 主账户管理器

    # 从Session里读取登录信息
    def _load_session(self):
        """
        从Session里读取登录信息
        :param request:
        :return:
        """

        from wejudge.const import system
        from .account import WeJudgeAccount

        self._init_context()


        _session_data = self._request.session.get(system.WEJUDGE_ACCOUNT_SESSION, None)
        # 如果无法访问session，
        # try:
        #     if int(_session_data.get('user_id', '0')) > 2:
        #         return False
        # except:
        #     return False

        if _session_data is None:
            # 尝试从Cookie中获取持久化登录的信息
            if self._load_cookies():
                # 重新读入session
                _session_data = self._request.session.get(system.WEJUDGE_ACCOUNT_SESSION, None)
                # 如果再次读入失败，返回未登录
                if _session_data is None:
                    return False
            else:
                return False

        # 使用Session信息构造账户管理器
        account = WeJudgeAccount(_session_data)
        if account is None or account.entity.locked:
            # 如果Session信息未能成功构造或者账户被锁(主账户），则删除并且返回未登录状态
            self._request.session[system.WEJUDGE_ACCOUNT_SESSION] = None
            del self._request.session[system.WEJUDGE_ACCOUNT_SESSION]
            return False
        elif _session_data.get('username', '') != account.entity.username \
                or _session_data.get('user_id', 0) != account.entity.id:
            # 校验失败
            self._request.session[system.WEJUDGE_ACCOUNT_SESSION] = None
            del self._request.session[system.WEJUDGE_ACCOUNT_SESSION]
            return False

        # 表达登录状态
        self._is_logined = True
        self._is_master_logined = True
        self._account_manager = account
        self._master_account_manager = account
        return True

    # 从Cookie里恢复登录信息（Cookie 只支持主账户）
    def _load_cookies(self):
        """
        从Cookie里恢复登录信息
        :return:
        """
        import time
        from wejudge.const import system
        from django.utils.timezone import now
        from .account import WeJudgeAccount
        from apps.account.models import Account
        from .tools import token_hmac_sha512_singature

        # 从Cookie中获取主账户的登录校验信息（令牌）
        user_token = self._request.COOKIES.get(system.WEJUDGE_ACCOUNT_COOKIE_TOKEN_KEY, None)
        if user_token is None or user_token.strip() == '':
            return False

        # 从Cookie中获取主账户的Token
        user_signature = self._request.COOKIES.get(system.WEJUDGE_ACCOUNT_COOKIE_SIGNATURE_KEY, '')

        if token_hmac_sha512_singature(user_token) != user_signature:
            return False

        try:
            user_info = json.loads(user_token)
        except:
            return False

        # 检查过期
        expire_at = user_info.get('expire_at', -1)
        if int(time.time()) >= expire_at:
            return False

        user = Account.objects.filter(id=user_info.get('user_id', ''))
        if user.exists():
            # 获取登录用户
            user = user[0]
            entity = user
        else:
            return False

        # 处理锁定的情况
        if entity.locked:
            return False

        account_manager = WeJudgeAccount(entity)
        # 未过期
        self._request.session[system.WEJUDGE_ACCOUNT_SESSION] = account_manager.dump_session_data()
        # 刷新最后登录时间（因为属于登录信息恢复的动作）
        entity.last_login_time = datetime.datetime.now()
        entity.save()
        return True


class WeJudgeContestSession(WeJudgeSession):

    """
    比赛子账户系统管理器

    :description 这里其实会出现一种情况，就是子账户属于未登录状态，主账户属于登录状态，这是合法的
    """

    def __init__(self, request, contest_id=None):
        """
        初始化
        :param request: django request 对象
        :param contest_id: Contest_id，弱校验，但是确保传入的没问题，这个由controllerbase决定
        :return:
        """
        self.contest_id = contest_id
        super(WeJudgeContestSession, self).__init__(request)

    def set_contest_id(self, contest_id):
        """
        设置Contest Id
        :param contest_id:
        :return:
        """
        self.contest_id = contest_id

    def get_contest_id(self):
        """
        获取Contest ID
        :return:
        """
        return self.contest_id

    def load_session(self):
        """
        （重写）载入Session
        :return:
        """
        from wejudge.core.error import WeJudgeError

        if self.contest_id is None:
            raise WeJudgeError(100)

        from wejudge.const import system
        from .account import WeJudgeContestAccount

        # 调用父级方法，拉取主账户登录信息
        super(WeJudgeContestSession, self)._load_session()

        # 清理子账户管理器
        # 由于要处理子账户的上下文了所以一定要初始化不然的话会出事的。
        self._is_logined = False                    # 子账户是否登录
        self._account_manager = None                # 子账户管理器（也可以存储主账户管理器）

        # # 载入子账户系统的session
        # _session_raw = self.__load_cookies()
        # if _session_raw is False:
        #     return None

        # 载入子账户系统的session
        _session_raw = self._request.session.get(system.WEJUDGE_CONTEST_ACCOUNT_SESSION, {})

        # 从Cookie中获取Signature
        user_signature = self._request.COOKIES.get(system.WEJUDGE_CONTEST_ACCOUNT_SESSION_SIGNATURE_KEY, '')
        from .tools import token_hmac_sha512_singature
        if token_hmac_sha512_singature(_session_raw) != user_signature:
            return False

        # 读取Session字典
        _session_data = _session_raw.get(str(self.contest_id), None)
        # 如果无法访问session，再见吧您嘞
        if _session_data is None:
            return False

        account = WeJudgeContestAccount(_session_data, self.contest_id)
        if account is None or account.entity.locked:
            # 如果Session信息未能成功构造或者账户被锁(子账户），则删除并且返回未登录状态
            # 注意，不需要再检查主账户了，反正调用父方法的时候已经确认了主账户没有被锁定了
            _session_raw[str(self.contest_id)] = None
            self._request.session[system.WEJUDGE_CONTEST_ACCOUNT_SESSION] = _session_raw
            return False
        if _session_data.get('username', '') != account.entity.username \
                or _session_data.get('user_id', 0) != account.entity.id:
            _session_raw[str(self.contest_id)] = None
            self._request.session[system.WEJUDGE_CONTEST_ACCOUNT_SESSION] = _session_raw
            return False

        # 表达登录状态
        self._is_logined = True
        self._account_manager = account
        return True

        # 从Cookie里恢复登录信息（Cookie 只支持主账户）

    # def __load_cookies(self):
    #     """
    #     从Cookie里恢复登录信息
    #     :return:
    #     """
    #     import time
    #     from wejudge.const import system
    #     from .tools import token_hmac_sha512_singature
    #
    #     # 从Cookie中获取主账户的登录校验信息（令牌）
    #     user_token = self._request.COOKIES.get(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_TOKEN_KEY, None)
    #     if user_token is None or user_token.strip() == '':
    #         return False
    #
    #     # 从Cookie中获取主账户的Token
    #     user_signature = self._request.COOKIES.get(system.WEJUDGE_CONTEST_ACCOUNT_COOKIE_SIGNATURE_KEY, '')
    #
    #     if token_hmac_sha512_singature(user_token) != user_signature:
    #         return False
    #
    #     try:
    #         user_info = json.loads(user_token)
    #     except:
    #         return False
    #
    #     # 检查过期
    #     expire_at = user_info.get('expire_at', -1)
    #     if int(time.time()) >= expire_at:
    #         return False
    #
    #     return user_info


class WeJudgeEducationSession(WeJudgeSession):
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
        self.school_id = school_id
        super(WeJudgeEducationSession, self).__init__(request)

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

        from wejudge.const import system
        from .account import WeJudgeEducationAccount

        # 调用父级方法，拉取主账户登录信息
        super(WeJudgeEducationSession, self)._load_session()

        # 清理子账户管理器
        # 由于要处理子账户的上下文了所以一定要初始化不然的话会出事的。
        self._is_logined = False                    # 子账户是否登录
        self._account_manager = None                # 子账户管理器（也可以存储主账户管理器）

        # # 载入子账户系统的session
        # _session_raw = self.__load_cookies()
        # if _session_raw is False:
        #     return None

        # 载入子账户系统的session
        _session_raw = self._request.session.get(system.WEJUDGE_EDU_ACCOUNT_SESSION, {})
        # 从Cookie中获取Signature
        user_signature = self._request.COOKIES.get(system.WEJUDGE_EDU_ACCOUNT_SESSION_SIGNATURE_KEY, '')
        from .tools import token_hmac_sha512_singature
        if token_hmac_sha512_singature(_session_raw) != user_signature:
            return False

        # 读取Session字典
        _session_data = _session_raw.get(str(self.school_id), None)
        # 如果无法访问session，再见吧您嘞
        if _session_data is None:
            return False



        account = WeJudgeEducationAccount(_session_data, self.school_id)
        if account is None or account.entity.locked:
            # 如果Session信息未能成功构造或者账户被锁(子账户），则删除并且返回未登录状态
            # 注意，不需要再检查主账户了，反正调用父方法的时候已经确认了主账户没有被锁定了
            _session_raw[str(self.school_id)] = None
            self._request.session[system.WEJUDGE_EDU_ACCOUNT_SESSION] = _session_raw
            return False
        if _session_data.get('username', '') != account.entity.username \
                or _session_data.get('user_id', 0) != account.entity.id:
            _session_raw[str(self.school_id)] = None
            self._request.session[system.WEJUDGE_EDU_ACCOUNT_SESSION] = _session_raw
            return False

        # 表达登录状态
        self._is_logined = True
        self._account_manager = account
        return True

    #
    # def __load_cookies(self):
    #     """
    #     从Cookie里恢复登录信息
    #     :return:
    #     """
    #     import time
    #     from wejudge.const import system
    #
    #
    #     # 从Cookie中获取主账户的登录校验信息（令牌）
    #     user_token = self._request.COOKIES.get(system.WEJUDGE_EDU_ACCOUNT_COOKIE_TOKEN_KEY, None)
    #     if user_token is None or user_token.strip() == '':
    #         return False
    #
    #     # 从Cookie中获取主账户的Token
    #     user_signature = self._request.COOKIES.get(system.WEJUDGE_EDU_ACCOUNT_COOKIE_SIGNATURE_KEY, '')
    #
    #     if token_hmac_sha512_singature(user_token) != user_signature:
    #         return False
    #
    #     try:
    #         user_info = json.loads(user_token)
    #     except:
    #         return False
    #
    #     # 检查过期
    #     expire_at = user_info.get('expire_at', -1)
    #     if int(time.time()) >= expire_at:
    #         return False
    #
    #     return user_info
