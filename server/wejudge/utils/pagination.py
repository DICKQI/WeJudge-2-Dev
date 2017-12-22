# -*- coding: utf-8 -*-
# coding:utf-8
import math

__author__ = 'lancelrq'


def WeJudgePagination(model_object, limit=10, page=1, display=11):
    """
    实现分页系统的装饰器
    :param model_object: ModelManager对象
    :param limit: 每页显示记录数
    :param page: 当前第几页
    :param display: 一共显示多少个页面的直接链接
    :return:
    """
    def decorator(func):
        """
        单项处理函数
        :param func: 这个函数的定义是：func(obj)，将迭代传入每一个obj对象
        :return:
        """
        def wrapper(*args, **kw):
            # 处理传入值
            _page = page if page >= 1 else 1
            _limit = limit if limit >= 1 else 10
            _display = display if display >= 1 else 11

            # 获取记录总数
            total = model_object.count()
            # 获取统计数量：
            data = [],
            pagination = {
                "pages": [1],
                "now_page": _page,
                "page_total": 1,
                "total": total,
                "limit": _limit,
                "display": _display
            }
            if total == 0:
                return {
                    "data": [],
                    "pagination": pagination
                }
            # 计算页面总数
            page_total = int(math.ceil(total / (_limit * 1.0)))
            pagination["page_total"] = page_total
            # 修正页面
            if _page > page_total:
                _page = page_total
            # 获取记录起点索引
            start_idx = _limit * (_page - 1)
            # 对记录进行分页
            data = [func(x, *args, **kw) for x in model_object[start_idx: start_idx + _limit]]
            # 获取分页信息
            pagination['pages'] = list(pager_calculation(page_total, _page, display=11))
            return {
                "data": data,
                "pagination": pagination
            }
        return wrapper
    return decorator


def pager_calculation(total, nowpage=1, display=11):
    """
    分页计算程序
    :param total: 记录总数
    :param nowpage: 当前第几页
    :param display: 一共显示多少个页面的直接链接
    :return:
    """
    if total <= display:
        return range(1, total+1)
    half = int(math.ceil(display / 2.0))
    if int(nowpage) < int(half):
        return range(1, display + 1)
    if int(nowpage + half > total):
        return range(total - display + 1, total + 1)
    else:
        return range(nowpage - half + 1, nowpage + half)