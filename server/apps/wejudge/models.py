# -*- coding: utf-8 -*-
# coding:utf-8

from django.db import models

__author__ = 'lancelrq'


# 全站设置
class Setting(models.Model):

    class Meta:
        verbose_name = "系统选项总表"
        verbose_name_plural = "系统选项总表"

    # 网站标题
    web_title = models.CharField(max_length=255, blank=True, null=True)

    # 网站Keyword
    web_keyword = models.CharField(max_length=255, blank=True, null=True)

    # 网站简介
    web_desc = models.CharField(max_length=255, blank=True, null=True)

    # 网站版本
    web_version = models.CharField(max_length=50, blank=True, null=True)

    # 维护模式
    web_fixing = models.BooleanField(default=False)

    # 暂停评测（全局）
    web_stop_judging = models.BooleanField(default=False)

    # 是否开放网站注册
    web_register = models.BooleanField(default=False)

    # smtp服务器
    smtp_server = models.CharField(max_length=50, blank=True, null=True)

    # smtp用户名
    smtp_user = models.CharField(max_length=50, blank=True, null=True)

    # smtp密码
    smtp_pwd = models.CharField(max_length=50, blank=True, null=True)

    # smtp发件账户
    smtp_mail_from = models.CharField(max_length=50, blank=True, null=True)

    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.web_title