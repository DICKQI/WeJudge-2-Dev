# -*- coding: utf-8 -*-
# coding:utf-8

from django import template
from wejudge.utils import tools
register = template.Library()

__author__ = 'lancelrq'


def problem_index(value, arg=None):
    try:
        return tools.gen_problem_index(value)
    except:
        return "NaN"

register.filter('problem_index', problem_index)