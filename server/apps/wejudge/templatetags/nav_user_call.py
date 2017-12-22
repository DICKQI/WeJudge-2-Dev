# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.utils import *
from wejudge.const import system
from django import template

__author__ = 'lancelrq'


register = template.Library()


@register.filter(name='nav_user_call')
def nav_user_call(value, arg=None):
    try:
        if isinstance(value, WeJudgeAccount):
            if isinstance(value, WeJudgeEducationAccount):
                return "%s%s" % (
                    value.entity.realname,
                    system.WEJUDGE_EDU_ACCOUNT_ROLES.call_friendly(value.entity.role)
                )
            elif isinstance(value, WeJudgeContestAccount):
                return "%s%s" % (
                    value.entity.nickname,
                    system.WEJUDGE_CONTEST_ACCOUNT_ROLES.call_friendly(value.entity.role)
                )

            else:
                return "%s" % value.entity.nickname
        else:
            return ""
    except Exception as ex:
        return str(ex)