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


# 资源库首页
def repository(request, sid, rid):

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)         # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    manager.check_repo_visit_privilege()

    response.set_navlist([
        const.apps.EDUCATION,
        [manager.school.name, 'education.school', (manager.school.id,)],
        ['教学资源仓库', 'education.school.repository', (manager.school.id,)],
        [manager.repository.title]
    ])

    return response.render_page(request, 'education/repository/repository.tpl', {
        "school": manager.school,
        "repository": manager.repository,
        "page_name": "REPOSITORY"
    })

# === API ===


# 获取学校下的所有仓库列表
def repositories_list(request, sid, cid=None):
    """
    获取学校下的所有仓库列表
    :param request:
    :param sid:
    :param cid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)

    if cid is not None:
        manager.get_course(cid)

    result = manager.get_repositories_list()

    return response.json(WeJudgeResult(result))


# 获取文件夹列表树（jstree格式)
def get_folders_tree(request, sid, rid):
    """
    获取文件夹列表树（jstree格式)
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.get_folders_tree()

    return response.json(result)


# 获取文件列表
def get_files_map(request, sid, rid):
    """
    获取文件列表
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.get_files_map()

    return response.json(WeJudgeResult(result))


# 新建文件夹
def repo_new_folder(request, sid, rid):
    """
    新建文件夹
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.repo_new_folder()

    return response.json(WeJudgeResult(result))


# 上传文件
def repo_upload_file(request, sid, rid):
    """
    上传文件
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.repo_upload_file()

    return response.json(WeJudgeResult(result))


# 删除文件/文件夹
def repo_delete(request, sid, rid):
    """
    删除文件/文件夹
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.repo_delete()

    return response.json(WeJudgeResult(result))


# 获取仓库信息
def repo_info(request, sid, rid):
    """
    获取仓库信息
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.repository.json(items=[
        'id', 'title', 'author', 'author__id', 'author__nickname',
        'author__realname', 'public_level', 'cur_size',
    ])

    return response.json(WeJudgeResult(result))


# 更改仓库信息
def edit_repo(request, sid, rid):
    """
    更改仓库信息
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.edit_repo()

    return response.json(WeJudgeResult(result))


# 增加仓库
def new_repo(request, sid):
    """
    增加仓库
    :param request:
    :param sid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    result = manager.edit_repo()

    return response.json(WeJudgeResult(result))


# 删除仓库
def delete_repo(request, sid, rid):
    """
    删除仓库
    :param request:
    :param sid:
    :param rid:
    :return:
    """
    wejudge_session = WeJudgeEducationSession(request)      # 创建会话
    response = WeJudgeResponse(wejudge_session)             # 创建响应

    manager = libs.EducationRepositoryController(request, response, sid)
    manager.get_repository(rid)
    result = manager.delete_repo()

    return response.json(WeJudgeResult(result))
