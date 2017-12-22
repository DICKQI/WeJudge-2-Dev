# -*- coding: utf-8 -*-
# coding:utf-8
import json

__author__ = 'lancelrq'


class WeJudgeResult(object):
    """
    WeJudge RESTful应答消息结构
    """

    def __init__(self, data=None, msg='', action=''):
        self.__msg = msg
        self.__data = data
        self.__action = action

    def dump(self):
        return json.dumps(self.to_dict())

    def to_dict(self):

        return {
            'WeJudgeError': False,
            'msg': self.__msg,
            'data': self.__data,
            'action': self.__action
        }