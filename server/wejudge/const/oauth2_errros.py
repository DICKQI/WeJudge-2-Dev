# -*- coding: utf-8 -*-
# coding:utf-8

__author__d = 'lancelrq'

ACTION_GOBACK = ['']
oauth2_errros = dict()


def generator(code, message, httpcode=200):
    oauth2_errros[code] = [message, httpcode]


generator(0, '无错误')
generator(1, '系统调用接口参数错误')
generator(2, '系统调用接口参数不符合约束')
generator(40000, '错误的APP ID. Invalid APP ID.')
generator(40001, '错误的Open ID. Invalid Open ID.')
generator(40002, '错误的授权码应答方式. Invalid Response Type.')
generator(40003, '用户未允许授权此应用. Authorization Forbidden.')
generator(40004, 'Access Token不存在或者失效. Invalid Access Token')
generator(40005, '错误的APP Secert. Invalid App Secert.')
generator(40006, '错误的授权方式. Invalid Grant Type.')
generator(40007, '错误或失效的授权Code. Invalid Authorize Code.')
generator(40008, '错误或失效的授权Refresh Token. Invalid Refresh Token.')
generator(40009, '请先登录账号再使用. Please Login First.')
generator(40010, '回调页面地址错误. Redirect URL No Match.')
