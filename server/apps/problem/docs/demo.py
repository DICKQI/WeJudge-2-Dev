# -*- coding: utf-8 -*-
# coding:utf-8
from wejudge.core import *
from wejudge.utils import *
import apps.problem.models as ProblemModel

__author__ = 'lancelrq'


class ProblemSetManager(object):

    def __init__(self, request, response):
        """
        初始化
        :param request: django request 对象
        :param response: WeJudge response 对象
        """
        self.__request = request        # HTTP请求对象
        self.__response = response      # HTTP应答对象
        if isinstance(response, WeJudgeResponse):
            self.session = response.session
        else:
            self.session = {}