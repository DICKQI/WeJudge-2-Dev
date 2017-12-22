# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
from wejudge.utils import tools
import apps.contest.libs as libs
from wejudge.const import system


# 展示题目内容
def view_problem(request, cid, pid):
    """
    展示题目
    :param request:
    :param cid:　Contest ID
    :param pid:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = libs.ContestProblemController(request, response, cid)
    manager.get_problem(pid)

    # 检查访问权限
    manager.login_check()
    manager.check_timepassed(status__gt=-1, errcode=5003)
    manager.check_problem_privilege(privilege_code=1)

    response.set_navlist([
        const.apps.CONTEST,
        [manager.contest.title, 'contest.contest', (manager.contest.id,)],
        ["题目%s" % tools.gen_problem_index(manager.contest_problem_item.index)]
    ])

    problem_entity = manager.problem

    return response.render_page(request, 'contest/problem.tpl', context={
        "contest": manager.contest,
        "problem": manager.contest_problem_item,
        "problem_entity": problem_entity,
        "contest_id": manager.contest.id,
        "problem_id": manager.contest_problem_item.id,
        "hide_login": True,
        "problems_list": manager.contest.problems.order_by('index')
    })


# === API ===

# 获取比赛题目内容
def get_problem_body(request, cid, pid):
    """
    获取比赛题目内容
    :param request:
    :param cid:
    :param pid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestProblemController(request, response, cid)
    manager.get_problem(pid)

    return response.json(WeJudgeResult(manager.get_problem_body()))


# 提交代码
@WeJudgePOSTRequire
def api_submit_code(request, cid, pid):
    """
    提交代码
    :param request:
    :param cid:
    :param pid:  题目ID
    :return:
    """
    # wejudge_cookie =
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestProblemController(request, response, cid)
    manager.get_problem(pid)

    status_id = manager.submit_code()

    # 从Cookie中获取Signature
    _session_raw = request.session.get(system.WEJUDGE_CONTEST_ACCOUNT_SESSION, {})
    user_signature = request.COOKIES.get(system.WEJUDGE_CONTEST_ACCOUNT_SESSION_SIGNATURE_KEY, '')
    from wejudge.utils import tools
    if tools.token_hmac_sha512_singature(_session_raw) != user_signature:
        raise WeJudgeError(8)

    return response.json(WeJudgeResult({
        "cid": manager.contest.id,
        "sid": status_id
    }, msg="OK"))


# 轮询评测状态接口
def api_rolling_judge_status(request, cid, sid):
    """
    轮询评测状态接口
    :param cid:
    :param sid:
    :param request:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestProblemController(request, response, cid)
    manager.get_status(sid)

    return response.json(WeJudgeResult({"flag": manager.status.flag}, msg="OK"))


# 获取评测状态
def api_judge_status_list(request, cid, pid):
    """
    获取评测状态
    :param request:
    :param cid:
    :param pid:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestProblemController(request, response, cid)
    manager.get_problem(pid)

    listdata = manager.get_judge_status()
    return response.json(WeJudgeResult(listdata))


# 发布题目（内部Hook
def create_problem(request, cid):
    """
    发布题目（内部Hook
    :param request:
    :param cid:
    :return:
    """

    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestProblemManagerController(request, response, cid)
    problem = manager.create_problem()

    return response.json(WeJudgeResult(problem.id, msg="创建题目成功！"))
