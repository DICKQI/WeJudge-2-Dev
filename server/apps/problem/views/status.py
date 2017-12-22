# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.problem.libs as libs
from wejudge.const import system
from django.shortcuts import reverse

__author__ = 'lancelrq'

# ==== HTML ====


# 展示评测详情
def judge_status(request, sid):
    """
    展示评测详情
    :param request:
    :param sid:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)

    manager.login_check()
    manager.get_status(sid)
    manager.judge_status_privilege()

    status = manager.status

    nav_pset = None
    if status.virtual_problem is not None:
        pset = status.virtual_problem.problemset
        if pset is not None:
            nav_pset = [pset.title, "problem.set.view", (int(pset.id),)]

    response.set_navlist([
        const.apps.PROBLEM,
        nav_pset,
        ["评测详情(ID:%s)" % manager.status.id]
    ])

    return response.render_page(request, 'problem/judge/status.tpl', context={
        "status": manager.status
    })


# ==== API ====

# 获取评测详情
def get_judge_detail(request, sid):
    """
    获取评测详情
    :param request:
    :param sid：
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.JudgeStatusController(request, response)

    manager.get_status(sid)
    data = manager.get_judge_detail()

    return response.json(WeJudgeResult(data))


