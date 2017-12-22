# *- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
import apps.contest.libs as libs
from wejudge.const import system
from django.shortcuts import reverse
from django.http.response import HttpResponseRedirect
from django.template import Context, Template
from django.db import transaction

__author__ = 'lancelrq'


# 比赛系统首页
def index(request):
    """
    比赛系统首页
    :param request:
    :return:
    """
    wejudge_session = WeJudgeSession(request)                       # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    response.set_navlist([
        const.apps.CONTEST
    ])

    return response.render_page(request, 'contest/index.tpl', {

    })


# 比赛展示页面
def contest(request, cid):
    """
    比赛系统首页
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.ContestController(request, response, cid)

    response.set_navlist([
        const.apps.CONTEST,
        [manager.contest.title]
    ])

    if wejudge_session.is_logined():
        if wejudge_session.account.password == '1e77c00131d49d6518d7eba2f8ebe70ada7a1ac9d8e8fe7f3bd07f9d9ab635ca':
            return response.render_page(request, 'contest/init.tpl', {
                "contest": manager.contest,
                "page_name": "INDEX",
                "hide_login": False,
                "hide_breadcrumb": True
            })

    storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CONTEST_STORAGE, str(manager.contest.id))
    if storage.exists("intro.html"):
        fp = storage.open_file("intro.html", 'r')
        index_view = fp.read()
        fp.close()
        t = Template(index_view)
        index_view = t.render(Context({
            "contest": manager.contest,
            "wejudge_session": manager.session
        }))
    else:
        index_view = "<h2>欢迎参加本次比赛</h2><div class='ui divider'></div><h4>比赛主办者很懒，居然连介绍都没有写... ┑(￣Д ￣)┍</h4>"
    #
    # from django.utils.timezone import now
    #
    # time_delta = 0
    # if manager.contest.start_time < now():
    #     try:
    #         time_delta = (manager.contest.end_time - now()).total_seconds()
    #     except:
    #         time_delta = 0
    #
    #     if time_delta >= 360000:
    #         time_delta = 0
    return response.render_page(request, 'contest/contest.tpl', {
        "contest": manager.contest,
        "index_view": index_view,
        "page_name": "INDEX",
        "hide_login": False,
        "hide_breadcrumb": True
    })


# 比赛管理页面
def contest_management(request, cid):
    """
    比赛管理页面
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.ContestController(request, response, cid)
    manager.check_privilege(1)  # 检查管理权限

    response.set_navlist([
        const.apps.CONTEST,
        [manager.contest.title]
    ])

    return response.render_page(request, 'contest/manager.tpl', {
        "contest": manager.contest,
        "page_name": "MANAGE",
    })


# 比赛滚榜页面
def rankboard(request, cid):
    """
    比赛滚榜页面
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.ContestController(request, response, cid)

    return response.render_page(request, 'contest/board.tpl', {
        "contest": manager.contest,
    })


# 生成打印预览
def printer_view(request, cid, pid):
    """
    生成打印预览
    :param request:
    :param cid:
    :param pid: page ID
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.ContestController(request, response, cid)

    return response.render_page(request, 'contest/printer.tpl', {
        "contest": manager.contest,
        "printer_item": manager.get_printer_queue_item(pid)
    })


# === API ===
# 获取比赛列表
def get_contest_list(request):
    """
    获取比赛列表
    :param request:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    contest_list = libs.ContestController.get_contest_list(request)

    return response.json(WeJudgeResult(contest_list))


# 创建比赛
def create_contest(request):
    """
    创建比赛
    :param request:
    :return:
    """
    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    if not wejudge_session.is_logined():
        raise WeJudgeError(1010)

    account = wejudge_session.account
    if not account.permission_create_contest:
        raise WeJudgeError(5999)

    contest_list = libs.ContestController.create_contest(request, wejudge_session.account)

    return response.json(WeJudgeResult(data=contest_list, msg="比赛创建成功！初始账户为admin，密码为您当前账户的密码！"))


# 获取比赛题目列表
def get_problems_list(request, cid):
    """
    获取比赛题目列表
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)
    result = manager.get_contest_problems()

    return response.json(WeJudgeResult(result))


# 获取比赛评测详情
def get_judge_status(request, cid):
    """
    获取比赛评测详情
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)
    result = manager.get_judge_status()

    return response.json(WeJudgeResult(result))


# 保存题目的设置信息
def save_contest_problem_setting(request, cid, pid):
    """
    保存题目的设置信息
    :param request:
    :param cid:
    :param pid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)
    manager.get_problem(pid)

    result = manager.save_contest_problem_setting()

    return response.json(WeJudgeResult(result))


# 删除题目引用
@WeJudgePOSTRequire
def remove_contest_problem(request, cid, pid):
    """
    删除题目引用
    :param request:
    :param cid:
    :param pid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)
    manager.get_problem(pid)

    result = manager.remove_contest_problem()

    return response.json(WeJudgeResult(result))


# 添加题目引用
@WeJudgePOSTRequire
def add_contest_problem(request, cid):
    """
    添加题目引用
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.add_contest_problem()

    return response.json(WeJudgeResult(result))


# 重判
@WeJudgePOSTRequire
def rejudge_contest_problem(request, cid, pid):
    """
    重判
    :param request:
    :param cid:
    :param pid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)
    manager.get_problem(pid)

    result = manager.rejudge_contest_problem()

    return response.json(WeJudgeResult(result))


# 比赛排行信息获取
def get_ranklist(request, cid):
    """
    比赛排行信息获取
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_ranklist()

    return response.json(WeJudgeResult(result))


# 比赛设置信息获取
def get_contest_settings(request, cid):
    """
    比赛设置信息获取
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_contest_settings()

    return response.json(WeJudgeResult(result))


# 比赛设置信息保存
def save_contest_settings(request, cid):
    """
    比赛设置信息保存
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.save_contest_settings()

    return response.json(WeJudgeResult(result))


# 获取FAQ列表
def get_faq_list(request, cid):
    """
    获取FAQ列表
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_faq_list()

    return response.json(WeJudgeResult(result))


# 回复FAQ
def reply_faq(request, cid):
    """
    回复FAQ
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.reply_faq()

    return response.json(WeJudgeResult(result))


# 新建FAQ
def new_faq(request, cid):
    """
    新建FAQ
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.new_faq()

    return response.json(WeJudgeResult(result))


# 设置FAQ为公开或者私密
def toggle_faq(request, cid):
    """
    设置FAQ为公开或者私密
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.change_faq_visable()

    return response.json(WeJudgeResult(result))


# 删除FAQ
def delete_faq(request, cid):
    """
    删除FAQ
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.delete_faq()

    return response.json(WeJudgeResult(result))


# 比赛公告
def get_notice_list(request, cid):
    """
    新建FAQ
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_notice_list()

    return response.json(WeJudgeResult(result))


# 新建公告（不支持编辑！发错了自己删）
def new_notice(request, cid):
    """
    设置FAQ为公开或者私密
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.new_notice()

    return response.json(WeJudgeResult(result))


# 删除公告
def delete_notice(request, cid):
    """
    删除公告
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.delete_notice()

    return response.json(WeJudgeResult(result))


# 获取比赛账户表
def get_account_list(request, cid):
    """
    获取比赛账户表
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_account_list()

    return response.json(WeJudgeResult(result))


# 新增或编辑用户信息
def edit_account(request, cid):
    """
    新增或编辑用户信息
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.edit_account()

    return response.json(WeJudgeResult(result))


# 从xls导入账户信息
@WeJudgePOSTRequire
def xls_import_account(request, cid):
    """
    从xls导入账户信息
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)        # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.xls_import_account()

    return response.json(WeJudgeResult(result))


# 删除用户
@WeJudgePOSTRequire
def delete_account(request, cid):
    """
    删除用户
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.delete_account()

    return response.json(WeJudgeResult(result))


# 获取实时查重信息
def get_cross_check_list(request, cid):
    """
    获取实时查重信息
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_cross_check_list()

    return response.json(WeJudgeResult(result))


# 删除查重信息
def delete_cross_check_record(request, cid):
    """
    删除查重信息
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.delete_cross_check_record()

    return response.json(WeJudgeResult(result))


# 查看查重代码对比
def read_cross_check_code(request, cid):
    """
    查看查重代码对比
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.read_cross_check_code()

    return response.json(WeJudgeResult(result))


# 确认最终排名
def confirm_finally_rank(request, cid):
    """
    确认最终排名
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.confirm_finally_rank()

    return response.json(WeJudgeResult(result))


# 更新比赛服数据
def refresh_contest_data(request, cid):
    """
    更新比赛服数据
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.refresh_contest_data()

    return response.json(WeJudgeResult(result))



# (Access)获取当前的SolutionList
def access_solution_list(request, cid):
    """
    (Access)获取当前的SolutionList
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.access_solution_list()

    return response.json(WeJudgeResult(result))


# (Access)获取比赛的题目列表
def access_contest_problems(request, cid):
    """
    (Access)获取比赛的题目列表
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.access_contest_problems()

    return response.json(WeJudgeResult(result))


# (Access)获取比赛的账户列表
def access_contest_accounts(request, cid):
    """
    (Access)获取比赛的账户列表
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.access_contest_accounts()

    return response.json(WeJudgeResult(result))


# 获取比赛的滚榜信息
def get_rank_board_datas(request, cid):
    """
    获取比赛的滚榜信息
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_rank_board_datas()

    return response.json(WeJudgeResult(result))


# 发送打印资料请求
def send_printer(request, cid):
    """
    发送打印资料请求
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.send_printer()

    return response.json(WeJudgeResult(result))


# 获取打印资料请求列表
def get_printer_queue(request, cid):
    """
    获取打印资料请求列表
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.get_printer_queue()

    return response.json(WeJudgeResult(result))


# 删除打印请求
def delete_printer_queue_item(request, cid):
    """
    删除打印请求
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.delete_printer_queue_item()

    return response.json(WeJudgeResult(result))


# 保存比赛选题
def save_problem_choosing(request, cid):
    """
    保存比赛选题
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)    # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.save_problem_choosing()

    return response.json(WeJudgeResult(result))


# 注册报名功能
def user_register(request, cid):
    """
    注册报名功能
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.user_register()

    return response.json(WeJudgeResult(result))


# 用户更改密码
def user_changepwd(request, cid):
    """
    用户更改密码
    :param request:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeContestSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.ContestController(request, response, cid)

    result = manager.user_changepwd()

    return HttpResponseRedirect(reverse("contest.contest", args=[manager.contest.id, ]))