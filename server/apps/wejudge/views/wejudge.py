# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from django.core import urlresolvers
import wejudge.const as const
from django.conf import settings
from django.urls import RegexURLResolver
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_page
__author__ = 'lancelrq'


def index(request):
    """
    WeJugde首页
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    response.set_navlist([
        const.apps.WEJUDGE,
    ])

    a = urlresolvers.reverse("wejudge.index.index")
    return response.render_page(request, 'wejudge/index.tpl', {
        "hide_breadcrumb": True
    })


def sys_open_debug(request):
    from django.http.response import HttpResponse
    request.session['ADMIN_DEV_DEBUG'] = True

    return HttpResponse("Debug Details On.")


def sys_close_debug(request):
    from django.http.response import HttpResponse
    request.session['ADMIN_DEV_DEBUG'] = False

    return HttpResponse("Debug Details Off.")


def sys_debug_status(request):
    raise OSError("如果你看见了这个页面，说明已经成功的在当前会话开启了500错误详情显示")


def system_urls(request):
    urlconf = settings.ROOT_URLCONF
    urls_dict = RegexURLResolver(r'^/', urlconf).reverse_dict
    urls = {}

    for k in urls_dict:
        if type(k) == str:
            if str(k) in system.WEJUDGE_URLS_EXPORT_EXCEPT:
                continue
            v = urls_dict.getlist(k)
            urls[k] = v
    return JsonResponse(WeJudgeResult(urls).to_dict())
