# -*- coding: utf-8 -*-
# coding:utf-8
import re
import time
import subprocess
__author__ = 'lancelrq'


def _log(msg):
    body = "[%s] %s" % (time.strftime("%m-%d %H:%M:%S"), msg)
    print(body)


def syscall(cmd):
    """
    系统调用
    :param cmd: 系统调用的命令行
    :return:
    """
    try:
        ret = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        if hasattr(ret, "decode"):
            return 0, ret.decode("utf-8")
        else:
            return 0, ret
    except subprocess.CalledProcessError as ex:
        ret = ex.stdout
        if hasattr(ret, "decode"):
            ret = ret.decode("utf-8")
        return ex.returncode, ret


def compiler(code_files, target_path, compiler_cmd):
    """
    编译代码的系统调用
    :param code_files: 待编译的源代码文件列表
    :param target_path: 编译目标
    :param compiler_cmd: 编译指令
    :return:
    """
    code_file_str = " ".join(code_files)

    target_cmd = compiler_cmd % (code_file_str, target_path)
    print(target_cmd)

    # 运行编译并截取编译器返回的数据
    exitcode, output = syscall(target_cmd)

    # 判断是否正确编译
    if exitcode != 0:
        return False, output

    return True, ''


def get_java_class_name(java_source_code):
    """
    自动解析java的类名字
    :param java_source_code:
    :return:
    """
    try:
        regex = re.compile("public class ([A-Za-z0-9_$]+)")
        result = regex.search(java_source_code)
        if result is None:
            return False
        else:
            return result.group(1)
    except:
        return False