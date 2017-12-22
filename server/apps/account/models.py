# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.db import ModelConverter
from django.db import models

__author__ = 'lancelrq'

WENUM_USER_SEX = (
    (-1, '未知'),
    (0, '女'),
    (1, '男')
)


class AccountBase(models.Model):
    """
    公有用户Model
    --- 这个model是可以继承的，并且系统不会创建其对应的数据表
    """

    # 用户名
    username = models.CharField(max_length=50)

    # 用户密码
    password = models.CharField(max_length=100, blank=True, null=True)

    # 用户性别
    sex = models.SmallIntegerField(default=-1, choices=WENUM_USER_SEX)

    # 用户昵称
    nickname = models.CharField(max_length=50, blank=True, null=True)

    # 真实姓名
    realname = models.CharField(max_length=50, blank=True, null=True)

    # Email (不展示)
    email = models.CharField(max_length=100, blank=True, null=True)

    # 用户头像
    headimg = models.CharField(max_length=50, blank=True, null=True)

    # 个性签名
    motto = models.CharField(max_length=255, blank=True, null=True)

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后一次登录的时间
    last_login_time = models.DateTimeField(null=True, blank=True)

    # 账号锁定（不能登录）
    locked = models.BooleanField(default=False)

    # 重试密码计数器
    passwd_retry_counter = models.SmallIntegerField(default=10)

    class Meta:
        # 不创建当前Model的数据表
        abstract = True


class Account(AccountBase, ModelConverter):
    """
    WeJudge主账户表（继承CommonUser）
    """

    class Meta:
        verbose_name = "WeJudge主账户表"
        verbose_name_plural = "WeJudge主账户表"

    # 站点管理员权限
    permission_administrator = models.BooleanField(default=False)

    # 发布题目的权限
    permission_publish_problem = models.BooleanField(default=False)

    # 创建题目集的权限
    permission_create_problemset = models.BooleanField(default=False)

    # 创建比赛的权限
    permission_create_contest = models.BooleanField(default=False)

    """ === 用户账户安全 === """

    # 邮箱是否认证
    email_validated = models.BooleanField(default=False)

    """=== 微信登陆部分 ==="""

    # AccessToken
    wc_access_token = models.CharField(max_length=255, blank=True, null=True)

    # AT过期时间
    wc_expires_in = models.CharField(max_length=255, blank=True, null=True)

    # AT刷新用的RefreshToken
    wc_refresh_token = models.CharField(max_length=255, blank=True, null=True)

    # 微信OpenID
    wc_openid = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    # 微信用户信息
    wc_user_info = models.TextField(blank=True, null=True)

    def __str__(self):

        return 'id = %s ；昵称：%s ；真实姓名：%s' % (self.id, self.nickname, self.realname)
