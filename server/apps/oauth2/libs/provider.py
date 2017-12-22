# -*- coding: utf-8 -*-
# coding:utf-8

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

__author__ = 'lancelrq'


class Oauth2Provider(WeJudgeControllerBase):

    def __init__(self, request, response):
        self.client = None
        self.oauth_user = None
        super(Oauth2Provider, self).__init__(request, response)

    def get_client(self, appid):
        """
        获取Client对象
        :param appid:
        :return:
        """
        client = Oauth2Model.Client.objects.filter(app_id=appid)
        if not client.exists():
            raise Oauth2Error(40000)
        self.client = client[0]

    def get_oauth_user(self, open_id):
        """
        获取Oauth用户对象
        :param
        :return:
        """
        uu = Oauth2Model.OauthUser.objects.filter(client=self.client, open_id=open_id)
        if not uu.exists():
            raise Oauth2Error(40001)
        self.oauth_user = uu[0]

    def get_oauth_user_by_auth_code(self, auth_code):
        """
        使用Auth Code获取Oauth用户对象
        :param
        :return:
        """
        uu = Oauth2Model.OauthUser.objects.filter(client=self.client, auth_code=auth_code)
        if not uu.exists():
            raise Oauth2Error(40007)
        self.oauth_user = uu[0]

    def get_or_create_oauth_user_by_account_id(self, account_type, account_id):
        """
        获取Oauth用户对象（通过account类型和ID）
        :param account_type:
        :param account_id:
        :return:
        """
        uu = Oauth2Model.OauthUser.objects.filter(client=self.client, account_type=account_type, account_id=account_id)
        if not uu.exists():
            uu = Oauth2Model.OauthUser()
            uu.client = self.client
            uu.account_type = account_type
            uu.account_id = account_id
            uu.open_id = self.gen_open_id()
            uu.save()
            self.oauth_user = uu
        else:
            self.oauth_user = uu[0]

    def gen_open_id(self):
        """
        计算openid
        :param client:
        :param user:
        :return:
        """
        raw = u"<%s>(%s)" % (self.client.app_id, uuid.uuid4())
        sha1 = hashlib.sha1()
        sha1.update(raw.encode('utf-8'))
        return "wejudge_%s" % base64.b64encode(sha1.digest()).decode("utf-8")

    def gen_access_token(self):
        """
        计算Access Token
        :param client:
        :param user:
        :return:
        """
        raw = u"<%s>%s,%s(%s)" % (self.client.app_id, self.oauth_user.open_id, uuid.uuid4(), time.time())
        sha256 = hashlib.sha256()
        sha256.update(raw.encode('utf-8'))
        return base64.b64encode(sha256.digest()).decode("utf-8")

    def create_new_access_token(self):
        """
        创建新的Token
        :return:
        """
        token = Oauth2Model.Tokens()
        token.access_token = self.gen_access_token()
        token.refresh_token = self.gen_refresh_token()
        # Refresh Token的有效规则是建立在Access Token有效的基础上的
        # 当AccessToken失效后，RefreshToken自动失效
        token.expires_at = int(time.time()) + self.client.at_expires_time
        token.save()
        return token

    def gen_refresh_token(self):
        """
        计算Refresh Token
        :param client:
        :param user:
        :return:
        """
        raw = u"<%s>%s?%s(%s)" % (self.client.app_id, self.oauth_user.open_id, uuid.uuid4(), time.time())
        sha512 = hashlib.sha512()
        sha512.update(raw.encode('utf-8'))
        return base64.b64encode(sha512.digest()).decode("utf-8")

    def gen_authorize_code(self):
        """
        计算auth code
        :return:
        """
        code = u"<%s>%s-%s(%s)" % (self.client.app_id, uuid.uuid4(), self.oauth_user.open_id, time.time())
        sha1 = hashlib.sha1()
        sha1.update(code.encode('utf-8'))
        return sha1.hexdigest()

    def get_account_type(self, account):
        """
        获取用户类型
        :param account:
        :return:
        """
        if isinstance(account, EducationModel.EduAccount):
            return "education"
        elif isinstance(account, ContestModel.ContestAccount):
            return "contest"
        return "wejudge"

    def check_user_allow(self, throw=True):
        """
        检查用户是否允许授权
        :return:
        """
        if self.oauth_user.is_allow:
            return True
        else:
            if throw:
                raise Oauth2Error(40003)
            else:
                return False

    def check_access_token(self, access_token, throw=True):
        """
        检查Access Token
        :param access_token:
        :param throw:
        :return:
        """
        at = self.oauth_user.tokens.filter(access_token=access_token)
        if at.exists():
            at = at[0]
            if at.expires_at > int(time.time()):
                return at
            else:
                at.delete()

        if throw:
            raise Oauth2Error(40004)
        else:
            return False

    def check_app_secret(self, appsecret, throw=True):
        """
        检查Client 的 APP secret
        :param appsecret:
        :param throw:
        :return:
        """
        if appsecret == self.client.app_secret:
            return True

        if throw:
            raise Oauth2Error(40005)
        else:
            return False

    @staticmethod
    def oauth2_success(rel):
        rel.update({
            "errcode": 0,
            "errmsg": "OK"
        })
        return rel
