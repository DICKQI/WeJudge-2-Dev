# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.education.libs as libs
from wejudge.const import system
from django.shortcuts import reverse
from django.http.response import HttpResponseRedirect


# 展示题目内容
def view_problem(request, sid, aid, pid):
    """
    展示题目
    :param request:
    :param aid:　Asgn ID
    :param pid:
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.AsgnProblemController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_problem(pid)

    # 检查访问权限
    manager.login_check()
    manager.check_problem_privilege(privilege_code=1)
    manager.check_assistant()           # 助教提权
    manager.check_asgn_visit()          # 检查作业权限
    manager.get_asgn_solution()         # 创建题目访问记录
    report = manager.get_asgn_report()  # 获取实验报告

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.index'],
        [
            "%s (%s)" % (manager.course.name, manager.course.term),
            'education.course.index',
            (manager.school.id, manager.course.id,)
         ],
        [manager.asgn.title, 'education.asgn.index', (manager.school.id, manager.asgn.id, )],
        ["题目%s：%s" % (manager.asgn_problem_item.index, manager.problem.title)]
    ])

    problem_entity = manager.problem

    return response.render_page(request, 'education/asgn/problem.tpl', context={
        "school": manager.school,
        "asgn": manager.asgn,
        "course": manager.course,
        "asgn_report": report,
        "problem": manager.asgn_problem_item,
        "problem_entity": problem_entity,
        "asgn_id": manager.asgn.id,
        "problem_id": manager.asgn_problem_item.id,
        "is_manager": manager.check_user_privilege(role=2, throw=False),
        "problems_list": manager.asgn.problems.order_by('index'),
        "page_name": "PROBLEM"
    })


# === API ===

# 获取作业题目内容
def get_problem_body(request, sid, aid, pid):
    """
    获取作业题目内容
    :param request:
    :param sid:
    :param aid:
    :param pid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.AsgnProblemController(request, response, sid)
    manager.login_check()
    manager.get_asgn(aid)
    manager.get_problem(pid)
    manager.check_assistant()  # 助教提权

    return response.json(WeJudgeResult(manager.get_problem_body()))


# 提交代码
@WeJudgePOSTRequire
def api_submit_code(request, sid, aid, pid):
    """
    提交代码
    :param request:
    :param aid:
    :param pid:  题目ID
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.AsgnProblemController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_problem(pid)
    manager.check_assistant()  # 助教提权

    # 从Cookie中获取Signature
    _session_raw = request.session.get(system.WEJUDGE_EDU_ACCOUNT_SESSION, {})
    user_signature = request.COOKIES.get(system.WEJUDGE_EDU_ACCOUNT_SESSION_SIGNATURE_KEY, '')
    from wejudge.utils import tools
    if tools.token_hmac_sha512_singature(_session_raw) != user_signature:
        raise WeJudgeError(8)

    status_id = manager.submit_code()

    return response.json(WeJudgeResult({
        "aid": manager.asgn.id,
        "sid": status_id
    }, msg="OK"))


# 轮询评测状态接口
def api_rolling_judge_status(request, sid, aid, status_id):
    """
    轮询评测状态接口
    :param aid:
    :param status_id:
    :param request:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.AsgnProblemController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_status(status_id)

    return response.json(WeJudgeResult({"flag": manager.status.flag}, msg="OK"))


# 获取评测状态
def api_judge_status_list(request, sid, aid, pid):
    """
    获取评测状态
    :param request:
    :param aid:
    :param pid:
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.AsgnProblemController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_problem(pid)
    manager.check_assistant()  # 助教提权

    listdata = manager.get_judge_status()
    return response.json(WeJudgeResult(listdata))
