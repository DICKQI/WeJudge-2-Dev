# -*- coding: utf-8 -*-
# coding:utf-8
import json
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
import wejudge.const.system

__author__ = 'lancelrq'


class WeJudgeError(Exception):

    def __init__(self, errcode, msg=None, data=None, action=None, httpcode=200):
        self.__errcode = errcode
        self.__httpcode = httpcode
        entity = wejudge.const.errors.get(errcode, wejudge.const.errors[0])
        self.__errmsg = entity[0] if msg is None else msg
        self.__action = entity[1] if action is None else action
        self.__data = data
        self._is_json = False
        Exception.__init__(self, self.__errmsg)

    def __str__(self):
        return repr(self.__errmsg)

    @staticmethod
    def __get_view_type(request):
        """
        获取view的预测渲染模型
        :param request: WSGIRequest()
        :return:
        """
        path = request.path
        if path[-5:] == '.json' or path[-3:] == '.do':
            return 'json'
        elif path[-4:] == '.txt' or path[-5:] == '.text':
            return 'text'
        else:
            return 'html'

    def get_response(self, request):
        """
        返回响应体
        :return:
        """
        response = HttpResponse('')
        response['Content-Type'] = 'text/plain'
        response.status_code = self.__httpcode
        view_type = WeJudgeError.__get_view_type(request)
        if view_type == 'json':
            response.content = json.dumps({
                "WeJudgeError": True,
                'data': self.__data,
                'errcode': self.__errcode,
                'errmsg': self.__errmsg,
                'action': self.__action
            })
            response['Content-Type'] = 'application/json'
        elif view_type == 'html':
            from django.shortcuts import render
            context = {
                "wejudge_navlist": [["错误提示"]],
                "WeJudgeError": True,
                'data': self.__data,
                'errcode': self.__errcode,
                'errmsg': self.__errmsg,
                'action': self.__action,
                'HTTP_REFERER': request.META.get('HTTP_REFERER', 'javascript:history.go(-1);'),
                'USER_AGENT': request.META.get('HTTP_USER_AGENT', ''),
            }

            if 3000 <= self.__errcode <= 3999:
                context['wejudge_appname'] = 'education'
            elif 5000 <= self.__errcode <= 5999:
                context['wejudge_appname'] = 'contest'
            #
            if self.__errcode != 1010:
                context['hide_login'] = True

            response.content = render(request, "error.tpl", context)
            response['Content-Type'] = 'text/html'
        elif view_type == 'text':
            response.content = self.__errmsg
        else:
            response.content = self.__errmsg

        return response


class Oauth2Error(Exception):

    def __init__(self, errcode, errmsg=None, data=None, httpcode=200):
        self.__errcode = errcode
        entity = wejudge.const.oauth2_errros.get(errcode, wejudge.const.oauth2_errros[0])
        self.__errmsg = entity[0] if errmsg is None else errmsg
        self.__httpcode = entity[1] if httpcode is None else httpcode
        self.__data = data
        self._is_json = False
        Exception.__init__(self, self.__errmsg)

    def __str__(self):
        return repr(self.__errmsg)

    def get_response(self, request):
        """
        返回响应体
        :return:
        """
        response = HttpResponse('')
        response['Content-Type'] = 'text/plain'
        response.status_code = self.__httpcode
        response.content = json.dumps({
            'data': self.__data,
            'errcode': self.__errcode,
            'errmsg': self.__errmsg,
        })
        response['Content-Type'] = 'application/json'

        return response

