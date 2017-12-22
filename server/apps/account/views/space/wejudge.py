# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
from wejudge.const import system
from apps.account.libs import space as AccountSpaceLib

__author__ = 'lancelrq'


def space(request, aid):
    """
    WeJudge 个人中心
    :param request:
    :param aid:
    :return:
    """

    wejudge_session = WeJudgeSession(request)               # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = AccountSpaceLib.WeJudgeAccountSpace(request, response, aid)
    account_info = manager.get_account_info()

    response.set_navlist([
        const.apps.ACCOUNT,
        [manager.account.nickname, 'account.space', (manager.account.id, )],
        ['个人中心']
    ])

    return response.render_page(request, 'account/space/wejudge.tpl', {
        'account_info': account_info,
        'account': manager.account,
        'hide_breadcrumb': True
    })

# === APIS ===

# 个人信息获取
def account_info(request, aid):
    """
    个人信息获取
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeSession(request)   # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = AccountSpaceLib.WeJudgeAccountSpace(request, response, aid)
    result = manager.get_account_info()

    return response.json(WeJudgeResult(result))


# 读取用户的做题信息
def get_user_problem_solutions(request, aid):
    """
    读取用户的做题信息
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeSession(request)   # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = AccountSpaceLib.WeJudgeAccountSpace(request, response, aid)
    result = manager.get_user_problem_solutions()

    return response.json(WeJudgeResult(result))


# 保存用户信息
def save_account_infos(request, aid):
    """
    保存用户信息
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeSession(request)   # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = AccountSpaceLib.WeJudgeAccountSpace(request, response, aid)
    result = manager.save_account_infos()

    return response.json(WeJudgeResult(result))


# 保存用户头像
def save_account_avatar(request, aid):
    """
    保存用户头像
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeSession(request)   # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = AccountSpaceLib.WeJudgeAccountSpace(request, response, aid)
    result = manager.save_account_avatar()

    return response.json(WeJudgeResult(result))


def avator(request, aid):
    """
    头像获取接口
    :param request:
    :param aid: 账户ID
    :return:
    """

    account = AccountSpaceLib.WeJudgeAccountSpace.get_account_static(aid)
    response = AccountSpaceLib.WeJudgeAccountSpace.get_account_avator(account)

    return response
