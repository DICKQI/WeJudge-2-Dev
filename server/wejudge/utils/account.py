# -*- coding: utf-8 -*-
# coding:utf-8
import json
from django.db import models
__author__ = 'lancelrq'


# WeJudge 用户主类
class WeJudgeAccount(object):
    """
    WeJudge 账户管理器
    """

    def __new__(cls, data):
        """
        初始化用户数据
        :param data: Session恢复信息或者Account的ORM对象
        """

        import apps.account.models as AccountModel

        # 如果data是AccountBase类派生的ORM对象
        if isinstance(data, AccountModel.AccountBase):
            session_data = None
            entity = data
        else:
            if isinstance(data, dict):
                session_data = data
            else:
                # 载入会话信息
                try:
                    session_data = json.loads(data)
                except BaseException as e:
                    return None

            user_id = session_data.get('user_id', '')
            entity = WeJudgeAccount.get_user_by_id(user_id=user_id)

            if entity is None:
                return None

        cls.entity = entity
        return object.__new__(cls)

    # 返回session化的存储信息标志
    def dump_session_data(self):
        """
        返回session化的存储信息标志
        :return:
        """
        data = {
            'user_id': self.entity.id,
            'username': self.entity.username
        }

        return data

    # 获取用户信息
    @staticmethod
    def get_user_by_id(*args, **kwargs):
        """
        获取用户信息
        :return:
        """
        user_id = kwargs.get('user_id', '0')

        import apps.account.models as AccountModel

        entity = AccountModel.Account.objects.filter(id=user_id)

        if entity.exists():
            return entity[0]
        else:
            return None


class WeJudgeEducationAccount(WeJudgeAccount):
    """
    WeJudge EduAccount 类
    """

    def __new__(cls, data, school_id):

        import apps.education.models as EducationModel

        if isinstance(data, EducationModel.EduAccount):
            entity = data
        else:
            if isinstance(data, dict):
                session_data = data
            else:
                session_data = None
                try:
                    session_data = json.loads(data)
                except:
                    return None

            user_id = session_data.get('user_id', '0')

            entity = WeJudgeEducationAccount.get_user_by_id(user_id=user_id, school_id=school_id)

            if entity is None:
                return None

        cls.entity = entity
        return WeJudgeAccount.__new__(cls, entity)

    def __init__(self, data, school_id):
        super(WeJudgeAccount, self).__init__()

    # 获取用户信息
    @staticmethod
    def get_user_by_id(*args, **kwargs):
        """
        获取用户信息
        :return:
        """

        school_id = kwargs.get('school_id', '0')
        user_id = kwargs.get('user_id', '0')

        import apps.education.models as EducationModel

        entity = EducationModel.EduAccount.objects.filter(school_id=school_id, id=user_id)

        if entity.exists():
            return entity[0]
        else:
            return None


class WeJudgeContestAccount(WeJudgeAccount):
    """
    WeJudge 比赛账户管理器
    """

    def __new__(cls, data, contest_id):
        """
        初始化
        :param data:
        :param contest_id:
        :return:
        """

        import apps.contest.models as ContestModel

        if isinstance(data, ContestModel.ContestAccount):
            entity = data
        else:
            if isinstance(data, dict):
                session_data = data
            else:
                session_data = None
                try:
                    session_data = json.loads(data)
                except:
                    return None

            user_id = session_data.get('user_id', '0')

            entity = WeJudgeContestAccount.get_user_by_id(user_id=user_id, contest_id=contest_id)

            if entity is None:
                return None

        cls.entity = entity
        return WeJudgeAccount.__new__(cls, entity)

    def __init__(self, data, contest_id):
        super(WeJudgeAccount, self).__init__()

    # 获取用户信息
    @staticmethod
    def get_user_by_id(*args, **kwargs):
        """
        获取用户信息
        :return:
        """

        contest_id = kwargs.get('contest_id', '0')
        user_id = kwargs.get('user_id', '0')

        import apps.contest.models as ContestModel

        entity = ContestModel.ContestAccount.objects.filter(contest_id=contest_id, id=user_id)

        if entity.exists():
            return entity[0]
        else:
            return None