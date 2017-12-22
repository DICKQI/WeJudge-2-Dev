# -*- coding: utf-8 -*-
# coding:utf-8

from urllib import request
from django.shortcuts import reverse
from django.conf import settings
import apps.problem.models as ProblemModel

__author__ = 'lancelrq'


def judge_callback(session, result):
    """
    判题回调
    :param session: Judge Session
    :param result:
    :return:
    """

    # 注意，这里的status.problem是PModel.Problem
    import logging
    status = ProblemModel.JudgeStatus.objects.filter(id=result.status_id)
    if not status.exists():
        return "ERROR STATUS NOT EXISTS"
    status = status[0]
    status.exe_mem = result.memused
    status.exe_time = result.timeused
    status.flag = result.exitcode
    status.result = result.dump_json()
    status.save()

    # 单题目统计
    apv = ProblemModel.AccountProblemVisited.objects.filter(author=status.author, problem=status.problem)
    if apv.exists():
        apv = apv[0]
        apv.accepted = ProblemModel.JudgeStatus.objects.filter(problem=status.problem, author=status.author, flag=0).count()
        apv.save()

    # （题目集）解决情况统计
    if session.options.get('vproblem_id', None) is not None:
        virtual_problem = ProblemModel.ProblemSetItem.objects.filter(id=session.options.get('vproblem_id'))
        if virtual_problem.exists():
            virtual_problem = virtual_problem[0]
            virtual_problem.accepted = ProblemModel.JudgeStatus.objects.filter(
                virtual_problem=virtual_problem, flag=0
            ).count()
            virtual_problem.save()
            sol = ProblemModel.ProblemSetSolution.objects.filter(
                author=status.author, virtual_problem=virtual_problem
            )
            if sol.exists():
                sol = sol[0]
                sol_status = ProblemModel.JudgeStatus.objects.filter(
                    virtual_problem=virtual_problem, author=status.author, flag=0
                )
                sol_status = sol_status.order_by('create_time')
                sub, ac, penalty = 0, 0, 0
                meet_ac = False
                for st in sol_status:
                    # 提交计数
                    sub += 1
                    # AC
                    if st.flag == 0:
                        # 如果还没遇到AC
                        if not meet_ac:
                            meet_ac = True
                        # AC计数
                        ac += 1
                        sol.best_memory = min(st.exe_mem, sol.best_memory) if sol.best_memory > -1 else st.exe_mem
                        sol.best_time = min(st.exe_time, sol.best_time) if sol.best_time > -1 else st.exe_time
                        sol.best_code_size = min(st.code_len, sol.best_code_size) if sol.best_code_size > -1 else st.code_len
                    # 其他（判定罚时，但是只要AC过，就不再判定
                    else:
                        # 如果还没遇到AC
                        if not meet_ac:
                            if str(st.flag) in [1, 2, 3, 4, 5, 6, 7, 10, 11]:
                                penalty += 1
                sol.submission, sol.accepted, sol.penalty = sub, ac, penalty
                sol.save(force_update=True)

    # 执行清理
    session.clean()
    return "FINISHED."


def tcmaker_callback(session, result):
    """
    测试数据生成器回调
    :param session: TCMaker Session
    :param result:
    :return:
    """
    status = ProblemModel.TCGeneratorStatus.objects.filter(id=result.status_id)
    if not status.exists():
        return "ERROR STATUS NOT EXISTS"
    status = status[0]
    status.exe_mem = result.memused
    status.exe_time = result.timeused
    status.flag = result.exitcode
    status.result = result.dump_json()
    status.save()

    if status.flag == 0:
        response = request.urlopen("%s%s?auth_code=%s" % (
            settings.MASTER_SERVER_URL,
            reverse('api.problem.manager.test.cases.maker.callback', args=(status.problem_id, status.id)),
            status.auth_code
        ))
        result = response.read()
        result = result.decode('utf-8')
        print(result)

    session.clean()
    return "FINISHED."
