# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.judger import JudgeSession
from wejudge.core import JudgeConfig, JudgeResult
import apps.problem.models as ProblemModel
import apps.education.models as EduModel
from celery import task
from wejudge.const import system

__author__ = 'lancelrq'


def asgn_judge_callback(session, result):
    """
    作业判题回调
    :param session:
    :param result:
    :return:
    """

    # 注意，这里的status.problem是EduModel.AsgnProblem

    status = EduModel.JudgeStatus.objects.filter(id=result.status_id)
    if not status.exists():
        return
    status = status[0]
    status.exe_mem = result.memused
    status.exe_time = result.timeused
    status.flag = result.exitcode
    status.result = result.dump_json()
    status.save()

    asgn_problem = status.virtual_problem

    asgn_id = session.options.get('asgn_id', 0)
    asgn = EduModel.Asgn.objects.filter(id=asgn_id)
    if not asgn.exists():
        return
    asgn = asgn[0]

    # 获取实验报告
    report = EduModel.AsgnReport.objects.filter(asgn=asgn, author=status.author)
    if report.exists():
        report = report[0]
    else:
        report = None

    processer = AsgnJudgeProcesser(asgn, asgn_problem)
    processer.proc_problem()
    processer.proc_solution(report)
    if report is not None:
        processer.proc_report(report)

    session.clean()
    return "FINISHED."


class AsgnJudgeProcesser:

    def __init__(self, asgn, asgn_problem):
        self.asgn = asgn
        self.problem = asgn_problem
        self.problem_entity = asgn_problem.entity
        self.config = JudgeConfig(self.problem_entity.judge_config)
        self.strict_mode = asgn_problem.strict_mode
        self.max_score_for_wrong = asgn_problem.max_score_for_wrong

        # 缓存测试数据数据定义
        self.td_score_precent = {}
        for td in self.config.test_cases:
            self.td_score_precent[td.handle] = td.score_precent

    def proc_problem(self):
        """
        更新题目统计数据
        :return:
        """

        self.problem.accepted = EduModel.JudgeStatus.objects.filter(
            virtual_problem=self.problem, flag=0
        ).count()
        self.problem.save()

    # Asgn Solution统计部分
    def proc_solution(self, report):

        # 如果遇到第一次ac了，那么后面就只看AC的，并且允许尝试刷时间
        # 也许有些学生觉得我学有余力，我想尝试不同的做法，可以优化时间、或者内存占用，或者代码长度，那么只要AC，就会被算作是最优时间

        # 获取用户的solution数据
        sol = EduModel.Solution.objects.filter(
            asgn=self.asgn, author=report.author, problem=self.problem
        )
        if sol.exists():
            sol = sol[0]
        else:
            return

        score = 0
        # sol_status = sol.judge_status.order_by('id')
        sol_status = self.asgn.judge_status.filter(
            author=report.author, virtual_problem=self.problem
        ).order_by('id')
        sub, ac, penalty = 0, 0, 0

        meet_ac = False

        for st in sol_status:
            # 临时分数
            tscore = 0
            # 遇到AC的时候，结算，但是首次AC的记录只会结算一次
            # 如果没有遇到AC的情况
            if not meet_ac:
                if (st.flag == 0) or (not self.strict_mode and st.flag == 1):
                    sol.first_ac_time = st.create_time
                    meet_ac = True
                    sol.best_memory = min(st.exe_mem, sol.best_memory) if sol.best_memory > -1 else st.exe_mem
                    sol.best_time = min(st.exe_time, sol.best_time) if sol.best_time > -1 else st.exe_time
                    sol.best_code_size = min(st.code_len,
                    sol.best_code_size) if sol.best_code_size > -1 else st.code_len

                    if st.flag == 0:
                        tscore = 100
                    if not self.strict_mode and st.flag == 1:
                        tscore = 100.0 * (self.max_score_for_wrong / 100.0)
                else:
                    try:
                        result = JudgeResult(st.result)
                        # 遍历评测记录的具体结果
                        for dt in result.details:
                            flag = dt.judge_result
                            handle = dt.handle
                            if flag == 0:
                                tscore += self.td_score_precent.get(handle, 0)
                            # 非严格模式，PE、WA情况
                            elif not self.strict_mode and flag in [1, 4]:
                                # WA的情况下
                                if flag == 4:
                                    line_ratio = float(dt.same_lines) / float(dt.total_lines)
                                else:
                                    line_ratio = 1
                                tscore += self.td_score_precent.get(handle, 0) * line_ratio * (self.max_score_for_wrong / 100.0)

                    except BaseException as ex:
                        tscore = 0
            # 提交计数
            sub += 1
            # AC 计数
            if (st.flag == 0) or (not self.strict_mode and st.flag == 1):
                ac += 1
            # 罚时判定
            if st.flag in [2, 3, 4, 5, 6, 7]:
                penalty += 1
            # 严格模式下，对PE罚时
            if self.strict_mode and st.flag == 1:
                penalty += 1

            # 取最大的一次成绩
            score = max(score, tscore)

        sol.score = score
        sol.submission, sol.accepted, sol.penalty = sub, ac, penalty
        sol.save()

        if sol.first_ac_time is not None:
            delta = sol.first_ac_time - report.start_time
            sol.used_time_real = delta.total_seconds()
            sol.used_time = system.WEJUDGE_GENERAL_PENATLY_TIME * sol.penalty + delta.total_seconds()

            if sol.used_time_real < 0:
                sol.used_time_real = 0
            if sol.used_time < 0:
                sol.used_time = 0
        else:
            sol.used_time_real = 0
            sol.used_time = 0

        sol.save(force_update=True)

    def proc_report(self, report):
        """
        实验报告统计
        感受到绝望了吗兄弟，这是WJ1.0里积累的代码，做啥的你自己看吧我懒得解释了
        :param report:
        :return:
        """
        full_score = self.asgn.full_score
        asgn_problems = self.asgn.problems.all()
        score = 0
        ac_cnt = 0
        total_cnt = 0
        solved_cnt = 0
        report.rank_timeused = 0
        report.rank_solved = 0
        for ap in asgn_problems:
            sol = self.asgn.solution_set.filter(problem=ap, author=report.author)
            sol = sol[0] if sol.exists() else None
            ac = True if (sol is not None) and (sol.accepted > 0) else False
            sol_score = sol.score if (sol is not None) else 0
            score += ap.score if ac else int(ap.score * (sol_score / 100.0))
            ac_cnt += sol.accepted if (sol is not None) else 0
            total_cnt += sol.submission if (sol is not None) else 0
            solved_cnt += 1 if ac else 0
            if ac:
                report.rank_timeused += sol.used_time
                report.rank_solved += 1

        if score > full_score:
            score = full_score

        report.judge_score = score
        report.ac_counter = ac_cnt
        report.submission_counter = total_cnt
        report.solved_counter = solved_cnt
        report.save()

