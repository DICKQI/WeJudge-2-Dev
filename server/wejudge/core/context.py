# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import time
import apps.wejudge.models as WeJudgeModel
import wejudge.const as sys_const


class WebConfiguration(object):
    """全站全局配置信息"""

    def __init__(self):
        """
        初始化配置信息
        :return:
        """
        """
        加载配置信息
        :return:
        """

        settings = WeJudgeModel.Setting.objects.all()
        if settings.exists():
            self.__setting = settings[0]
        else:
            self.__setting = WeJudgeModel.Setting()
            self.__setting.web_title = ""
            self.__setting.save()
            self.server_time = int(time.time())

    def __getattr__(self, item):
        """
        获取配置信息
        :param item: 属性名称
        :return:
        """
        if '__setting' in item:
            return object.__getattribute__(self, item)
        elif 'server_time' == str(item):
            return int(time.time())
        elif hasattr(self.__setting, item):
            return getattr(self.__setting, item)
        else:
            raise AttributeError("WebConfiguration attribute %s not found" % item)

    def __setattr__(self, key, value):
        """
        更改配置信息
        :param key: 属性名称
        :param value: 新值
        :return:
        """
        if '__setting' in key:
            return object.__setattr__(self, key, value)
        if hasattr(self.__setting, key):
            setattr(self.__setting, key, value)
        else:
            raise AttributeError("WebConfiguration attribute %s not found" % key)

    def save(self):
        """
        保存配置信息到数据库
        :return:
        """
        self.__setting.save()


wejudge_assets_hash = None

def WejudgeContext(request):
    """
    WeJudge 上下文管理器
    :param request:
    :return:
    """
    import os
    import json
    import time
    global wejudge_assets_hash

    config = WebConfiguration()

    from django.conf import settings

    if settings.DEBUG or wejudge_assets_hash is None:
        try:
            f = open(os.path.join(settings.BASE_DIR, 'config/assets.json'), 'r')
            assets_config = json.loads(f.read())
            f.close()
            wejudge_assets_hash = assets_config.get('hash')
        except:
            wejudge_assets_hash = ""

    return {
        "wejudge_assets_hash": wejudge_assets_hash,
        "wejudge_config": config,
        "wejudge_const": sys_const,
        "wejudge_servertime": int(time.time()),
        "django_settings": settings
    }