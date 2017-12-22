# -*- coding: utf-8 -*-
# coding:utf-8
import json
from django.http.response import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import render

__author__ = 'lancelrq'

class WeJudgeResponse(HttpResponse):
    """
    WeJudge前端响应封装框架(渲染页面)
    """

    def __init__(self,  session_manager, *args, **kwargs):
        super(WeJudgeResponse, self).__init__(b'', *args, **kwargs)
        self.session = session_manager
        self.navlist = []
        self['Content-Type'] = 'text/html'

    def set_navlist(self, _navlist):
        self.navlist = _navlist

    def text(self, body):
        """
        响应文本
        :return:
        """
        self.content = body
        self['Content-Type'] = 'text/plain'
        return self

    def html(self, body):
        """
        响应网页
        :return:
        """
        self.content = body
        self['Content-Type'] = 'text/html'
        return self

    def render_page(self, request, template_file, context=None):
        """
        渲染页面（封装django的render）
        :param template_file:
        :param context:
        :return:
        """
        from wejudge.utils import tools
        # from wejudge.utils.session import WeJudgeContestSession, WeJudgeEducationSession
        #
        # app_name = "wejudge"
        #
        # if isinstance(self.session, WeJudgeEducationSession):
        #     app_name = "education"
        #
        # if isinstance(self.session, WeJudgeEducationSession):
        #     app_name = "contest"

        _context = {
            # "wejudge_appname": app_name,        # 账户子系统名称
            "wejudge_navlist": tools.gen_navgation(self.navlist),
            "wejudge_session": self.session,
        }

        if context is not None and isinstance(context, dict):
            _context.update(context)
        self.content = render(request, template_file, _context)
        self['Content-Type'] = 'text/html'
        return self

    def json(self, data):
        """
         JSON渲染
        :param data: 支持类：list、dict、set、tuple、WeJudgeResult
        :return:
        """
        from .result import WeJudgeResult

        self['Content-Type'] = 'application/json'

        if data is None:
            self.content = '{}'
        elif isinstance(data, WeJudgeResult):
            self.content = data.dump()
        elif isinstance(data, dict) or isinstance(data, list) or isinstance(data, set) or isinstance(data, tuple):
            self.content = json.dumps(data)
        else:
            self.content = '{}'
        return self


class WeJudgeFileResponse(FileResponse):
    """
    WeJudge 文件响应
    """

    def __init__(self, streaming_content=(), file_name='download', *args, **kwargs):
        """
        下载流格式
        :param streaming_content:
        :param file_name:
        :return:
        """
        super(WeJudgeFileResponse, self).__init__(streaming_content, *args, **kwargs)
        self['Content-Disposition'] = 'attachment; filename=%s' % file_name


def WeJudgePOSTRequire(func):
    """
    强制POST请求装饰器
    :param func: 函数
    :return:
    """
    from .error import WeJudgeError

    def wrapper(*args, **kw):
        if isinstance(args[0], HttpRequest):
            request = args[0]
            print([x for x in kw])
            if request.method != 'POST':
                raise WeJudgeError(40501, 405)

        return func(*args, **kw)
    return wrapper


def WeJudgeGETRequire(func):
    """
    强制GET请求装饰器
    :param func: 函数
    :return:
    """
    from .error import WeJudgeError

    def wrapper(*args, **kw):
        if isinstance(args[0], HttpRequest):
            request = args[0]
            print([x for x in kw])
            if request.method != 'GET':
                raise WeJudgeError(40500, 405)

        return func(*args, **kw)
    return wrapper