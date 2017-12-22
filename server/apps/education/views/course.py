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


# 教学系统课程信息
def course(request, sid, cid):
    """
    教学系统课程信息
    :param request:
    :param cid: Course Id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationController(request, response, sid)
    manager.get_course(cid)

    # 检查访问权限
    manager.login_check()
    manager.check_assistant()  # 助教提权
    # 检查课程访问权限
    manager.check_course_visit()

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term)]
    ])

    return response.render_page(request, 'education/course/course.tpl', {
        "course": manager.course,
        "course_teachers": [teacher for teacher in manager.course.teacher.all()],
        "course_arrangements": [arrangement for arrangement in manager.course.arrangements.all()],
        "school": manager.school,
        "page_name": "INDEX"
    })


# 教学系统课程排课管理
def arrangements(request, sid, cid):
    """
    教学系统课程排课管理
    :param request:
    :param cid: Course Id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationController(request, response, sid)
    manager.get_course(cid)

    # 检查访问权限
    manager.login_check()
    manager.check_assistant()  # 助教提权
    # 检查课程访问权限
    manager.check_course_visit()
    manager.check_user_privilege(2)

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term),
         'education.course.index', (manager.school.id, manager.course.id)],
        ["排课管理"]
    ])
    return response.render_page(request, 'education/course/arrangements.tpl', {
        "course": manager.course,
        "school": manager.school,
        "page_name": "ARRANGEMENTS"
    })


# 教学系统资源仓库列表
def repository(request, sid, cid):
    """
    教学系统资源仓库列表
    :param request:
    :param cid: Course Id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationController(request, response, sid)
    manager.get_course(cid)

    # 检查访问权限
    manager.login_check()
    manager.check_assistant()  # 助教提权
    # 检查课程访问权限
    manager.check_course_visit()

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term),
         'education.course.index', (manager.school.id, manager.course.id)],
        ["教学资源仓库"]
    ])
    return response.render_page(request, 'education/course/repository.tpl', {
        "course": manager.course,
        "school": manager.school,
        "page_name": "REPOSITORY"
    })


# 教学系统课程设置页面
def settings(request, sid, cid):
    """
    教学系统课程设置页面
    :param request:
    :param cid: Course Id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)                                 # 创建响应

    manager = libs.EducationController(request, response, sid)
    manager.get_course(cid)

    # 检查访问权限
    manager.login_check()
    manager.check_assistant()  # 助教提权
    # 检查课程访问权限
    manager.check_course_visit()
    manager.check_user_privilege(2)

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ["%s (%s)" % (manager.course.name, manager.course.term),
         'education.course.index', (manager.school.id, manager.course.id)],
        ["课程设置"]
    ])
    return response.render_page(request, 'education/course/settings.tpl', {
        "course": manager.course,
        "school": manager.school,
        "page_name": "SETTINGS"
    })


# === API ===


# 教学系统课程作业接口
def api_course_asgn(request, sid, cid):
    """
    教学系统课程作业接口
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)
    manager.check_assistant()  # 助教提权

    return response.json(WeJudgeResult(manager.get_asgn_list()))


# 创建作业接口
def api_create_asgn(request, sid, cid):
    """
    创建作业接口
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    return response.json(WeJudgeResult(manager.create_asgn()))


# 当前课程的排课信息列表
def api_get_course_arrangements(request, sid, cid):
    """
    当前课程的排课信息列表
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.get_arrangements_list()

    return response.json(WeJudgeResult(result))


# 当前课程的排课信息列表
def api_get_students_by_arrangements(request, sid, cid, arrid):
    """
    当前课程的排课信息列表
    :param request:
    :param cid: course id
    :param sid:
    :param arrid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.get_students_by_arrangements(arrid)

    return response.json(WeJudgeResult({
        "data": result
    }))


# 增删改排课信息
def api_change_arrangements(request, sid, cid):
    """
    增删改排课信息
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.change_arrangements()

    return response.json(WeJudgeResult(result))


# 向排课添加/删除学生
def api_toggle_student_to_arrangements(request, sid, cid):
    """
    向排课添加/删除学生
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.toggle_student_to_arrangements()

    return response.json(WeJudgeResult(result))


# 获取课程设置信息
def get_course_settings_info(request, sid, cid):
    """
    获取课程设置信息
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.get_course_settings_info()

    return response.json(WeJudgeResult(result))


# 保存课程设置信息
def save_course_settings(request, sid, cid):
    """
    保存课程设置信息
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.save_course_info()

    return response.json(WeJudgeResult(result))


# 向课程添加/删除学生助教
def api_toggle_assistant_to_course(request, sid, cid):
    """
    向课程添加/删除学生助教
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.toggle_assistant_to_course()

    return response.json(WeJudgeResult(result))


# 向课程添加/删除老师
def api_toggle_teacher_to_course(request, sid, cid):
    """
    向课程添加/删除老师
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.toggle_teacher_to_course()

    return response.json(WeJudgeResult(result))


# 向课程添加/删除教学资源库关联
def api_toggle_repository_to_course(request, sid, cid):
    """
    向课程添加/删除教学资源库关联
    :param request:
    :param cid: course id
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)

    result = manager.toggle_repository_to_course()

    return response.json(WeJudgeResult(result))


# XLS导入学生账户
def xls_student_to_arrangements(request, sid, cid, arrid):
    """
    XLS导入学生账户
    :param request:
    :param sid:
    :param cid:
    :param arrid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)
    result = manager.xls_student_to_arrangements(arrid)

    return response.json(WeJudgeResult(msg=result))


# 删除课程
def delete_course(request, sid, cid):
    """
    删除课程
    :param request:
    :param sid:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)
    school_id = manager.delete_course()

    return HttpResponseRedirect(reverse('education.school', args=(school_id, )))


def asgn_score_count(request, sid , cid):
    """
    作业成绩统计
    :param request: 
    :param sid: 
    :return: 
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建目录
    response = WeJudgeResponse(wejudge_session)  # 创建相应

    manager = libs.EducationCourseController(request, response, sid)
    manager.get_course(cid)
    manager.get_asgn_list()

    result = manager.asgn_score_counter()

    return  response.json(WeJudgeResult(result))