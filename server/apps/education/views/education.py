# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge import const
import apps.education.libs as libs
from wejudge.const import system
from django.shortcuts import reverse
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.template import Context, Template


# 教学系统首页
def index(request):
    """
    教学系统首页
    :param request:
    :return:
    """
    wejudge_session = WeJudgeSession(request)       # 创建会话
    response = WeJudgeResponse(wejudge_session)     # 创建响应

    parser = ParamsParser(request)

    if not parser.get_boolean("choose"):
        sid = request.COOKIES.get('EDU_LAST_VISITED_SCHOOL', None)
        if sid is not None and libs.EducationController.get_school_by_school_id(sid, throw=False):
            return HttpResponseRedirect(reverse("education.school", args=(sid,)))
        else:
            response.delete_cookie('EDU_LAST_VISITED_SCHOOL')

    response.set_navlist([
        const.apps.EDUCATION
    ])
    return response.render_page(request, 'education/school/school_choose.tpl', {
        "school_list": libs.EducationController.get_schools_list(),
        "hide_login": True
    })


# 学校首页
def school_index(request, sid):
    if not tools.is_numeric(sid):
        school = libs.EducationController.get_school_by_short_name(sid)
        return HttpResponseRedirect(reverse("education.school", args=[school.id]))

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.EducationController(request, response, sid)

    __change_term(request, manager)

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name]
    ])
    # 设置学校访问记录
    response.set_cookie('EDU_LAST_VISITED_SCHOOL', sid, expires=365 * 86400)

    academies = [academy.json(items=['id', 'name']) for academy in manager.get_school_academies()]

    storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.EDUCATION_STORAGE, str(manager.school.id))
    if storage.exists("intro.html"):
        fp = storage.open_file("intro.html", 'r')
        index_view = fp.read()
        fp.close()
        t = Template(index_view)
        index_view = t.render(Context({
            "school": manager.school,
            "term_list": manager.get_terms_list(),
            "now_term": manager.term,
            "wejudge_session": manager.session
        }))
    else:
        index_view = ""

    return response.render_page(request, 'education/school/school.tpl', {
        "school": manager.school,
        "term_list": manager.get_terms_list(),
        "now_term": manager.term,
        "WJ_EDU_ARC": system.WEJUDGE_EDU_ACCOUNT_ROLES_CALLED,
        "page_name": "INDEX",
        "hide_breadcrumb": True,
        "academies": json.dumps(academies),
        "index_view": index_view
    })


# 教学资源
def repository(request, sid):

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.EducationController(request, response, sid)

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id,)],
        ['教学资源仓库']
    ])

    return response.render_page(request, 'education/school/repository.tpl', {
        "school": manager.school,
        "page_name": "REPOSITORY",
    })


# # 课程中心
# def courses(request, sid):
#
#     wejudge_session = WeJudgeEducationSession(request)  # 创建会话
#     response = WeJudgeResponse(wejudge_session)         # 创建响应
#
#     manager = libs.EducationController(request, response, sid)
#
#     # 检查访问权限
#     manager.login_check()
#
#     __change_term(request, manager)
#
#     response.set_navlist([
#         const.apps.EDUCATION,
#         [manager.school.name, 'education.school', (manager.school.id, )],
#         ['课程中心']
#     ])
#
#     academies = [academy.json(items=['id', 'name']) for academy in manager.get_school_academies()]
#
#     return response.render_page(request, 'education/school/courses.tpl', {
#         "school": manager.school,
#         "term_list": manager.get_terms_list(),
#         "now_term": manager.term,
#         "WJ_EDU_ARC": system.WEJUDGE_EDU_ACCOUNT_ROLES_CALLED,
#         "page_name": "COURSES",
#         "academies": json.dumps(academies)
#     })


# 学校管理
def management(request, sid):

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.EducationController(request, response, sid)

    # 检查访问权限
    manager.login_check()
    manager.check_user_privilege(3)

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id, )],
        ['学校管理']
    ])

    academies = [academy.json(items=['id', 'name']) for academy in manager.get_school_academies()]

    return response.render_page(request, 'education/school/manager.tpl', {
        "school": manager.school,
        "term_list": manager.get_terms_list(),
        "now_term": manager.term,
        "WJ_EDU_ARC": system.WEJUDGE_EDU_ACCOUNT_ROLES_CALLED,
        "page_name": "MANAGER",
        "academies": json.dumps(academies)
    })


# 如果有改变学期的要求，则自动处理
def __change_term(request, manager):
    parser = ParamsParser(request)
    change_term = parser.get_int("term", 0)

    if manager.school is not None:

        if change_term > 0:
            new_term = manager.get_term(change_term)
            if new_term is not None:
                # 设置学期
                manager.set_term_to_session(new_term)
            else:
                raise WeJudgeError(3003)

            return HttpResponseRedirect(reverse("education.school", args=(manager.school.id,)))


# === API ===

# 获取当前学校的所有课程信息
def get_courses_list(request, sid):
    """
    获取当前学校的所有课程信息
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.get_courses_list()

    return response.json(WeJudgeResult(result))


# 教学系统首页作业和课程列表
def api_course_asgn(request, sid):
    """
    教学系统首页作业和课程列表
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.get_education_course_asgn_datas()

    return response.json(WeJudgeResult(result))


# 创建课程
def create_course(request, sid):
    """
    创建课程
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.create_course()

    return response.json(WeJudgeResult(result))


# 获取学校账户列表
def get_account_list(request, sid):
    """
    获取学校账户列表
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.get_account_list()

    return response.json(WeJudgeResult(result))


# 新增或编辑用户信息
def edit_account(request, sid):
    """
    新增或编辑用户信息
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.edit_account()

    return response.json(WeJudgeResult(result))


# 删除用户
def delete_account(request, sid):
    """
    删除用户
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.delete_account()

    return response.json(WeJudgeResult(result))


# 获取学校的设置信息
def get_schools_info(request, sid):
    """
    获取学校的设置信息
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.get_schools_info()

    return response.json(WeJudgeResult(result))


# 保存上课时间信息
def save_sections_data(request, sid):
    """
    保存上课时间信息
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.save_sections_data()

    return response.json(WeJudgeResult(result))


# 增加/删除学年学期
def change_year_terms(request, sid):
    """
    增加/删除学年学期
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.change_year_terms()

    return response.json(WeJudgeResult(result))


# 增加/删除学年学期
def save_school_info(request, sid):
    """
    增加/删除学年学期
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.save_school_info()

    return response.json(WeJudgeResult(result))


# 导入学生账户
def xls_import_account(request, sid):
    """
    导入学生账户
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.xls_import_account()

    return response.json(WeJudgeResult(msg=result))


# 注册或者绑定WeJudge主账户
def master_register_or_bind(request, sid):
    """
    注册或者绑定WeJudge主账户
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = libs.EducationController(request, response, sid)
    result = manager.master_register_or_bind()

    return response.json(WeJudgeResult(msg=result))


# 搜索教师用户接口
def api_search_account(roles):

    def func(request, sid):
        parser = ParamsParser(request)
        kw = parser.get_str('kw', '')

        if kw == '':
            return JsonResponse({
                "results": []
            })

        results = []

        def find(role):
            accounts = libs.EducationController.search_user(kw, sid, role=role)
            for account in accounts:
                results.append({
                    "description": "%s(%s)" % (account.realname, account.username),
                    "title": account.username
                })

        for role in roles:
            find(role)

        return JsonResponse({
            "results": results
        })

    return func