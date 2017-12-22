# -*- coding: utf-8 -*-
# coding:utf-8

from django.views.decorators.csrf import csrf_exempt
from wejudge.core import *
from wejudge.utils import *
import wejudge.const as const
from django.views.decorators.cache import cache_page
from apps.wejudge.libs import CKEditorAPIController
__author__ = 'lancelrq'


@csrf_exempt
def imgupload(request):
    """
    上传图片
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = CKEditorAPIController(request, response)

    return response.html(manager.ckeditor_imgupload())


@csrf_exempt
def fileupload(request):
    """
    上传文件
    :param request:
    :return:
    """

    wejudge_session = WeJudgeSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    manager = CKEditorAPIController(request, response)

    return response.html(manager.ckeditor_fileupload())

