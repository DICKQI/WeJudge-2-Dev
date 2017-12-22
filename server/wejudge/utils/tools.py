# -*- coding: utf-8 -*-
# coding:utf-8
import uuid
import hashlib
import time
__author__ = 'lancelrq'


# 唯一标识符
def uuid1():
    rel = uuid.uuid1()
    return str(rel)


# 唯一标识符
def uuid4():
    rel = uuid.uuid4()
    return str(rel)


# 数字判断
def is_numeric(val):
    try:
        int(val)
        return True
    except:
        return False


# 浮点判断
def is_float(val):
    try:
        float(val)
        return True
    except:
        return False


# 检查混合存储的权限
def check_privilege(target, mixed, allow_all=False):
    """
    检查混合存储的权限
    :param target:
    :param mixed:
    :param allow_all: 当target为0的时候视作是All，返回True
    :return:
    """
    if target == 0:
        if allow_all:
            return True
        else:
            return False
    if mixed == 0:
        return False
    return (target & mixed) > 0


# 密码密文生成器
def gen_passwd(pwd):
    """
    密码密文生成器(静态)
    算法: sha256($salt.md5($pwd))
    :param pwd: 密码明文
    :return:
    """
    from wejudge.const import system
    try:
        pwd = pwd.encode("utf-8")
        md5 = hashlib.md5()
        md5.update(pwd)
        pwd = md5.hexdigest()       # 小写
        pwd = u'%s%s' % (system.WEJUDGE_ACCOUNT_PASSWORD_SALT, pwd)
        pwd = pwd.encode("utf-8")
        sha256 = hashlib.sha256()
        sha256.update(pwd)
        pwd = sha256.hexdigest()    # 小写
        return pwd
    except Exception as ex:
        print(ex)
        return ''


# Handle生成器（16位）
def gen_handle():
    """
    Handle生成器（16位）
    :return:
    """
    rel = str(uuid.uuid4())
    rel = rel.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(rel)
    return md5.hexdigest()[8:24]


# 登录令牌生成器(静态)
def create_login_token(username, passwd):
    """
    登录令牌生成器(静态)
    :param username: 用户名
    :param passwd: 密码
    :return:
    """
    from wejudge.const import system
    import uuid

    token = '%s.%s.%s.%s' % (username, passwd, str(time.time()), str(uuid.uuid4()))
    md5 = hashlib.md5()
    md5.update(token.encode("utf-8"))
    token = md5.hexdigest()
    token = '%s%s' % (token, system.WEJUDGE_ACCOUNT_PASSWORD_SALT)
    sha256 = hashlib.sha256()
    sha256.update(token.encode("utf-8"))
    token = sha256.hexdigest()
    return token


# 面包屑导航处理程序
def gen_navgation(navlist):
    """
    面包屑导航处理程序
    :param navlist:
    :return:
    """
    from django.shortcuts import reverse
    out_navlist = []

    i = 0
    length = len(navlist)
    for navitem in navlist:
        if navitem is None:
            continue
        i += 1
        if i == length:
            out_navlist.append([navitem[0], ])
        else:
            lv = len(navitem)
            if lv == 1:
                out_navlist.append([navitem[0], ])
            elif lv == 2:
                out_navlist.append([navitem[0], reverse(navitem[1])])
            elif lv == 3:
                out_navlist.append([navitem[0], reverse(navitem[1], args=navitem[2])])
            elif lv == 4:
                out_navlist.append([navitem[0], "%s?%s" % (reverse(navitem[1], args=navitem[2]), navitem[3])])

    return out_navlist


# 清除UTF-8的bom
def clear_bom(td_stor, fn):
    fp = td_stor.open_file(fn, 'rb')
    if "\xef\xbb\xbf" == fp.read(3):
        contents = fp.read()
        fp.close()
        fp = td_stor.open_file(fn, 'wb')
        fp.write(contents)
        fp.close()
        return
    fp.close()


# 过期检查（基于时间戳）
def check_timestamp_passed(start_time=0, end_time=0):
    """
    过期检查（基于时间戳）
    :param start_time:开始时间
    :param end_time:结束时间
    :return:
    """
    now_time = time.time()
    if now_time > end_time:
        return 1, now_time - end_time       # 已结束，返回已过去多少时间
    elif now_time < start_time:
        return -1, start_time - now_time    # 未开始，返回距离开始还剩
    return 0, end_time - now_time           # 运行中，返回剩余时间


# 过期检查（基于DateTime）
def check_time_passed(start_time, end_time):
    """
    过期检查（基于DateTime）
    :param start_time:
    :param end_time:
    :return:
    """
    from django.utils.timezone import now
    now_time = now()
    if now_time > end_time:
        return 1, now_time - end_time  # 已结束，返回已过去多少时间
    elif now_time < start_time:
        return -1, start_time - now_time  # 未开始，返回距离开始还剩

    return 0, end_time - now_time  # 运行中，返回剩余时间


# 题目标号转换系统（string -> num)
def char_to_index(keyword):

    index = 0
    keyword = keyword.lower()
    charlist = [chr(x+97) for x in range(26)]
    for s in keyword:
        if s not in charlist:
            return 0
        index *= 26
        index += (ord(s) - 97) + 1
    return index


# 题目标号转换系统（num -> string)
def gen_problem_index(value):
    try:
        v = int(value)
        outstr = ""
        while v > 0:
            if v % 26 != 0:
                outstr = chr(v % 26 + 64) + outstr
            else:
                outstr = 'Z' + outstr
            if v % 26 == 0:
                v -= 1
            v //= 26

        return outstr
    except:
        return "NaN"


# 生成随机密码，易于识别的（小写）
def gen_random_pwd(randomlength):
    """
    生成随机密码，易于识别的（小写）
    :param randomlength:
    :return:
    """
    from random import Random
    rstr = ''
    chars = 'ABCDEFGHJKMQPRTWXY2346789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        rstr += chars[random.randint(0, length)]
    return rstr


# 会话SHA512签名
def token_hmac_sha512_singature(body):
    from wejudge.const import system
    raw = "%s|%s|%s" % (body, system.WEJUDGE_ACCOUNT_PASSWORD_SALT, system.WEJUDGE_COOKIE_HMAC_SALT)
    return hashlib.sha512(raw.encode('utf-8')).hexdigest()
