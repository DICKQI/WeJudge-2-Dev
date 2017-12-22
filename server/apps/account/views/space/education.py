# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
from wejudge.const import system
from apps.account.libs import space as AccountSpaceLib

__author__ = 'lancelrq'


def space(request, sid, aid):
    """
    WeJudge 教学账户 个人中心
    :param request:
    :param aid:
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)                  # 创建会话
    response = WeJudgeResponse(wejudge_session)                         # 创建响应

    manager = AccountSpaceLib.EducationAccountSpace(request, response, sid, aid)
    account_info = manager.get_account_info()

    response.set_navlist([
        const.apps.ACCOUNT,
        [manager.school.name, 'education.school', (manager.school.id,)],
        [manager.account.nickname, 'account.education.space', (manager.school.id, manager.account.id)],
        ['个人中心']
    ])

    return response.render_page(request, 'account/space/education.tpl', {
        'account_info': account_info,
        'account': manager.account,
        'school': manager.school,
        'hide_breadcrumb': True,
        "WJ_EDU_ARC": system.WEJUDGE_EDU_ACCOUNT_ROLES_CALLED
    })


# === APIS ===

# 个人信息获取
def account_info(request, sid, aid):
    """
    个人信息获取
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = AccountSpaceLib.EducationAccountSpace(request, response, sid, aid)
    result = manager.get_account_info()

    return response.json(WeJudgeResult(result))


# 个人信息获取
@WeJudgePOSTRequire
def oauth2_account_info(request, sid, aid=None):
    """
    个人信息获取
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeEducationOauth2Session(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    wejudge_session.set_school_id(sid)
    wejudge_session.load_session()

    if aid is None:
        manager = AccountSpaceLib.EducationAccountSpace(
            request, response, sid, wejudge_session.account.id if wejudge_session.account is not None else 0
        )
    else:
        manager = AccountSpaceLib.EducationAccountSpace(request, response, sid, aid)

    result = manager.get_account_info()

    return response.json(WeJudgeResult(result))


# 读取用户的做题信息
def get_user_problem_solutions(request, sid, aid):
    """
    读取用户的做题信息
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = AccountSpaceLib.EducationAccountSpace(request, response, sid, aid)
    result = manager.get_user_problem_solutions()

    return response.json(WeJudgeResult(result))


# 保存用户信息
def save_account_infos(request, sid, aid):
    """
    保存用户信息
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = AccountSpaceLib.EducationAccountSpace(request, response, sid, aid)
    result = manager.save_account_infos()

    return response.json(WeJudgeResult(result))


# 保存用户头像
def save_account_avatar(request, sid, aid):
    """
    保存用户头像
    :param request:
    :param aid: 账户ID
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = AccountSpaceLib.EducationAccountSpace(request, response, sid, aid)
    result = manager.save_account_avatar()

    return response.json(WeJudgeResult(result))


def avator(request, sid, aid):
    """
    头像获取接口
    :param request:
    :param sid: School Id
    :param aid: 账户ID
    :return:
    """

    account = AccountSpaceLib.EducationAccountSpace.get_account_static(aid, sid)
    response = AccountSpaceLib.EducationAccountSpace.get_account_avator(account)

    return response
