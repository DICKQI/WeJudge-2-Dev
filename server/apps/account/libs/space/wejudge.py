# -*- coding: utf-8 -*-
# coding:utf-8

import os
import json
import time
import datetime
from django.utils.timezone import now
from django.utils.cache import patch_cache_control
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.account.models as AccountModel
import apps.problem.models as ProblemModel
from django.db.models import Q
from django.conf import settings

__author__ = 'lancelrq'


# WeJudge主账户个人空间 控制类
class WeJudgeAccountSpace(WeJudgeControllerBase):

    def __init__(self, request, response, account_id):
        """
        初始化
        :param request: django request 对象
        :param response: django response 对象
        :return:
        """
        self.headimg_storage_dir = 'wejudge'
        self.account = None
        self.get_account(account_id)
        super(WeJudgeAccountSpace, self).__init__(request, response)

    # 获取用户的展示信息
    @WeJudgeControllerBase.login_validator
    def get_account_info(self):
        """
        获取用户的展示信息
        :return:
        """
        if self.account == self.session.account:
            its = [
                'id', 'username', 'nickname', 'realname', 'sex', 'headimg', 'email',
                'motto', 'create_time', 'last_login_time', 'wc_openid', 'email_validated',
                'permission_administrator', 'permission_publish_problem',
                'permission_create_problemset', 'permission_create_contest'
            ]
        else:
            its = [
                'id', 'username', 'nickname', 'realname', 'sex', 'headimg',
                'motto', 'create_time', 'last_login_time', 'wc_openid',
                'permission_administrator', 'permission_publish_problem',
                'permission_create_problemset', 'permission_create_contest'
            ]
        account_info = self.account.json(items=its)
        pv = {
            'total': self.account.accountproblemvisited_set.count(),
            'solved': self.account.accountproblemvisited_set.filter(accepted__gt=0).count()
        }
        account_info['problem_visited'] = pv
        return account_info

    # 读取用户的做题信息
    @WeJudgeControllerBase.login_validator
    def get_user_problem_solutions(self):
        """
        读取用户的做题信息
        :return:
        """
        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        solutions = ProblemModel.ProblemSetSolution.objects.filter(author=self.account)

        @WeJudgePagination(
            model_object=self._solutions_filter(solutions),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_solutions_item(sol):
            view_item = sol.json(items=[
                'id', 'problem', 'problem__id', 'problem__title', 'virtual_problem', 'virtual_problem_id',
                'problemset', 'problemset__id', 'problemset__title', 'accepted', 'submission', 'penalty',
                'best_memory', 'best_time', 'best_code_size'
            ])
            return view_item

        result = proc_solutions_item()
        return result

    # 保存用户信息
    @WeJudgeControllerBase.login_validator
    def save_account_infos(self):
        """
        保存用户信息
        :return:
        """
        self.check_self_account()

        parser = ParamsParser(self._request)
        username = parser.get_str('username', require=True, method="POST", errcode=1101)
        password = parser.get_str('password', require=True, method="POST", errcode=1104)
        newpassword = parser.get_str('newpassword', "", method="POST")
        renewpassword = parser.get_str('renewpassword', "", method="POST")
        nickname = parser.get_str('nickname', require=True, method="POST", errcode=1102)
        realname = parser.get_str('realname', '', method="POST")
        motto = parser.get_str('motto', '', method="POST")
        email = parser.get_str('email', require=True, method="POST", errcode=1106)
        sex = parser.get_int('sex', -1, method="POST")

        if tools.gen_passwd(password) != self.account.password:
            raise WeJudgeError(1104)

        if self.account.username != username:
            uca = AccountModel.Account.objects.filter(username=username)
            if uca.exists() and uca[0] != self.account:
                raise WeJudgeError(1103)

        if self.account.nickname != nickname:
            uca = AccountModel.Account.objects.filter(nickname=nickname)
            if uca.exists() and uca[0] != self.account:
                raise WeJudgeError(1108)

        if newpassword.strip() != "":
            if newpassword == renewpassword:
                self.account.password = tools.gen_passwd(newpassword)
            else:
                raise WeJudgeError(1105)

        self.account.username = username
        self.account.nickname = nickname
        self.account.realname = realname
        self.account.sex = sex
        self.account.email = email
        self.account.motto = motto

        self.account.save()

    # 保存用户头像
    def save_account_avatar(self):
        """
        保存用户头像
        :return:
        """
        self.check_self_account()

        parser = ParamsParser(self._request)
        headimg = parser.get_file('headimg', type=[
            'image/pjpeg', 'image/jpeg', 'image/png', 'image/x-png'
        ], max_size=2*1024*1024, require=True)
        x = parser.get_float('x', min=0, require=True, method='POST')
        y = parser.get_float('y', min=0, require=True, method='POST')
        w = parser.get_float('w', min=0, require=True, method='POST')
        h = parser.get_float('h', min=0, require=True, method='POST')

        filename = str(self.account.id)

        flag, msg = self._save_avatar(headimg, filename, x, y, w, h)
        if flag:
            self.account.headimg = msg
            self.account.save()
            return flag
        else:
            raise WeJudgeError(msg)

    # 检查时候是否是自我账号
    def check_self_account(self, throw=True):
        """
        检查时候是否是自我账号
        :param throw: 错误是否抛出
        :return:
        """
        if self.session.account != self.account:
            if throw:
                raise WeJudgeError(1100)
            else:
                return False
        return True

    # 检查时候是否是自我账号（访问器
    @staticmethod
    def self_account_validator(func):
        """
        检查时候是否是自我账号
        :return:
        """

        def wrapper(*args, **kwargs):
            self = args[0]
            self.check_self_account()
            return func(*args, **kwargs)

        return wrapper

    # 读取账号
    def get_account(self, account_id):
        """
        获取账户信息
        :return:
        """
        account = AccountModel.Account.objects.filter(id=account_id)
        if account.exists():
            self.account = account[0]
        else:
            raise WeJudgeError(1000)

    # 读取账号（静态）
    @staticmethod
    def get_account_static(account_id):
        """
        读取账号
        :return:
        """
        account = AccountModel.Account.objects.filter(id=account_id)
        if account.exists():
            return account[0]
        else:
            return None

    # 读取头像信息（静态）
    @staticmethod
    def get_account_avator(account):
        """
        读取头像信息（静态）
        :return:
        """
        headimg = None
        sex = -1

        if account is not None:
            sex = account.sex
            if account.headimg is None or account.headimg.strip() == "":
                if (hasattr(account, 'master')) \
                        and (account.master is not None) \
                        and (account.master.headimg is not None) \
                        and (account.master.headimg.strip() != ""):
                    headimg = account.master.headimg
            else:
                headimg = account.headimg

        if headimg is None:
            if sex == 0:
                headimg = os.path.join(settings.BASE_DIR, './static/images/avator/girl.png')
            else:
                headimg = os.path.join(settings.BASE_DIR, './static/images/avator/boy.png')
            fp = open(headimg, 'rb')
        else:
            storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.USER_HEADIMAGE_DIR, '')
            fp = storage.open_file(headimg, 'rb')
            headimg = storage.get_file_path(headimg)

        if '.png' in headimg:
            mime = "image/png"
        else:
            mime = "image/jpeg"

        def read_file(buf_size=8192):  # 大文件下载，设定缓存大小
            while True:  # 循环读取
                c = fp.read(buf_size)
                if c:
                    yield c
                else:
                    break
            fp.close()

        response = HttpResponse(
            read_file(),
            content_type=str(mime)
        )  # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
        response['Content-Length'] = os.path.getsize(headimg)
        patch_cache_control(response, max_age=60 * 10)
        return response

    # 解决方案过滤器
    def _solutions_filter(self, solist):
        """
        解决方案过滤器
        :param solist:
        :return:
        """

        parser = ParamsParser(self._request)
        keyword = parser.get_str('keyword', '')             # 关键字(problem id）

        if (keyword is not None) and (keyword.strip() != ""):
            if tools.is_numeric(keyword):
                solist = solist.filter(problem__id__contains=keyword)
        return solist.order_by('-id')

    # 保存头像
    def _save_avatar(self, headimg, filename, x, y, w, h):
        """
        保存头像
        :param headimg: Django File Object
        :param filename: 保存文件名，系统将自动附上扩展名
        :return:
        """
        ftype = headimg.content_type
        ext = None
        if (ftype == "image/pjpeg") or (ftype == "image/jpeg"):
            ext = '.jpg'
        elif (ftype == "image/png") or (ftype == "image/x-png"):
            ext = '.png'
        if ext is None:
            return False, 1107

        path = "%s%s" % (filename, ext)
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.USER_HEADIMAGE_DIR, self.headimg_storage_dir)
        destination = storage.open_file(path, 'wb+')
        for chunk in headimg.chunks():
            destination.write(chunk)
        destination.close()

        if (x == 0) or (y == 0) or (w == 0) or (h == 0):
            return False, 1

        from PIL import Image

        oim = Image.open(storage.get_file_path(path))
        im = oim.crop((x, y, x + w, y + h))
        ori_w, ori_h = im.size
        width_ratio = height_ratio = None
        dst_w = dst_h = 180
        ratio = 1
        if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
            if dst_w and ori_w > dst_w:
                width_ratio = float(dst_w) / ori_w
            if dst_h and ori_h > dst_h:
                height_ratio = float(dst_h) / ori_h

            if width_ratio and height_ratio:
                if width_ratio < height_ratio:
                    ratio = width_ratio
                else:
                    ratio = height_ratio

            if width_ratio and not height_ratio:
                ratio = width_ratio
            if height_ratio and not width_ratio:
                ratio = height_ratio

            new_width = int(ori_w * ratio)
            new_height = int(ori_h * ratio)

        else:
            new_width = ori_w
            new_height = ori_h

        im.resize((new_width, new_height), Image.ANTIALIAS).save(storage.get_file_path(path), quality=95)

        return True, storage.get_file_path(path).replace(system.WEJUDGE_STORAGE_ROOT.USER_HEADIMAGE_DIR + '/', '')
