# -*- coding: utf-8 -*-
# coding:utf-8
import time
from django.db import models
from django.utils.timezone import get_current_timezone
__author__ = 'lancelrq'


class ModelConverter:

    def json(self, items=None, timestamp=True, pre="", timestamp_msec=False):
        """
        转换JSON
        :param items:   设置需要输出的项目，如果不设置默认为所有，格式和django的命名格式一致
        :param pre:     递归使用的前缀标识符(不用管）
        :param timestamp: 时间信息输出为时间戳，设置为否，则输出文本日期
        :param timestamp_msec: 精确到毫秒
        :return:
        """
        if items is None or not isinstance(items, list):
            items = None

        dict_out = {}

        for f in self._meta.fields:
            if isinstance(f, models.CharField) \
                    or isinstance(f, models.IntegerField) \
                    or isinstance(f, models.BigIntegerField) \
                    or isinstance(f, models.AutoField) \
                    or isinstance(f, models.TextField) \
                    or isinstance(f, models.FloatField) \
                    or isinstance(f, models.SmallIntegerField) \
                    or isinstance(f, models.BooleanField):
                # 常规Field
                if items is not None:   # 判定是否需要输出
                    if "%s%s" % (pre, f.name) not in items:
                        continue
                dict_out[f.name] = getattr(self, f.name)

            elif isinstance(f, models.DateTimeField):
                if items is not None:   # 判定是否需要输出
                    if "%s%s" % (pre, f.name) not in items:
                        continue
                item = getattr(self, f.name)
                if item is None:
                    dict_out[f.name] = None
                else:
                    if timestamp:
                        if timestamp_msec:
                            ms = item.microsecond
                            dict_out[f.name] = int((time.mktime(item.timetuple()) * 1000000 + ms) / 1000)
                        else:
                            dict_out[f.name] = int(time.mktime(item.timetuple()))
                    else:
                        dict_out[f.name] = item.strftime('%Y-%m-%d %H:%M:%S')

            elif isinstance(f, models.TimeField):
                if items is not None:   # 判定是否需要输出
                    if "%s%s" % (pre, f.name) not in items:
                        continue
                item = getattr(self, f.name)
                if item is None:
                    dict_out[f.name] = None
                else:
                    if timestamp:
                        dict_out[f.name] = item.hour * 3600 + item.minute * 60 + item.second
                    else:
                        dict_out[f.name] = item.strftime('%H:%M:%S')

            elif isinstance(f, models.ForeignKey):
                if items is not None:   # 判定是否需要输出
                    s1 = "%s%s" % (pre, f.name)
                    s2 = "%s%s_id" % (pre, f.name)
                    s3 = "%s%s__str" % (pre, f.name)
                    if s1 in items:
                        item = getattr(self, f.name)
                        if item is None:
                            dict_out[f.name] = None
                        else:
                            dict_out[f.name] = item.json(items, pre="%s%s__" % (pre, f.name), timestamp=True)

                    if s3 in items:
                        dict_out["%s__str" % f.name] = str(getattr(self, f.name))

                    if s2 in items:
                        dict_out["%s_id" % f.name] = getattr(self, "%s_id" % f.name)

        return dict_out
