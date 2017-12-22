# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.judger import JudgeSession
from wejudge.const import system
from celery import task
import apps.problem.models as ProblemModel
import apps.education.models as EducationModel

from .judge import asgn_judge_callback
from .judge import AsgnJudgeProcesser

__author__ = 'lancelrq'


@task()
def asgn_judge(problem_id, status_id, asgn_id, strict_mode=False):
    """
    判题入口
    :return:
    """
    session = JudgeSession(problem_id, status_id, options={
        "asgn_id": asgn_id,
        "strict_mode": strict_mode
    }, prefix='education', model=EducationModel.JudgeStatus)
    session.judge(asgn_judge_callback)
    return "FINISH"


@task()
def refresh_asgn_datas(asgn_id):
    """
    重算作业数据
    :param asgn_id:
    :return:
    """
    asgn = EducationModel.Asgn.objects.filter(id=asgn_id)
    if not asgn.exists():
        return 'Asgn Not Exists.'
    asgn = asgn[0]

    plist = asgn.problems.all()
    reports_list = EducationModel.AsgnReport.objects.filter(asgn=asgn)

    # 先更新题目数据
    for asgn_problem in plist:

        ajp = AsgnJudgeProcesser(asgn, asgn_problem)
        ajp.proc_problem()

        for report in reports_list:
            # 重算该用户所有的sol
            ajp.proc_solution(report)

        # 再更新报告信息
        for report in reports_list:
            ajp.proc_report(report)

    return "FINISH"

