# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from apps.account.libs import session as AccountLib

__author__ = 'lancelrq'


# === APIS ===

@WeJudgePOSTRequire
def login_backend(request):
    """
    WeJudge 登录检查接口
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)   # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    # 调用登录功能
    AccountLib.WeJudgeAccountSessionManager(request, response).login()

    # 注册一个一次性标记，用于第一次进入教学系统时自动挂起此主账户关联的子账户。
    request.session['ONCE_AUTO_LOGIN_IF_ENTER_EDUCATION'] = True

    return response.json(WeJudgeResult(msg="登录成功"))


def logout_backend(request):
    """
    WeJudge 登出接口
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    # 调用登出功能
    AccountLib.WeJudgeAccountSessionManager(request, response).logout()

    return response.json(WeJudgeResult(msg="登出成功"))


@WeJudgePOSTRequire
def register(request):
    """
    WeJudge 注册入口
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    # 调用注册功能
    AccountLib.WeJudgeAccountSessionManager(request, response).register()

    return response.json(WeJudgeResult(msg="注册成功"))
