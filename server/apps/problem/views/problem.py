# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.problem.libs as libs
from wejudge.const import system as c_sys
from django.shortcuts import reverse
from django.views.decorators.cache import cache_page

__author__ = 'lancelrq'

# ==== HTML ====


# 展示题目内容
def view(request, psid, pid):
    """
    展示题目
    :param request:
    :param psid:
    :param pid:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    if int(psid) != 0:
        manager.get_problemset(psid)
    manager.get_problem(pid)
    manager.check_problemset_privilege()

    # # # #我也不知道我以前干嘛要写这个东西难道是因为YQQ的原因？然而实际上我的权限系统已经设置的非常非常牛逼了啊...
    # # 私人访问时（也就是通过真实题号），如果不是本人，则提示题目不存在。这是保护策略。
    # if int(psid) == 0:
    #     if manager.problem.author_id != wejudge_session.account.id:
    #         raise WeJudgeError(2001)

    # 检查访问权限
    # manager.login_check()
    manager.check_problem_privilege(privilege_code=1)

    pset = manager.problem_set

    nav_pset = None if int(psid) == 0 else [pset.title, "problem.set.view", (int(pset.id),)]

    problem_entity = manager.problem

    response.set_navlist([
        const.apps.PROBLEM,
        nav_pset,
        ["题目%s：%s" % (problem_entity.id if int(psid) == 0 else manager.problem_set_item.id, problem_entity.title)]
    ])

    return response.render_page(request, 'problem/entity/problem.tpl', context={
        "problemset": pset,
        "problem": manager.problem_set_item,
        "problem_entity": problem_entity,
        "pset_id": 0 if pset is None else pset.id,
        "problem_id": problem_entity.id if pset is None else manager.problem_set_item.id,
        "flag_description": json.dumps(c_sys.WEJUDGE_JUDGE_STATUS_DESC),
        "show_manager_link": (wejudge_session.is_logined() and wejudge_session.account.permission_publish_problem)
    })


# ==== API ====

# 获取题目内容
def api_get_body(request, psid, pid):
    """
    获取题目内容
    :param request:
    :param psid: 题目集合ID
    :param pid:  题目ID
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    if int(psid) != 0:
        manager.get_problemset(psid)
    manager.get_problem(pid)

    return response.json(WeJudgeResult(manager.get_problem_body()))


# 提交代码
@WeJudgePOSTRequire
def api_submit_code(request, psid, pid):
    """
    提交代码
    :param request:
    :param psid: 题目集合ID
    :param pid:  题目ID
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    if int(psid) != 0:
        manager.get_problemset(psid)
    manager.get_problem(pid)

    status_id = manager.submit_code()

    return response.json(WeJudgeResult({
        "sid": status_id
    }, msg="OK"))


# 轮询评测状态接口
def api_rolling_judge_status(request, sid):
    """
    轮询评测状态接口
    :param request:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)

    manager.get_status(sid)

    return response.json(WeJudgeResult({"flag": manager.status.flag}, msg="OK"))


# 获取当前题目当前单个人的评测状态信息
def api_judge_status_list(request, psid, pid):
    """
    获取当前题目当前单个人的评测状态信息
    :param request:
    :param psid:    Pset ID
    :param pid
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    if int(psid) != 0:
        manager.get_problemset(psid)
    manager.get_problem(pid)

    listdata = manager.get_judge_status()

    return response.json(WeJudgeResult(listdata))


# 代码格式化
def api_code_indent(request):
    """
    代码格式化
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)       # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = libs.ProblemBodyController(request, response)
    result = manager.code_indent()
    
    return response.json(WeJudgeResult(result))


# 获取题目分析统计信息
def api_get_statistics(request, pid):
    """
    获取题目分析统计信息
    :param request:
    :param pid
    :return:
    """

    wejudge_session = WeJudgeSession(request)       # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = libs.ProblemBodyController(request, response)
    manager.get_problem(pid)

    result = manager.get_statistics()

    return JsonResponse(WeJudgeResult(result).to_dict())


# 获取当前用户的草稿代码
def get_code_drafts(request, pid):
    """
    获取当前用户的草稿代码
    :param request:
    :param pid:  题目ID
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    manager.get_problem(pid)

    result = manager.get_code_drafts()

    return response.json(WeJudgeResult(result))


# 保存当前用户的草稿代码
@WeJudgePOSTRequire
def save_code_draft(request, pid):
    """
    保存当前用户的草稿代码
    :param request:
    :param pid:  题目ID
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    manager.get_problem(pid)

    result = manager.save_code_draft()

    return response.json(WeJudgeResult(result, msg="草稿代码保存成功"))