# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.const import system
from django import template

__author__ = 'lancelrq'


register = template.Library()


@register.filter(name='desc_status_flag')
def desc_status_flag(value, arg=None):
    try:
        desc = system.WEJUDGE_JUDGE_STATUS_DESC.get(int(value))
        return '<h1 class="ui %s header">%s</h1>' % (desc.get('color'), desc.get('title'))
    except:
        return None
