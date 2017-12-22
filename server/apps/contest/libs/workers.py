# -*- coding: utf-8 -*-
# coding:utf-8

from wejudge.core import *
from wejudge.judger import JudgeSession
from wejudge.const import system
from celery import task
import apps.problem.models as ProblemModel
import apps.contest.models as ContestModel

from .cross_check import ContestCodeCrossCheck
from .judge import contest_judge_callback, ContestJudgeProcesser

__author__ = 'lancelrq'


@task()
def cross_check(contest_id, status_id):
    c = ContestCodeCrossCheck(contest_id, status_id)
    c.text_check()
    return "FINISH"

@task()
def contest_judge(problem_id, status_id, contest_id, strict_mode=True):
    """
    判题入口
    :return:
    """
    session = JudgeSession(problem_id, status_id, options={
        "contest_id": contest_id,
        "strict_mode": strict_mode
    }, prefix='contest', model=ContestModel.JudgeStatus)
    session.judge(contest_judge_callback)
    return "FINISH"

@task()
def contest_refresh_all_data(contest_id):
    """
    CELERY 比赛数据重算
    :param contest_id:
    :return:
    """

    contest = ContestModel.Contest.objects.filter(id=contest_id)
    if not contest.exists():
        return 'Contest Not Exists.'
    contest = contest[0]

    # 先把题目列表搞出来，在因为对于每个cjp对象，contest和problem是固定的
    # 然后把账户表都弄出来，按每个用户遍历(role==0，其他不用管)
    # 最后再去搜他们solution

    # 理论上来看，这种处理方式，引起的sql操作是最少的。
    # 假设 有题目n题，用户m个，由于做了缓存，也就是循环而已，都是已经读取到内存的记录
    # 也就仅仅第三层要做n * m次solution表的查询。
    # 如果是直接查询solution整个表出来，假设由p条记录，
    # 每一次sol表遍历操作都必须创建ContestJudgeProcesser对象，查询用户信息，会引起大量重复的查询，
    # 那么就会引起 p^(n^m) 次sql查询，这个贼不划算好吗！
    # 如果将来谁维护这段代码的时候，能好好想想我现在为什么要这样做。
    # P.S: 牺牲内存为代价减少查询的复杂度！因为一次性把所有题目和账户信息加载到内存了。

    plist = contest.problems.all()
    accounts_list = ContestModel.ContestAccount.objects.filter(contest=contest, role=0)

    for contest_problem in plist:

        cjp = ContestJudgeProcesser(contest, contest_problem)
        cjp.proc_problem()

        for account in accounts_list:
            # 重算该用户所有的sol
            cjp.proc_solution(account)

        for account in accounts_list:
            # 重算该用户的排行
            cjp.proc_rank(account)

    return "FINISH"


@task
def contest_ranklist_snapshot(contest_id, filename):
    """
    排行榜快照生成
    :param contest_id:
    :param filename:
    :return:
    """

    contest = ContestModel.Contest.objects.filter(id=contest_id)
    if not contest.exists():
        return 'Contest Not Exists.'
    contest = contest[0]

    storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CONTEST_STORAGE, str(contest_id))
    if storage.exists("snapshot.lock"):
        return "LOCKED"

    storage.open_file("snapshot.lock", 'w+').close()
    try:
        import json
        from .contest import ContestController
        data = json.dumps(ContestController.get_ranklist_data(contest))
        fp = storage.open_file(filename, 'w+')
        fp.write(data)
        fp.close()
    except Exception as ex:
        print("Error: %s" % repr(ex))
    finally:
        storage.delete("snapshot.lock")
