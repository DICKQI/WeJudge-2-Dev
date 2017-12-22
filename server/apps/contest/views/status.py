# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.contest.libs as libs
from wejudge.const import system
from django.shortcuts import reverse

__author__ = 'lancelrq'

# ==== HTML ====


# 展示评测详情
def judge_status(request, cid, sid):
    """
    展示评测详情
    :param request:
    :param cid:
    :param sid:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContentJudgeStatusController(request, response, cid)

    manager.login_check()
    manager.get_status(sid)
    manager.judge_status_privilege()

    response.set_navlist([
        const.apps.CONTEST,
        [manager.contest.title, 'contest.contest', (manager.contest.id,)],
        ["评测详情(ID:%s)" % manager.status.id]
    ])

    return response.render_page(request, 'contest/status.tpl', context={
        "contest_problem": manager.status.virtual_problem,
        "status": manager.status,
        "contest": manager.contest
    })


# ==== API ====

# 获取评测详情
def get_judge_detail(request, cid, sid):
    """
    获取评测详情
    :param request:
    :param cid:
    :param sid：
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContentJudgeStatusController(request, response, cid)

    manager.get_status(sid)
    data = manager.get_judge_detail()

    return response.json(WeJudgeResult(data))


# 读取评测状态信息
def get_judge_status(request, cid, sid):
    """
    读取评测状态信息
    :param request:
    :param cid:
    :param sid：
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContentJudgeStatusController(request, response, cid)

    manager.get_status(sid)
    data = manager.get_status_body()

    return response.json(WeJudgeResult(data))


# 删除评测状态
@WeJudgePOSTRequire
def delete_judge_status(request, cid, sid):
    """
    删除评测状态
    :param request:
    :param cid:
    :param sid：
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContentJudgeStatusController(request, response, cid)

    manager.get_status(sid)
    data = manager.delete()

    return response.json(WeJudgeResult(data))


# 编辑评测状态
@WeJudgePOSTRequire
def edit_judge_status(request, cid, sid):
    """
    编辑评测状态
    :param request:
    :param cid:
    :param sid：
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContentJudgeStatusController(request, response, cid)

    manager.get_status(sid)
    data = manager.edit()

    return response.json(WeJudgeResult(data))


# 重判单个评测记录
@WeJudgePOSTRequire
def rejudge_status(request, cid, sid):
    """
    重判单个评测记录
    :param request:
    :param cid:
    :param sid：
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContentJudgeStatusController(request, response, cid)

    manager.get_status(sid)
    data = manager.rejudge()

    return response.json(WeJudgeResult(data))


