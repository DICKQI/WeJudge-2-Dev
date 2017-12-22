# -*- coding: utf-8 -*-
# coding:utf-8

__author__ = 'lancelrq'


class WeJudgeControllerBase(object):

    def __init__(self, request, response):
        """
        初始化
        :param request: django request 对象
        :param response: WeJudge response 对象
        """
        from wejudge.core import WeJudgeResponse

        self._request = request        # HTTP请求对象
        self._response = response      # HTTP应答对象
        if isinstance(response, WeJudgeResponse):
            self.session = response.session
        else:
            self.session = None

    # 登录检查器（装饰器）
    @staticmethod
    def login_validator(func):
        """
        登录检查器（装饰器）
        :return:
        """
        from wejudge.core.error import WeJudgeError

        def wrapper(*args, **kwargs):

            self = args[0]
            self.login_check()

            return func(*args, **kwargs)

        return wrapper

    def login_check(self, throw=True):
        """
        登录检查器
        :param throw:
        :return:
        """
        if self.session is None:
            return False

        from wejudge.core.error import WeJudgeError
        if not self.session.is_logined():
            if throw:
                raise WeJudgeError(1010)
            else:
                return False
        else:
            return True
