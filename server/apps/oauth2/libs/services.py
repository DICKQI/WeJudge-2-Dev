# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import uuid
import time
import hashlib
import base64
import apps.oauth2.models as Oauth2Model
import apps.education.models as EducationModel
import apps.contest.models as ContestModel
import apps.account.models as AccountModel
from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from wejudge.utils import tools
from .provider import Oauth2Provider


class Oauth2Service(Oauth2Provider):

    def __init__(self, request, response):
        super(Oauth2Provider, self).__init__(request, response)

    def authorize(self):
        """
        引导授权页面
        :return:
        """
        parser = ParamsParser(self._request, exception_privider=Oauth2Error)

        appid = parser.get_str('appid', require=True, errcode=40000)
        redirect_uri = parser.get_str('redirect_uri', require=True, errcode=40010)
        response_type = parser.get_str('response_type', require=True, errcode=40002)
        state = parser.get_str('state', '')

        self.get_client(appid)

        if response_type != 'code':
            raise Oauth2Error(40002)

        if redirect_uri != self.client.redirect_uris:
            raise Oauth2Error(40010)

        # GET 方法
        if self._request.method.upper() == 'GET':

            if self.session.is_logined():     # 如果用户已经登录了

                account = self.session.account
                account_type = self.get_account_type(account)
                # 拿授权信息
                self.get_or_create_oauth_user_by_account_id(account_type, account.id)

                if self.check_user_allow(False):
                    # 创建授权Code
                    self.oauth_user.auth_code = self.gen_authorize_code()
                    self.oauth_user.auth_code_expires_at = int(time.time()) + 600
                    self.oauth_user.save()
                    return True, "%s?code=%s&state=%s" % (
                        self.client.redirect_uris, self.oauth_user.auth_code, state
                    ), None

            # 渲染授权请求页面
            return False, "", {
                "client": self.client,
                "appid": appid,
                "redirect_uri": redirect_uri,
                "response_type": response_type,
                "state": state,
                "urlcall": self._request.GET.urlencode()
            }

        elif self._request.method.upper() == 'POST':

            if not self.session.is_logined():  # 如果用户未登录
                raise Oauth2Error(1)

            account = self.session.account
            account_type = self.get_account_type(account)
            # 拿授权信息
            self.get_or_create_oauth_user_by_account_id(account_type, account.id)

            parser = ParamsParser(self._request, exception_privider=Oauth2Error)
            confirm = parser.get_boolean('confirm', True, require=True, method='POST')

            self.oauth_user.is_allow = confirm
            self.oauth_user.save()

            if self.oauth_user.is_allow:
                # 创建授权Code
                self.oauth_user.auth_code = self.gen_authorize_code()
                self.oauth_user.auth_code_expires_at = int(time.time()) + 600
                self.oauth_user.save()
                return True, "%s?code=%s&state=%s" % (
                    self.client.redirect_uris, self.oauth_user.auth_code, state
                ), None
            else:
                return True, self.client.cancel_redirect_uri, None

        else:
            raise Oauth2Error(40500, errmsg="错误的请求方法", httpcode=405)

    def access_token(self):
        """
        用code换取access token
        :return:
        """
        parser = ParamsParser(self._request, exception_privider=Oauth2Error)
        appid = parser.get_str('appid', require=True, errcode=40000)
        appsecret = parser.get_str('appsecret', require=True, errcode=40005, method='POST')
        grant_type = parser.get_str('grant_type', require=True, errcode=40006, method='POST')
        code = parser.get_str('code', require=True, errcode=40007, method='POST')

        self.get_client(appid)
        # 检查Appsecret
        self.check_app_secret(appsecret)
        # 检查授权类型
        if grant_type != 'authorization_code':
            raise Oauth2Error(40006)
        # 通过Auth Code获取授权用户
        self.get_oauth_user_by_auth_code(code)
        if not self.check_user_allow(False):
            raise Oauth2Error(40003)
        # 判断授权是否过期
        if self.oauth_user.auth_code_expires_at < int(time.time()):
            self.oauth_user.auth_code_expires_at = 0
            self.oauth_user.auth_code = ""
            self.oauth_user.save()
            raise Oauth2Error(40007)

        at = self.oauth_user.tokens.order_by('-id')
        if not at.exists():
            at = self.create_new_access_token()
            self.oauth_user.tokens.add(at)
        else:
            at = at[0]
            # 如果Token已经过期，则创建新的Token
            if at.expires_at - int(time.time()) < 0:
                at.delete()
                at = self.create_new_access_token()
                self.oauth_user.tokens.add(at)
            # 如果当前时间离过期时间还剩不到10分钟，则创建新的Token，但不删除当前Token
            elif at.expires_at - int(time.time()) < 600:
                at = self.create_new_access_token()
                self.oauth_user.tokens.add(at)
            # 否则返回当前可用Token

        self.oauth_user.auth_code = ""
        self.oauth_user.auth_code_expires_at = 0

        return {
            "access_token": at.access_token,
            "expires_in": self.client.at_expires_time,           # 返回客户允许的过期时长
            "expires_at": at.expires_at,                        # 返回过期时间的服务器时间戳
            "refresh_token": at.refresh_token,
            "openid": self.oauth_user.open_id,
            "account_type": self.oauth_user.account_type         # 返回账户类型
        }

    def valid_access_token(self):
        """
        返回Access Token是否有效
        :return:
        """
        parser = ParamsParser(self._request, exception_privider=Oauth2Error)
        appid = parser.get_str('appid', require=True, errcode=40000, method='GET')
        appsecret = parser.get_str('appsecret', require=True, errcode=40005, method='POST')
        openid = parser.get_str('openid', require=True, errcode=40001, method='POST')
        access_token = parser.get_str('access_token', require=True, errcode=40004, method='POST')

        self.get_client(appid)
        # 检查Appsecret
        self.check_app_secret(appsecret)
        self.get_oauth_user(openid)
        self.check_access_token(access_token)

        return {}

    def refresh_token(self):
        """
        刷新Access Token
        :return:
        """

        parser = ParamsParser(self._request, exception_privider=Oauth2Error)
        appid = parser.get_str('appid', require=True, errcode=40000, method='GET')
        appsecret = parser.get_str('appsecret', require=True, errcode=40005, method='POST')
        openid = parser.get_str('openid', require=True, errcode=40001, method='POST')
        access_token = parser.get_str('access_token', require=True, errcode=40004, method='POST')
        refresh_token = parser.get_str('refresh_token', require=True, errcode=40008, method='POST')

        self.get_client(appid)
        # 检查Appsecret
        self.check_app_secret(appsecret)
        self.get_oauth_user(openid)
        # 如果Access Token失效，则RefreshToken也同时失效！
        at = self.check_access_token(access_token)

        if at.refresh_token != refresh_token:
            raise Oauth2Error(40008)

        at.expires_at = int(time.time()) + self.client.rt_expires_time
        at.refresh_token = self.gen_refresh_token()
        at.save()

        return {
            "openid": self.oauth_user.open_id,
            "expires_in": self.client.rt_expires_time,            # 返回客户允许的过期时长
            "expires_at": at.expires_at,                        # 返回过期时间的服务器时间戳
            "refresh_token": at.refresh_token                   # 新的Token
        }
