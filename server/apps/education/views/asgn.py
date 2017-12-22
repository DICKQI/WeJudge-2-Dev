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


# 作业首页
def asgn_index(request, sid, aid):
    """
    作业首页
    :param request:
    :param sid:
    :param aid: aid
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    manager.login_check()                           # 登录检查
    manager.check_assistant()                       # 助教提权
    flag, dec = manager.check_asgn_visit()          # 作业访问权限检查
    report = manager.get_asgn_report()              # 获取/创建实验报告

    arrangements = [arr.json(items=[
        'id', 'name', 'day_of_week', 'start_week', 'end_week', 'odd_even', 'start_section',
        'end_section', 'start_time', 'end_time'
    ]) for arr in manager.course.arrangements.all()]

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term), 'education.course.index',
         (manager.school.id, manager.course.id, )],
        ["在线作业：%s" % manager.asgn.title]
    ])
    return response.render_page(request, 'education/asgn/index.tpl', {
        "course": manager.course,
        "asgn": manager.asgn,
        "school": manager.school,
        "arrangements": json.dumps(arrangements),
        "asgn_vstatus": flag,
        "asgn_vdec": int(dec),
        "asgn_report": report,
        "page_name": "INDEX",
        "hide_breadcrumb": True
    })


# 实验报告
def asgn_report(request, sid, aid, rid=None):
    """
    实验报告
    :param request:
    :param sid:
    :param aid: aid
    :param rid: rid
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    manager.login_check()                           # 登录检查
    manager.check_assistant()                       # 助教提权
    flag, dec = manager.check_asgn_visit()          # 作业访问权限检查
    report = manager.get_asgn_report(rid)           # 获取实验报告

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term), 'education.course.index',
         (manager.school.id, manager.course.id, )],
        ["在线作业：%s" % manager.asgn.title, 'education.asgn.index', (manager.school.id, manager.asgn.id)],
        ["%s的实验报告" % report.author.realname]
    ])
    return response.render_page(request, 'education/asgn/report.tpl', {
        "course": manager.course,
        "asgn": manager.asgn,
        "school": manager.school,
        "asgn_vstatus": flag,
        "asgn_vdec": int(dec),
        "asgn_report": report,
        "page_name": "REPORT"
    })


# 作业管理
def asgn_manager(request, sid, aid):
    """
    作业管理
    :param request:
    :param sid
    :param aid: aid
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    # 检查访问权限
    manager.login_check()

    if not wejudge_session.is_master_logined():
        if wejudge_session.account.master is not None:
            # 如果主账户没有登录，则挂起登录
            from apps.account.libs import session
            session.WeJudgeAccountSessionManager(request, response).login_by_system(wejudge_session.account.master)

    manager.check_assistant()           # 助教提权

    flag, msg = manager.check_asgn_visit()

    if flag != 2:
        raise WeJudgeError(3120)

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term), 'education.course.index',
         (manager.school.id, manager.course.id, )],
        ["在线作业：%s" % manager.asgn.title, 'education.asgn.index', (manager.school.id, manager.asgn.id)],
        ["作业管理"]
    ])

    arrangements = json.dumps(manager.get_asgn_arrangements())

    return response.render_page(request, 'education/asgn/manager.tpl', {
        "course": manager.course,
        "asgn": manager.asgn,
        "school": manager.school,
        "asgn_vstatus": flag,
        "asgn_vmsg": msg,
        "page_name": "MANAGER",
        "arrangements": arrangements
    })


# 作业管理
def asgn_statistic(request, sid, aid):
    """
    作业管理
    :param request:
    :param sid
    :param aid: aid
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    # 检查访问权限
    manager.login_check()
    manager.check_assistant()           # 助教提权
    flag, msg = manager.check_asgn_visit()

    if flag != 2:
        raise WeJudgeError(3120)

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term), 'education.course.index',
         (manager.school.id, manager.course.id, )],
        ["在线作业：%s" % manager.asgn.title, 'education.asgn.index', (manager.school.id, manager.asgn.id)],
        ["统计与分析"]
    ])

    return response.render_page(request, 'education/asgn/statistic.tpl', {
        "course": manager.course,
        "asgn": manager.asgn,
        "school": manager.school,
        "asgn_vstatus": flag,
        "asgn_vmsg": msg,
        "page_name": "STATISTIC",
    })


# 作业滚动排行榜
def asgn_rank_board(request, sid, aid):
    """
    作业滚动排行榜
    :param request:
    :param sid:
    :param aid: aid
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    # 检查访问权限
    manager.login_check()
    manager.check_assistant()                       # 助教提权

    flag, msg = manager.check_asgn_visit()
    if flag < 1:
        raise WeJudgeError(3120)

    return response.render_page(request, 'education/asgn/board.tpl', {
        "course": manager.course,
        "asgn": manager.asgn,
        "school": manager.school,
    })



# === API ===


# 作业题目列表接口
def asgn_problems_list(request, sid, aid):
    """
    作业题目列表接口
    :param request:
    :param aid: asgn id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_asgn_problems()

    return response.json(WeJudgeResult(result))


# 获取整个作业评测状态
def asgn_judge_status_list(request, sid, aid):
    """
    获取整个作业评测状态
    :param request:
    :param aid:   Asgn ID
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    listdata = manager.get_judge_status()

    return response.json(WeJudgeResult(listdata))


# 作业题目列表接口
def get_asgn_report(request, sid, aid, rid=None):
    """
    作业题目列表接口
    :param request:
    :param sid:
    :param aid: asgn id
    :param rid: report id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_asgn_report_detail(rid)

    return response.json(WeJudgeResult(result))


# 保存实验感想
def save_asgn_report_impression(request, sid, aid):
    """
    作业题目列表接口
    :param request:
    :param aid: asgn id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.save_asgn_report_impression()

    return response.json(WeJudgeResult(result))


# 实验报告上传附件
def upload_asgn_report_attchment(request, sid, aid):
    """
    实验报告上传附件
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    result = manager.upload_asgn_report_attchment()

    return response.json(WeJudgeResult(result, msg="刷新页面后查看"))


# 下载实验报告的附件
def download_asgn_report_attchment(request, sid, aid, rid):
    """
    下载实验报告的附件
    :param request:
    :param aid: asgn id
    :param sid: school id
    :param rid: report id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    response = manager.download_asgn_report_attchment(rid)

    return response


# 作业排行榜列表接口
def asgn_rank_list(request, sid, aid):
    """
    作业排行榜列表接口
    :param request:
    :param aid: asgn id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_ranklist()

    return response.json(WeJudgeResult(result))


# 获取滚榜数据接口
def get_rank_board_datas(request, sid, aid):
    """
    获取滚榜数据接口
    :param request:
    :param aid: asgn id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_rank_board_datas()

    return response.json(WeJudgeResult(result))


# 保存作业题目设置
def save_asgn_problem_setting(request, sid, aid, pid):
    """
    保存作业题目设置
    :param request:
    :param aid: asgn id
    :param pid: aproblem id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_problem(pid)
    manager.check_assistant()

    result = manager.save_asgn_problem_setting()

    return response.json(WeJudgeResult(result))


# 移除作业题目关联
def remove_asgn_problem(request, sid, aid, pid):
    """
    移除作业题目关联
    :param request:
    :param sid:
    :param aid: asgn id
    :param pid: aproblem id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_problem(pid)
    manager.check_assistant()

    result = manager.remove_asgn_problem()

    return response.json(WeJudgeResult(result))


# 获取作业设置信息
def get_asgn_settings(request, sid, aid):
    """
    获取作业设置信息
    :param request:
    :param aid: asgn id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_asgn_settings()

    return response.json(WeJudgeResult(result))


# 保存作业设置信息
def save_asgn_settings(request, sid, aid):
    """
    保存作业设置信息
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.save_asgn_setting()

    return response.json(WeJudgeResult(result))


# 获取实验报告列表
def get_reports_list(request, sid, aid):
    """
    获取实验报告列表
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_reports_list()

    return response.json(WeJudgeResult(result))


# 保存作业的批改信息
def save_asgn_report_checkup(request, sid, aid, rid):
    """
    保存作业的批改信息
    :param request:
    :param aid: asgn id
    :param sid: school id
    :param rid: report id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.save_asgn_report_checkup(rid)

    return response.json(WeJudgeResult(result))


# 批量保存作业的批改信息
def save_asgn_report_checkup_batch(request, sid, aid):
    """
    批量保存作业的批改信息
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.save_asgn_report_checkup_batch()

    return response.json(WeJudgeResult(result))


# 获取作业参考答案
def get_answer(request, sid, aid):
    """
    获取作业参考答案
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_answer()

    return response.json(WeJudgeResult(result))


# 保存作业选题
def save_problem_choosing(request, sid, aid):
    """
    保存作业选题
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.save_problem_choosing()

    return response.json(WeJudgeResult(result))


# 获取调课记录信息
def get_visit_requirement(request, sid, aid):
    """
    获取调课记录信息
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.get_visit_requirement()

    return response.json(WeJudgeResult(result))


# 创建调课信息
def add_visit_requirement(request, sid, aid):
    """
    创建调课信息
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.add_visit_requirement()

    return response.json(WeJudgeResult(result))


# 删除调课请求信息
def delete_visit_requirement(request, sid, aid):
    """
    删除调课请求信息
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.check_assistant()

    result = manager.delete_visit_requirement()

    return response.json(WeJudgeResult(result))


# 删除作业
def delete_asgn(request, sid, aid):
    """
    删除作业
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    course_id = manager.delete_asgn()

    return HttpResponseRedirect(reverse('education.course.index', args=(manager.school.id, course_id)))


# 获取作业的已选择题目
def get_problems_choosed(request, sid, aid):
    """
    获取作业的已选择题目
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    result = manager.get_problems_choosed()

    return response.json(WeJudgeResult(result))


# 重算作业的数据
def refresh_asgn_datas(request, sid, aid):
    """
    重算作业的数据
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    result = manager.refresh_asgn_datas()

    return response.json(WeJudgeResult(result, msg="重算工作已经发起，请稍等"))


# 重算作业的数据
def rejudge_problems(request, sid, aid, pid):
    """
    重算作业的数据
    :param request:
    :param aid: asgn id
    :param sid: school id
    :param pid: problem id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)
    manager.get_problem(pid)

    result = manager.rejudge_problems()

    return response.json(WeJudgeResult(result, msg="重判工作已经发起，请稍等"))


#打包代码
def zip_the_codes(request,sid,aid):
    """
    
    :param request: 
    :param sid: school id
    :param aid: asgn id
    :return: 
    """
    wejudge_session = WeJudgeEducationSession(request) #创建目录
    response = WeJudgeResponse(wejudge_session) #创建相应

    manager = libs.EducationAsgnController(request , response , sid)
    manager.get_asgn(aid)

    result = manager.asgn_zip_the_codes(aid)

    return result



# === Statistic

# 重算作业的数据
def get_statistic_data(request, sid, aid):
    """
    重算作业的数据
    :param request:
    :param aid: asgn id
    :param sid: school id
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationAsgnController(request, response, sid)
    manager.get_asgn(aid)

    result = manager.get_statistic_data()

    return response.json(WeJudgeResult(result))

