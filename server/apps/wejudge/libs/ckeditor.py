# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import os
import uuid
from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from wejudge.utils import tools
from PIL import Image as image


class CKEditorAPIController(WeJudgeControllerBase):

    def ckeditor_imgupload(self):
        """
        CKEditor 图片上传接口
        :return:
        """
        callback = self._request.GET.get('CKEditorFuncNum')

        if not self.login_check(False):
            self._context = "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '上传功能需要登录WeJudge主账户');</script>" % callback
            return

        files = self._request.FILES.get('upload')
        if files is None:
            return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '无文件上传');</script>" % callback

        if files.size > 5*1024*1024:
            return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '图片文件过大(限制在5MB内)');</script>" % callback

        type = files.content_type
        ext = None
        if (type == "image/pjpeg") or (type == "image/jpeg"):
            ext = '.jpg'
        elif (type == "image/png") or (type == "image/x-png"):
            ext = '.png'
        elif type == "image/gif":
            ext = '.gif'
        elif type == 'image/bmp':
            ext = '.bmp'

        if ext is None:
            return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '文件格式不正确（必须为.jpg/.gif/.bmp/.png文件）');</script>" % callback

        path = "%s%s" % (uuid.uuid4(), ext)
        file_name = os.path.join(system.WEJUDGE_STORAGE_ROOT.CKEDITOR_UPLOAD_IMAGE_DIR, path)
        destination = open(file_name, 'wb+')
        for chunk in files.chunks():
            destination.write(chunk)
        destination.close()

        if ext != ".gif":
            self._resize_img(ori_img=file_name, dst_img=file_name, dst_w=1280, dst_h=1280, save_q=80)

        return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'%s', '');</script>" % (callback, "/resource/imgupload/" + path)

    def ckeditor_fileupload(self):
        """
        CKEditor 文件上传接口
        :return:
        """
        callback = self._request.GET.get('CKEditorFuncNum')

        if not self.login_check(False):
            self._context = "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '上传功能需要登录WeJudge主账户');</script>" % callback
            return

        files = self._request.FILES.get('upload')
        if files is None:
            return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '无文件上传');</script>" % callback

        if files.size > 20*1024*1024:
            return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '附件文件过大(限制为20MB内)');</script>" % callback

        ftype = files.content_type

        ENABLED_TYPE = [
            "image/pjpeg", "image/jpeg", "image/png", "image/x-png", "image/gif", "image/bmp",
            "application/msword", "application/vnd.ms-excel", "application/vnd.ms-powerpoint", "application/pdf",
            "application/x-gzip", "application/zip", "text/plain",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ]

        # if ftype not in ENABLED_TYPE:
        #     return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'', '不被允许的文件格式：%s');console.log('%s')</script>" % (callback, ftype, ftype)

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CKEDITOR_UPLOAD_FILE_DIR, str(self.session.account.id))
        fname = "%s_%s" % (tools.gen_handle(), files.name)
        destination = storage.open_file(fname, 'wb+')
        for chunk in files.chunks():
            destination.write(chunk)
        destination.close()

        return "<script type=\"text/javascript\">window.parent.CKEDITOR.tools.callFunction(%s,'%s', 'ok');</script>" % (
            callback, storage.get_file_path(fname).replace(
                system.WEJUDGE_STORAGE_ROOT.CKEDITOR_UPLOAD_FILE_DIR, "/resource/fileupload/"
            )
        )

    # 等比例压缩图片
    def _resize_img(self, **args):
        args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q': 80}
        arg = {}
        for key in args_key:
            if key in args:
                arg[key] = args[key]

        im = image.open(arg['ori_img'])
        ori_w, ori_h = im.size
        widthRatio = heightRatio = None
        ratio = 1
        if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
            if arg['dst_w'] and ori_w > arg['dst_w']:
                widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
            if arg['dst_h'] and ori_h > arg['dst_h']:
                heightRatio = float(arg['dst_h']) / ori_h

            if widthRatio and heightRatio:
                if widthRatio < heightRatio:
                    ratio = widthRatio
                else:
                    ratio = heightRatio

            if widthRatio and not heightRatio:
                ratio = widthRatio
            if heightRatio and not widthRatio:
                ratio = heightRatio

            newWidth = int(ori_w * ratio)
            newHeight = int(ori_h * ratio)
        else:
            newWidth = ori_w
            newHeight = ori_h

        im.resize((newWidth,newHeight), image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])
