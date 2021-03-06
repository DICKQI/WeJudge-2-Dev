# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from apps.account.libs import session as AccountLib

__author__ = 'lancelrq'


def logout_backend(request, cid):
    """
    WeJudge Contest 登出接口
    :param request:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request, cid)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    # 调用登出功能
    AccountLib.ContestAccountSessionManager(request, response).logout()

    return response.json(WeJudgeResult(msg="登出成功"))


def check_master_login(request, cid):
    """
    WeJudge Contest 账户主登录状态检测
    :param request:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request, cid)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    return response.json(WeJudgeResult(data=AccountLib.ContestAccountSessionManager(request, response).check_master_login()))


@WeJudgePOSTRequire
def login_backend(request, cid):
    """
    WeJudge Contest 登录检查接口
    :param request:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request, cid)   # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    # 调用登录功能
    AccountLib.ContestAccountSessionManager(request, response).login()

    return response.json(WeJudgeResult(msg="登录成功"))


@WeJudgePOSTRequire
def login_use_master(request, cid):
    """
    WeJudge Contest 关联登录接口
    :param request:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request, cid)   # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    # 调用登录功能
    AccountLib.ContestAccountSessionManager(request, response).login_use_master()

    return response.json(WeJudgeResult(msg="登录成功"))

