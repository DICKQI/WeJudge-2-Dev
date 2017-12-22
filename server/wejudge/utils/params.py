# -*- coding: utf-8 -*-
# coding:utf-8
import logging
from wejudge.core import WeJudgeError
__author__ = 'lancelrq'

class ParamsParser(object):
    """
    HTTP参数解析处理程序
    """

    def __init__(self, request, exception_privider=WeJudgeError):
        self.__request = request
        self.__exception_provider = exception_privider

    def __get_query_set(self, method):
        if method.lower() == 'post':
            return self.__request.POST
        if method.lower() == 'session':
            return self.__request.session
        if method.lower() == 'cookie':
            return self.__request.COOKIES
        else:
            return self.__request.GET

    def __get_value(self, key, method='GET', require=False):

        queryset = self.__get_query_set(method)
        value = queryset.get(key, None)
        if require and (value is None):
            raise self.__exception_provider(1)
        if value is None:
            return ""
        return value

    def get_list(self, key, method='GET', require=False):
        queryset = self.__get_query_set(method)
        value = queryset.getlist(key, None)
        if require and (value is None):
            raise self.__exception_provider(1)
        if value is None:
            return []
        return value

    def get_int(self, key, default="0", min=None, max=None, method="GET", require=False, errcode=None):
        value = self.__get_value(key, method, require)
        if not require and value == "":
            value = default
        try:
            x = int(value)
        except BaseException as ex:
            raise self.__exception_provider(errcode or 1)

        if isinstance(min, int) and x < min:
            raise self.__exception_provider(errcode or 2)
        if isinstance(max, int) and x > max:
            raise self.__exception_provider(errcode or 2)
        return x


    def get_float(self, key, default="0", min=0, max=None, method="GET", require=False, errcode=None):
        value = self.__get_value(key, method, require)
        if not require and value == "":
            value = default
        try:
            x = float(value)
            if isinstance(min, float) and x < min:
                raise self.__exception_provider(errcode or 2)
            if isinstance(max, float) and x > max:
                raise self.__exception_provider(errcode or 2)
            return x
        except:
            raise self.__exception_provider(errcode or 1)

    def get_boolean(self, key, default="", method="GET", require=False):
        value = self.__get_value(key, method, require)
        if not require and value == "":
            value = default
        if value == 'true' or value == '1' or value == 'True' or value == 'T':
            return True
        else:
            return False

    def get_str(self, key, default="", method="GET", require=False, errcode=None):
        value = self.__get_value(key, method, require)
        if require and value == "":
            raise self.__exception_provider(errcode or 1)
        if value == "":
            value = default
        return value

    def get_file(self, key, type=None, require=False, max_size=1048576, allow_empty=False):
        file = self.__request.FILES.get(key, None)
        if require and file is None:
            raise self.__exception_provider(3)
        if type is not None and file.content_type not in type:
            raise self.__exception_provider(4, msg='上传文件类型不符合要求，仅支持：%s' % ",".join(type))
        if file.size > max_size:
            raise self.__exception_provider(5, msg='上传文件大小不符合要求，最大不能超过%s字节' % max_size)
        if not allow_empty and file.size == 0:
            raise self.__exception_provider(6)
        return file

    def get_datetime(self, key, default=None, format="%Y-%m-%d %H:%M:%S", method="GET", require=False, errcode=None):

        from django.utils.timezone import datetime

        value = self.__get_value(key, method, require)
        if not require and value == "":
            return None

        try:
            x = datetime.strptime(value, format)

        except BaseException as ex:
            raise self.__exception_provider(errcode or 1)

        return x