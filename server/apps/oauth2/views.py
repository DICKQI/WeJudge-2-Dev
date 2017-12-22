# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge import const
import apps.oauth2.libs as libs
import apps.education.libs as EduLibs
from django.http.response import HttpResponseRedirect


def authorize_education(request, sid):
    """
    Oauth2教学系统授权页面
    :param request:
    :return:
    """

    wejudge_session = WeJudgeEducationSession(request)  # 创建会话
    response = WeJudgeResponse(wejudge_session)  # 创建响应

    education_manager = EduLibs.EducationController(request, response, sid)

    manager = libs.Oauth2Service(request, response)
    rel, url, ctx = manager.authorize()

    response.set_navlist([
        const.apps.EDUCATION,
        [education_manager.school.name, 'education.school', (education_manager.school.id,)],
        ['WeJudge开放平台'],
        [manager.client.appname],
        ['应用授权']
    ])

    if not rel:
        ctx.update({
            "school": education_manager.school,
            "page_name": "INDEX"
        })
        return response.render_page(request, 'oauth2/authorize/education.tpl', ctx)
    else:
        return HttpResponseRedirect(url)


@WeJudgePOSTRequire
def access_token(request):
    """
    AccessToken换取接口
    :param request:
    :return:
    """
    response = JsonResponse({})
    manager = libs.Oauth2Service(request, response)
    rel = manager.oauth2_success(manager.access_token())

    response.content = json.dumps(rel)
    return response


@WeJudgePOSTRequire
def valid_access_token(request):
    """
    AccessToken校验接口
    :param request:
    :return:
    """
    response = JsonResponse({})
    manager = libs.Oauth2Service(request, response)
    rel = manager.oauth2_success(manager.valid_access_token())

    response.content = json.dumps(rel)
    return response


@WeJudgePOSTRequire
def refresh_token(request):
    """
    Refresh Access Token 接口
    :param request:
    :return:
    """
    response = JsonResponse({})
    manager = libs.Oauth2Service(request, response)
    rel = manager.oauth2_success(manager.refresh_token())

    response.content = json.dumps(rel)
    return response
