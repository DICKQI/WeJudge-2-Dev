# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.problem.libs as libs
from wejudge.const import system as c_sys
import json
__author__ = 'lancelrq'

# ==== HTML ====


# 题目集列表
def view_list(request):
    """
    题目集列表
    :param request:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    response.set_navlist([
        const.apps.PROBLEM,
    ])

    return response.render_page(request, 'problem/set/list.tpl', context={
        "listdata": manager.get_problemset_list(),
    })


# 展示题目集的页面
def view_problemset(request, psid):
    """
    展示题目集的页面
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    pset = manager.problem_set
    manager.check_problemset_privilege()

    response.set_navlist([
        const.apps.PROBLEM,
        [pset.title]
    ])

    return response.render_page(request, 'problem/set/entity.tpl', context={
        "problemset": pset,
        "pset_id": 0 if pset is None else pset.id,
        "problemset_management": wejudge_session.is_logined() and (wejudge_session.account == pset.manager or wejudge_session.account.permission_administrator)
    })


# 发布题目
def publish_problem(request, psid):
    """
    发布题目
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    if not wejudge_session.account.permission_publish_problem:
        raise WeJudgeError(2200)

    manager = libs.ProblemSetController(request, response)
    if int(psid) > 0:
        manager.get_problemset(psid)
        pset = manager.problem_set
        pmgr = manager.check_problemset_manager_privilege(False)
        if not pmgr and pset.publish_private:
            raise WeJudgeError(2107)
        nav_pset = [pset.title, "problem.set.view", (int(pset.id),)]
    else:
        pset = None
        nav_pset = None
        pmgr = False

    response.set_navlist([
        const.apps.PROBLEM,
        nav_pset,
        ['发布题目']
    ])

    return response.render_page(request, 'problem/set/publish_problem.tpl', context={
        "problemset": pset,
        "pset_id": 0 if pset is None else pset.id,
        "pset_mgr_privilege": pmgr
    })


# ==== APIS ====


# 题目集列表数据
def api_list_data(request):
    """
    题目集列表数据
    :param request:
    :return:
    """
    wejudge_session = WeJudgeSession(request)       # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    manager = libs.ProblemSetController(request, response)
    listdata = manager.get_problemset_list()

    return response.json(WeJudgeResult(listdata))


# 题目集的题目列表
def api_problems_list_data(request, psid):
    """
    题目集的题目列表
    :param request:
    :param psid
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)

    listdata = manager.get_problems_list()

    return response.json(WeJudgeResult(listdata))


# 返回当前登录用户发布的题目
def api_problems_list_by_logined_user(request):
    """
    返回当前登录用户发布的题目
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)

    listdata = manager.get_problems_by_logined_user()

    return response.json(WeJudgeResult(listdata))


# 获取评测状态
def api_judge_status_list(request, psid):
    """
    获取评测状态
    :param request:
    :param psid:    Pset ID
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)

    listdata = manager.get_judge_status()
    return response.json(WeJudgeResult(listdata))


# 获取题目集信息
def api_get_problemset_info(request, psid):
    """
    获取题目集信息
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    result = manager.problem_set.json(items=[
        "title", "description", "image", "manager",
        "manager__nickname", "manager__id", 'private', 'publish_private'
    ])

    return response.json(WeJudgeResult(result))


# 移动题目到指定的分类（批量处理）
def problem_moveto_classify(request, psid, cid):
    """
    移动题目到指定的分类（批量处理）
    :param request:
    :param psid:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    manager.get_classify(cid)
    result = manager.problem_moveto_classify()

    return response.json(WeJudgeResult(result))


# 推送题目到指定的题目集（批处理，权限已内部控制）
def problem_moveto_problemset(request, psid):
    """
    推送题目到指定的题目集（批处理，权限已内部控制）
    :param request:
    :param psid:

    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    result = manager.problem_moveto_problemset()

    return response.json(WeJudgeResult(result))


# 从题库中批量移除题目（批量处理）
def problem_removefrom_problemset(request, psid):
    """
    从题库中批量移除题目（批量处理）
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    result = manager.problem_removefrom_problemset()

    return response.json(WeJudgeResult(result))




# -> manager <-

# 创建题目集
@WeJudgePOSTRequire
def api_mgr_create_problemset(request):
    """
    创建题目集
    :param request:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    result = manager.create_problemset()

    # 调用成功则返回新的题目集的ID
    return response.json(WeJudgeResult(result, msg="题目集创建成功！"))


# 编辑题目集
@WeJudgePOSTRequire
def api_mgr_modify_problemset(request, psid):
    """
    编辑题目集
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    result = manager.modify_problemset()

    # 调用成功则返回新的题目集的ID
    return response.json(WeJudgeResult(result, msg="题目集信息修改成功！"))


# 上传题目集照片
@WeJudgePOSTRequire
def api_mgr_upload_problemset_image(request, psid):
    """
    上传题目集照片
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    result = manager.change_problemset_image()

    # 调用成功则返回新的题目集的ID
    return response.json(WeJudgeResult(result, msg="上传成功！"))


# 从题库中移除题目
@WeJudgePOSTRequire
def api_remove_from_problemset(request, psid, pid):
    """
    从题库中移除题目
    :param request:
    :param psid:
    :param pid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    manager.get_problem(pid)
    result = manager.remove_from_problemset()

    return response.json(WeJudgeResult(result))

# === 分类系统


# 获取分类信息
def get_classify_list(request, psid):
    """
    获取分类信息
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    result = manager.get_classify_list()

    return response.json(result)


# 获取分类信息(WEJUDGE_RESULT)
def get_classify_list_wejudge(request, psid):
    """
    获取分类信息
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    result = manager.get_classify_list()

    return response.json(WeJudgeResult(result))


# 移动题目到指定的分类（批量处理）
def change_classify(request, psid, cid):
    """
    移动题目到指定的分类（批量处理）
    :param request:
    :param psid:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemSetController(request, response)
    manager.get_problemset(psid)
    manager.get_classify(cid)
    result = manager.change_classify()

    return response.json(WeJudgeResult(result))

