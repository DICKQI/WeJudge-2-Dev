# -*- coding: utf-8 -*-
# coding:utf-8


from celery import task
from .judge import judge_callback, tcmaker_callback
from wejudge.judger import JudgeSession, TCMakerSession
import apps.problem.models as ProblemModel

__author__ = 'lancelrq'

@task()
def judge(problem_id, status_id, vproblem_id=None):
    """
    判题入口
    :return:
    """
    session = JudgeSession(problem_id, status_id, options={
        "vproblem_id": vproblem_id,
        "strict_mode": True
    }, prefix='problem', model=ProblemModel.JudgeStatus)
    session.judge(judge_callback)
    return "FINISH"


@task()
def tcmaker(problem_id, status_id):
    """
    测试数据生成器入口
    :return:
    """
    session = TCMakerSession(problem_id, status_id, options={
        "strict_mode": True
    })
    session.judge(tcmaker_callback)
    return "FINISH"


