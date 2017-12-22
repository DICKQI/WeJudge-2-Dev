# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
from django.core import urlresolvers
import wejudge.const as const
from django.views.decorators.cache import cache_page
__author__ = 'lancelrq'


def faq(request):
    """
    WeJugde首页
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    response.set_navlist([
        const.apps.HELP,
    ])

    return response.render_page(request, 'helper/index.tpl')

