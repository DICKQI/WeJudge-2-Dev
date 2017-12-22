# -*- coding: utf-8 -*-
# coding:utf-8

import logging
from .account import WeJudgeAccount, WeJudgeEducationAccount, WeJudgeContestAccount
from .session import WeJudgeSession, WeJudgeEducationSession, WeJudgeContestSession
from .oauth2_session import WeJudgeOauth2Session, WeJudgeEducationOauth2Session
from .pagination import WeJudgePagination
from .params import ParamsParser
from .controller_base import WeJudgeControllerBase

__author__ = 'lancelrq'


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \n%(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='/data/log/debug.log',
    filemode='a'
 )

__all__ = [
    'WeJudgeAccount', 'WeJudgeEducationAccount', 'WeJudgeSession',
    'WeJudgePagination', 'ParamsParser', "WeJudgeControllerBase",
    'logging', 'WeJudgeContestAccount', 'WeJudgeContestSession'
    ,'WeJudgeEducationSession', 'WeJudgeOauth2Session', 'WeJudgeEducationOauth2Session'
]

