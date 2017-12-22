# -*- coding: utf-8 -*-
# coding:utf-8

from django import template

__author__ = 'lancelrq'


register = template.Library()


@register.filter(name='attr')
def attr(value, arg=None):
    try:
        if isinstance(value, dict):
            return value.get(arg, None)
        else:
            return getattr(value, arg)
    except Exception as ex:
        return None