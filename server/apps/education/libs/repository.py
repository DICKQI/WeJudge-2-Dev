# -*- coding: utf-8 -*-
# coding:utf-8

import os
import os.path
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.education.models as EducationModel
from .base import EducationBaseController

__author__ = 'lancelrq'


class EducationRepositoryController(EducationBaseController):

    def __init__(self, request, response, sid):
        super(EducationRepositoryController, self).__init__(request, response, sid)

    # 按照不同的用户身份，取得仓库列表
    def get_repositories_list(self):
        """
        按照不同的用户身份，取得仓库列表
        :return:
        """
        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', 40)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)
        only_me = parser.get_boolean('only_me', False)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        if self.session.is_logined():
            account = self.session.account
            if account.role < 2 and self.course is not None:
                repositories_list = self.course.repositories.all()
            else:
                if only_me:
                    repositories_list = EducationModel.Repository.objects.filter(school=self.school, author=account)
                else:
                    repositories_list = EducationModel.Repository.objects.filter(school=self.school, public_level__gte=1)
        else:
            if self.course is not None:
                raise WeJudgeError(3010)
            repositories_list = EducationModel.Repository.objects.filter(school=self.school, public_level=2)

        @WeJudgePagination(
            model_object=repositories_list.order_by("-id"),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 40),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_item(repository):
            repo = repository.json(items=[
                'id', 'title', 'author', 'author__id', 'author__nickname',
                'author__realname', 'public_level', 'cur_size',
            ])
            if self.course is not None:
                if self.course.repositories.filter(id=repository.id).exists():
                    repo['enabled'] = True
                else:
                    repo['enabled'] = False

            return repo

        view = proc_item()
        return view

    # 取得仓库信息
    def get_repository(self, rid):
        """
        取得仓库信息
        :param rid: Repository Id
        :return:
        """
        repo = EducationModel.Repository.objects.filter(school=self.school, id=rid)
        if repo.exists():
            self.repository = repo[0]
        else:
            raise WeJudgeError(3400)

    # 获取文件夹列表树（jstree格式)
    @EducationBaseController.check_repo_visit_validator(manager=False)
    def get_folders_tree(self):
        """
        获取文件夹列表树（jstree格式)
        :return:
        """
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.REPOSITORY_ROOT_DIR, str(self.repository.id))

        data = []

        path = self.get_path('id')

        if storage.is_folder(path):
            # 读取子文件夹
            clist = storage.get_dirs_list(path)
            for folder in clist:
                ch_path = os.path.join(path, folder)
                data.append({
                    "id": ch_path,
                    "text": folder,
                    "children": len(storage.get_dirs_list(ch_path)) > 0
                })
        if path == './':
            data = [{
                "id": "./",
                "text": "根目录",
                "children": data,
                "state": {
                    "opened": True,
                    "selected": True
                }
            }]

        return data

    # 取得仓库内的文件及文件夹信息
    @EducationBaseController.check_repo_visit_validator(manager=False)
    def get_files_map(self):
        """
        取得仓库内的文件及文件夹信息
        :param path: 位置
        :return:
        """
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.REPOSITORY_ROOT_DIR, str(self.repository.id))

        path = self.get_path()

        if not storage.is_folder(path):
            raise WeJudgeError(3450)
        files = storage.get_files_list(path, with_info=True)
        return {
            "data": [file for file in files]
        }

    # 新建文件夹
    @EducationBaseController.check_repo_visit_validator(manager=True)
    def repo_new_folder(self):
        """
        新建文件夹
        :return:
        """
        parser = ParamsParser(self._request)
        folder_name = parser.get_str('folder_name', '新文件夹', method="POST")

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.REPOSITORY_ROOT_DIR, str(self.repository.id))

        path = self.get_path()

        if not storage.is_folder(path):
            raise WeJudgeError(3450)

        # 切换到路径下
        nstorage = storage.get_child_storage(path)
        # 新建文件夹
        nstorage.new_folder(folder_name)

        return True

    # 上传文件
    @EducationBaseController.check_repo_visit_validator(manager=True)
    def repo_upload_file(self):
        """
        上传文件
        :return:
        """
        parser = ParamsParser(self._request)

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.REPOSITORY_ROOT_DIR, str(self.repository.id))

        path = self.get_path()

        if not storage.is_folder(path):
            raise WeJudgeError(3450)

        file = parser.get_file("uploadFile", require=True, max_size=1024*1024*1024)
        file_name = file.name

        # 切换到路径下
        nstorage = storage.get_child_storage(path)
        # 打开文件
        fp = nstorage.open_file(file_name, 'wb+')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        self.repository.cur_size = storage.get_dir_size('')
        self.repository.save()

        return

    # 删除文件/文件夹
    @EducationBaseController.check_repo_visit_validator(manager=True)
    def repo_delete(self):
        """
        删除文件/文件夹
        :return:
        """

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.REPOSITORY_ROOT_DIR, str(self.repository.id))

        path = self.get_path()

        if not storage.exists(path):
            raise WeJudgeError(3451)

        target_path = storage.get_file_path(path)
        # 根目录判定
        if target_path == storage.get_current_path():
            raise WeJudgeError(3453)

        storage.delete(path)

        self.repository.cur_size = storage.get_dir_size('')
        self.repository.save()

        return "./" + os.path.dirname(target_path).replace(storage.get_current_path(), "")

    # 增加或更改仓库信息(这个不要注册权限检查器啊，内部检查了）
    def edit_repo(self):
        """
        增加或更改仓库信息
        :return:
        """
        parser = ParamsParser(self._request)
        title = parser.get_str("title", require=True, method="POST", errcode=3403)
        public_level = parser.get_int("public_level", min=0, max=2, require=True, method="POST")

        if self.repository is None:
            if not self.session.is_logined() or self.session.account.role < 2:
                raise WeJudgeError(3402)
            self.repository = EducationModel.Repository()
            self.repository.school = self.school
            self.repository.author = self.session.account
        else:
            self.check_repo_visit_privilege(manager=True)

        self.repository.title = title
        self.repository.public_level = public_level

        self.repository.save()

    @EducationBaseController.check_repo_visit_validator(manager=True)
    def delete_repo(self):
        """
        删除仓库
        :return:
        """
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.REPOSITORY_ROOT_DIR, str(self.repository.id))
        storage.delete('./')
        self.repository.delete()

    # 获取并处理path
    def get_path(self, key='path'):
        """
        获取并处理path
        :return:
        """
        parser = ParamsParser(self._request)
        path = parser.get_str(key, '')

        if path == "#" or path == "/" or path.strip() == '':
            path = "./"

        if path[:1] == "/":
            path = "." + path

        if '../' in path:
            raise WeJudgeError(3454)

        return path

