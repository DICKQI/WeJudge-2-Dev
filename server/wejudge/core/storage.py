# -*- coding: utf-8 -*-
# coding:utf-8
import os
import shutil
import os.path
__author__ = 'lancelrq'


class WeJudgeStorage(object):

    def __init__(self, root_dir, folder_name="", create_new=True):
        """
        初始化
        :param root_dir: 根目录
        :param folder_name: 子目录
        :param create_new: 是否新建目录
        :return:
        """
        if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
            raise OSError("%s NOT A VAILD DIR" % root_dir)
        # 绝对目录路径
        self.__folder_dir = (os.path.join(root_dir, folder_name))

        # 如果目标子目录不存在则新建
        if create_new and (not os.path.exists(self.__folder_dir)):
            os.mkdir(self.__folder_dir)

    def get_file_path(self, file_name):
        """
        返回文件/文件夹绝对路径
        :param file_name: 文件名
        :return:
        """
        try:
            return os.path.join(self.__folder_dir, file_name)
        except BaseException as ex:
            return ""

    def get_folder_path(self, folder_name):
        """
        返回文件夹绝对路径
        :param folder_name:
        :return:
        """
        return self.get_file_path(folder_name)

    def is_file(self, file_name):
        """
        判断是否为文件，如果不存在则返回False
        :param file_name: 文件名
        :return:
        """
        try:
            if self.exists(file_name):
                return os.path.isfile(self.get_file_path(file_name))
            return False
        except BaseException as ex:
            return False

    def is_folder(self, folder_name):
        """
        判断是否为文件夹，如果不存在则返回False
        :param folder_name:  文件夹名称
        :return:
        """
        try:
            if self.exists(folder_name):
                return os.path.isdir(self.get_file_path(folder_name))
            return False
        except BaseException as ex:
            return False

    def exists(self, file_name):
        """
        判断路径是否存在
        :param file_name: 文件名
        :return:
        """
        try:
            if os.path.exists(self.get_file_path(file_name)):             # 判断文件是否存在
                return True
            else:
                return False
        except BaseException as ex:
            return False

    def get_child_storage(self, child_folder_name, create_new=True):
        """返回子目录的存储访问类"""
        if not create_new and not self.is_folder(child_folder_name):
            raise OSError("Child folder not exists.")
        return WeJudgeStorage(self.__folder_dir, child_folder_name)

    def get_current_path(self):
        """
        返回当前目录位置
        :return:
        """
        return self.__folder_dir

    def clone_from_file(self, file_name, source_full_path):
        """
        将文件克隆进来
        :param file_name: 目标文件名
        :param source_full_path: 源文件完整地址
        :return:
        """
        try:
            if os.path.exists(source_full_path):
                shutil.copy(source_full_path, self.get_file_path(file_name))
                return True
            else:
                return False
        except BaseException as ex:
            return False

    def clone_to_file(self, file_name, dst_full_path):
        """
        将文件克隆出去
        :param file_name: 目标文件名
        :param dst_full_path: 源文件完整地址
        :return:
        """
        try:
            if self.exists(file_name):
                shutil.copy(self.get_file_path(file_name), dst_full_path)
                return True
            else:
                return False
        except BaseException as ex:
            return False

    def clone_to_dir(self, folder_name, dst_folder_path):
        """
        将子文件夹克隆到目标位置
        :param folder_name:
        :param dst_folder_path:
        :return:
        """
        try:
            if os.path.isdir(folder_name) and os.path.exists(dst_folder_path) and os.path.isdir(dst_folder_path):
                shutil.copytree(self.get_folder_path(folder_name), dst_folder_path)
                return True
            else:
                return False
        except BaseException as ex:
            return False

    def clone_from_dir(self, folder_name, source_folder_path):
        """
        从源文件夹克隆到目标位置
        :param folder_name:
        :param dst_folder_path:
        :return:
        """
        try:
            if os.path.isdir(folder_name) and os.path.exists(source_folder_path) and os.path.isdir(source_folder_path):
                shutil.copytree(source_folder_path, self.get_folder_path(folder_name))
                return True
            else:
                return False
        except BaseException as ex:
            return False

    def rename(self, file_name, new_name):
        """
        重命名
        :param file_name: 源文件
        :param new_name: 新文件名
        :return:
        """
        if self.exists(file_name):
            shutil.move(self.get_file_path(file_name), self.get_file_path(new_name))
            return True
        else:
            return False

    def delete(self, file_name):
        """
        删除文件/目录
        :param file_name: 文件名
        :return:
        """
        if not self.exists(file_name):
            return False
        file_path = self.get_file_path(file_name)
        try:
            if self.is_folder(file_name):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            return True
        except BaseException as e:
            return False

    def new_folder(self, folder_name):
        """
        新建文件夹（不推荐使用）
        :param folder_name: 文件夹名称
        :return:
        """
        if self.is_folder(folder_name):
            return False
        try:
            os.mkdir(self.get_file_path(folder_name))
            return True
        except BaseException as e:
            return False

    def open_file(self, file_name, mode='r'):
        """
        打开文件
        :param file_name: 文件名
        :param mode: 打开模式，默认是r
        :return:
        """
        file_path = self.get_file_path(file_name)
        try:
            fp = open(file_path, mode)
            return fp
        except BaseException as e:
            return None

    def get_files_list(self, path='', with_info=False, full_path=False):
        """
        读取文件列表
        :param path: 扫描子路径，不写则为当前文件夹
        :param with_info: 返回文件详细信息
        :param full_path: 返回完整路径
        :return:
        """
        if not self.is_folder(path):
            return []
        tpath = self.get_folder_path(path)
        lists = os.listdir(tpath)
        flist = []
        for item in lists:
            if os.path.isfile(os.path.join(tpath, item)):
                if full_path:
                    fp = os.path.join(tpath, item)
                else:
                    fp = item
                if with_info:
                    flist.append({
                        'file_name': fp,
                        'modify_time': os.path.getatime(os.path.join(tpath, item)),
                        'create_time': os.path.getctime(os.path.join(tpath, item)),
                        'size':  os.path.getsize(os.path.join(tpath, item))
                    })
                else:
                    flist.append(fp)
        return flist

    def get_dirs_list(self, path='', full_path=False):
        """
        返回目录
        :param path: 扫描子路径，不写则为当前文件夹
        :param full_path: 返回完整路径
        :return:
        """
        if not self.is_folder(path):
            return []
        tpath = self.get_folder_path(path)
        lists = os.listdir(tpath)
        flist = []
        for item in lists:
            if os.path.isdir(os.path.join(tpath, item)):
                if full_path:
                    flist.append(os.path.join(tpath, item))
                else:
                    flist.append(item)
        return flist

    def get_file_attribute(self, file_name):
        """
        获取文件属性
        :param file_name: 文件名
        :return:
        """
        if self.exists(file_name):
            fn_path = self.get_file_path(file_name)
            return {
                'modify_time': os.path.getatime(fn_path),
                'create_time': os.path.getctime(fn_path),
                'size':  os.path.getsize(fn_path)
            }
        else:
            return {}

    def get_file_size(self, file_name):
        """
        获取文件大小
        :param file_name:
        :return:
        """
        if self.exists(file_name):
            fn_path = self.get_file_path(file_name)
            return os.path.getsize(fn_path)
        else:
            return -1

    def get_dir_size(self, folder_name):
        """
        获取文件夹大小
        :param file_name:
        :return:
        """
        if self.exists(folder_name) and self.is_folder(folder_name):
            dir_path = self.get_file_path(folder_name)
            size = 0
            for root, subfolders, files in os.walk(dir_path):
                for filepath in files:
                    size += os.path.getsize(os.path.join(root, filepath))
            return size
        else:
            return -1