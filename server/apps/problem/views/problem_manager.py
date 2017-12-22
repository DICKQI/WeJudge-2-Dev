# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.problem.libs as libs
from wejudge.const import system as c_sys
from django.shortcuts import reverse
__author__ = 'lancelrq'

# ==== HTML ====


# 评测设置管理
def judge_manager(request, psid, pid):
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    if int(psid) != 0:
        manager.get_problemset(psid)
    manager.get_problem(pid)

    # 检查管理访问权限（仅仅是看的权限，不一定能修改）
    manager.login_check()
    manager.check_problem_privilege(privilege_code=4)

    pset = manager.problem_set
    problem_entity = manager.problem
    nav_pset = None if int(psid) == 0 else [pset.title, "problem.set.view", (int(pset.id),)]
    nav_problem = [
        "%s：%s" % (problem_entity.id if int(psid) == 0 else manager.problem_set_item.id, problem_entity.title),
        "problem.view",
        (0, problem_entity.id,) if int(psid) == 0 else (int(pset.id), manager.problem_set_item.id,)
    ]

    response.set_navlist([
        const.apps.PROBLEM,
        nav_pset,
        nav_problem,
        ["评测设置管理"]
    ])

    return response.render_page(request, 'problem/entity/manager/judge.tpl', context={
        "problemset": pset,
        "problem": manager.problem_set_item,
        "problem_entity": problem_entity,
        "pset_id": 0 if pset is None else pset.id,
        "problem_id": problem_entity.id if pset is None else manager.problem_set_item.id,
        "page_name": "JUDGE"
    })


# 题目编辑
def problem_editor(request, psid, pid):
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    if int(psid) != 0:
        manager.get_problemset(psid)
    manager.get_problem(pid)

    # 检查管理访问权限（仅仅是看的权限，不一定能修改）
    manager.login_check()
    manager.check_problem_privilege(privilege_code=4)

    pset = manager.problem_set
    problem_entity = manager.problem
    nav_pset = None if int(psid) == 0 else [pset.title, "problem.set.view", (int(pset.id),)]
    nav_problem = [
        "%s：%s" % (problem_entity.id if int(psid) == 0 else manager.problem_set_item.id, problem_entity.title),
        "problem.view",
        (0, problem_entity.id,) if int(psid) == 0 else (int(pset.id), manager.problem_set_item.id,)
    ]

    response.set_navlist([
        const.apps.PROBLEM,
        nav_pset,
        nav_problem,
        ["编辑题目内容"]
    ])

    return response.render_page(request, 'problem/entity/manager/editor.tpl', context={
        "problemset": pset,
        "problem": manager.problem_set_item,
        "problem_entity": problem_entity,
        "pset_id": 0 if pset is None else pset.id,
        "problem_id": problem_entity.id if pset is None else manager.problem_set_item.id,
        "page_name": "EDITOR"
    })


# 题目集关联管理
def problemset_relation(request, psid, pid):
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemBodyController(request, response)
    if int(psid) != 0:
        manager.get_problemset(psid)
    manager.get_problem(pid)

    # 检查管理访问权限（仅仅是看的权限，不一定能修改）
    manager.login_check()
    manager.check_problem_privilege(privilege_code=4)

    pset = manager.problem_set
    problem_entity = manager.problem
    nav_pset = None if int(psid) == 0 else [pset.title, "problem.set.view", (int(pset.id),)]
    nav_problem = [
        "%s：%s" % (problem_entity.id if int(psid) == 0 else manager.problem_set_item.id, problem_entity.title),
        "problem.view",
        (0, problem_entity.id,) if int(psid) == 0 else (int(pset.id), manager.problem_set_item.id,)
    ]

    response.set_navlist([
        const.apps.PROBLEM,
        nav_pset,
        nav_problem,
        ["题目集关联管理"]
    ])

    return response.render_page(request, 'problem/entity/manager/problemset.tpl', context={
        "problemset": pset,
        "problem": manager.problem_set_item,
        "problem_entity": problem_entity,
        "pset_id": 0 if pset is None else pset.id,
        "problem_id": problem_entity.id if pset is None else manager.problem_set_item.id,
        "page_name": "PROBLEMSET"
    })


# ==== API ====


# 发布新题目
@WeJudgePOSTRequire
def create_problem(request, psid):
    """
    发布新题目
    :param request:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)
    manager.get_problemset(psid) if int(psid) > 0 else ""

    problem = manager.create_problem()

    return response.json(WeJudgeResult(problem.id, msg="创建题目成功！点击确定进入评测设置的页面"))


# 编辑题目
@WeJudgePOSTRequire
def modify_problem(request, pid, psid):
    """
    编辑题目
    :param request:
    :param pid
    :param psid
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)
    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    problem = manager.modify_problem()

    return response.json(WeJudgeResult(problem.id, msg="修改题目成功！"))


# 获取判题设置信息
def get_judge_config(request, pid, psid):
    """
    获取判题设置信息
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    test_cases = manager.get_judge_config()

    return response.json(WeJudgeResult(test_cases))


# 获取题目对于题目集合的关联
def get_problemset_relations(request, pid, psid):
    """
    获取题目对于题目集合的关联
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.get_problemset_relations()

    return response.json(WeJudgeResult(result))


# 获取题目对于题目集合的关联(注意传值)
def publish_to_problemset(request, pid, psid):
    """
    获取题目对于题目集合的关联
    :param request:
    :param pid:  Problem Entity ID
    :param psid: Problemset ID
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problem(pid)
    manager.get_problemset(psid) if int(psid) > 0 else ""

    result = manager.publish_to_problemset()

    return response.json(WeJudgeResult(result))


# 从题库中移除题目
def remove_from_problemset(request, pid, psid):
    """
    从题库中移除题目
    :param request:
    :param pid:  Problem Entity ID
    :param psid: Problemset ID
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problem(pid)
    manager.get_problemset(psid) if int(psid) > 0 else ""

    result = manager.remove_from_problemset()

    return response.json(WeJudgeResult(result))


# 保存评测设置
def save_judge_config(request, pid, psid):
    """
    保存评测设置
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    test_cases = manager.save_judge_config()

    return response.json(WeJudgeResult(test_cases))


# 评测开关
def toggle_judge(request, pid, psid):
    """
    评测开关
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    test_cases = manager.toggle_judge()

    return response.json(WeJudgeResult(test_cases))


# 保存特殊评测的程序代码
def save_specical_judge_program(request, pid, psid):
    """
    保存特殊评测的程序代码
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result, msg = manager.save_specical_judge_program()

    return response.json(WeJudgeResult(result, msg="编译错误：%s" % msg if msg != "" else "编译成功！"))


# 保存示例代码
def save_answer_case(request, pid, psid):
    """
    保存示例代码
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.save_answer_case()

    return response.json(WeJudgeResult(result))


# 保存测试数据设置
def save_test_cases_settings(request, pid, psid):
    """
    保存测试数据设置
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.save_test_cases_settings()

    return response.json(WeJudgeResult(result))


# 删除测试数据
def remove_test_cases(request, pid, psid):
    """
    删除测试数据
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.remove_test_cases()

    return response.json(WeJudgeResult(result))


# 获取测试数据的内容
def get_test_cases_content(request, pid, psid):
    """
    获取测试数据的内容
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.get_test_cases_content()

    return response.json(WeJudgeResult(result))


# 保存测试数据的内容
def save_test_cases_content(request, pid, psid):
    """
    保存测试数据的内容
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.save_test_cases_content()

    return response.json(WeJudgeResult(result))


# 保存上传的测试数据的内容
def upload_test_cases_content(request, pid, psid, type):
    """
    保存上传的测试数据的内容
    :param request:
    :param pid:
    :param psid:
    :param type:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.upload_test_cases_content(type)

    return response.json(WeJudgeResult(result))


# 使用测试数据生成器生成目标输出结果
def tcmaker_run(request, pid, psid):
    """
    使用测试数据生成器生成目标输出结果
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.tcmaker_run()

    return response.json(WeJudgeResult(data=result, msg="创建队列成功！异步操作有一定的延时，请在【操作历史】查看执行结果。"))


# 使用测试数据生成器生成目标输出结果
def get_tcmaker_status(request, pid, psid):
    """
    使用测试数据生成器生成目标输出结果
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.get_tcmaker_status()

    return response.json(WeJudgeResult(data=result))


# 使用测试数据生成器生成目标输出结果
def tcmaker_callback(request, pid, tcsid):
    """
    使用测试数据生成器生成目标输出结果
    :param request:
    :param pid:
    :param tcsid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problem(pid)

    result = manager.tcmaker_callback(tcsid)

    return response.text(result)


# 保存填空示例代码
def save_demo_cases_code(request, pid, psid):
    """
    保存填空示例代码
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.save_demo_cases_code()

    return response.json(WeJudgeResult(result))


# 保存填空用例设置
def save_demo_cases_settings(request, pid, psid):
    """
    保存填空用例设置
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.save_demo_cases_settings()

    return response.json(WeJudgeResult(result))


# 删除填空用例设置
def remove_demo_cases(request, pid, psid):
    """
    删除填空用例设置
    :param request:
    :param pid:
    :param psid:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ProblemManagerController(request, response)

    manager.get_problemset(psid) if int(psid) > 0 else ""
    manager.get_problem(pid)

    result = manager.remove_demo_cases()

    return response.json(WeJudgeResult(result))
