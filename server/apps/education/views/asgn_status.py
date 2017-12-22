# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.education.libs as libs
from wejudge.const import system
from django.shortcuts import reverse

__author__ = 'lancelrq'

# ==== HTML ====


# 展示评测详情
def judge_status(request, sid, aid, status_id):
    """
    展示评测详情
    :param request:
    :param aid:
    :param status_id:
    :param sid:
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.AsgnJudgeStatusController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_status(status_id)

    # 检查访问权限
    manager.login_check()
    manager.check_assistant()  # 助教提权
    manager.judge_status_privilege()
    report = manager.get_asgn_report()

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.index'],
        [
            "%s (%s)" % (manager.course.name, manager.course.term),
            'education.course.index',
            (manager.school.id, manager.course.id,)
        ],
        [manager.asgn.title, 'education.asgn.index', (manager.school.id, manager.asgn.id,)],
        ["评测详情(ID:%s)" % manager.status.id]
    ])

    problem_entity = manager.problem
    manager.asgn_problem_item = manager.status.virtual_problem

    return response.render_page(request, 'education/asgn/status.tpl', context={
        "school": manager.school,
        "asgn": manager.asgn,
        "asgn_report": report,
        "course": manager.course,
        "problem": manager.asgn_problem_item,
        "problem_entity": problem_entity,
        "asgn_id": manager.asgn.id,
        "status": manager.status,
        "problem_id": manager.asgn_problem_item.id,
        "is_manager": manager.check_user_privilege(role=2, throw=False),
        "page_name": "PROBLEM"
    })


# ==== API ====

# 获取评测详情
def get_judge_detail(request, sid, aid, status_id):
    """
    获取评测详情
    :param request:
    :param aid:
    :param status_id:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.AsgnJudgeStatusController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_status(status_id)
    manager.check_assistant()  # 助教提权

    data = manager.get_judge_detail()

    return response.json(WeJudgeResult(data))


# 读取评测状态信息
def get_judge_status(request, sid, aid, status_id):
    """
    读取评测状态信息
    :param request:
    :param aid:
    :param status_id:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.AsgnJudgeStatusController(request, response, sid)

    manager.get_asgn(aid)
    manager.get_status(status_id)
    manager.check_assistant()  # 助教提权

    data = manager.get_status_body()

    return response.json(WeJudgeResult(data))


# 编辑评测状态
@WeJudgePOSTRequire
def edit_judge_status(request, sid, aid, status_id):
    """
    编辑评测状态
    :param request:
    :param aid:
    :param status_id:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.AsgnJudgeStatusController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_status(status_id)
    manager.check_assistant()           # 助教提权

    data = manager.edit()

    return response.json(WeJudgeResult(data))


# 重判单个评测记录
@WeJudgePOSTRequire
def rejudge_status(request, sid, aid, status_id):
    """
    重判单个评测记录
    :param request:
    :param aid:
    :param status_id:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.AsgnJudgeStatusController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_status(status_id)
    manager.check_assistant()  # 助教提权

    data = manager.rejudge()

    return response.json(WeJudgeResult(data))


# 删除评测状态
@WeJudgePOSTRequire
def delete_judge_status(request, sid, aid, status_id):
    """
    删除评测状态
    :param request:
    :param aid:
    :param status_id:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.AsgnJudgeStatusController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_status(status_id)
    manager.check_assistant()  # 助教提权

    data = manager.delete()

    return response.json(WeJudgeResult(data))

