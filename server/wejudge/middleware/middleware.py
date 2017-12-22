# -*- coding: utf-8 -*-
# coding:utf-8

import sys
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response, ExceptionReporter
from django.http.response import HttpResponse
from django.conf import settings

__author__ = 'lancelrq'


class WeJudgeMiddleware(MiddlewareMixin):


    def process_request(self, request):
        """
        响应处理
        :param request:
        :return:
        """

    def process_response(self, request, response):
        """
        处理应答部分
        :param request:
        :param response:
        :return:
        """
        return response

    def process_exception(self, request, exception):
        """
        异常处理
        :param request:
        :param exception:
        :return:
        """
        from wejudge.core import WeJudgeError, Oauth2Error

        if isinstance(exception, WeJudgeError) or isinstance(exception, Oauth2Error):
            return exception.get_response(request)

        if settings.DEBUG or request.session.get('ADMIN_DEV_DEBUG') is True:
            # return HttpResponse('{"WeJudgeError": true, "errmsg": "内部服务错误" }')
            return technical_500_response(request, *sys.exc_info())
        else:
            return HttpResponse("Oh, Oop!OJ好像出现了一点问题 >.< ")
