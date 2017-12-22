


import json
import apps.contest.models as ContestModel
from wejudge.core import JudgeConfig, JudgeResult

__author__ = 'lancelrq'


def contest_judge_callback(session, result):
    """
    比赛判题回调
    :param session:
    :param result:
    :return:
    """

    # 注意，这里的status.problem是ContestModel.ContestProblem

    status = ContestModel.JudgeStatus.objects.filter(id=result.status_id)
    if not status.exists():
        return 'Status Not Exists.'
    status = status[0]
    status.exe_mem = result.memused
    status.exe_time = result.timeused
    status.flag = result.exitcode
    status.result = result.dump_json()
    status.save(force_update=True)

    contest_problem = status.virtual_problem

    contest_id = session.options.get('contest_id', 0)
    contest = ContestModel.Contest.objects.filter(id=contest_id)
    if not contest.exists():
        return 'Contest Not Exists.'
    contest = contest[0]

    # 发起查重
    ignore_cc = contest.cross_check_ignore_problem.filter(id=contest_problem.id).exists()
    if not ignore_cc and contest.cross_check and status.flag == 0:
        from .workers import cross_check
        cross_check.delay(contest.id, status.id)

    if contest_problem.judger_mode in [1, 2]:
        # 设置状态为人工评测中
        status.flag = 20
        status.save()
        return "MANUAL JUDGE."

    processer = ContestJudgeProcesser(contest, contest_problem)
    processer.proc_problem()
    processer.proc_solution(status.author)
    processer.proc_rank(status.author)

    session.clean()
    return "FINISHED."


# 评测处理程序
class ContestJudgeProcesser:

    def __init__(self, contest, contest_problem):
        self.contest = contest
        self.problem = contest_problem
        self.problem_entity = contest_problem.entity
        self.config = JudgeConfig(self.problem_entity.judge_config)
        self.penaltys = (self.contest.penalty_items or "").split(",")
        penalty_time = self.contest.penalty_time
        self.penalty_time = penalty_time.hour * 3600 + penalty_time.minute * 60 + penalty_time.second

    def proc_problem(self):
        """
        更新题目统计数据
        :return:
        """
        self.problem.accepted = ContestModel.JudgeStatus.objects.filter(
            virtual_problem=self.problem, flag=0).count()
        self.problem.save(force_update=True)

    # Solution统计部分
    def proc_solution(self, author):
        """
        根据solution计算排行榜信息
        :param author:
        :return:
        """

        # 统计（用户）
        sol = ContestModel.ContestSolution.objects.filter(
            contest=self.contest, author=author, problem=self.problem
        )
        if sol.exists():
            sol = sol[0]
        else:
            return

        # sol_status = sol.judge_status.order_by('create_time')
        sol_status = self.contest.judge_status.filter(
            author=author, virtual_problem=self.problem
        ).order_by('id')
        sub, ac, penalty = 0, 0, 0

        meet_ac = False

        for st in sol_status:

            sub += 1

            # AC
            if st.flag == 0:

                if not meet_ac:
                    sol.first_ac_time = st.create_time
                    meet_ac = True

                ac += 1
                sol.best_memory = min(st.exe_mem, sol.best_memory) if sol.best_memory > -1 else st.exe_mem
                sol.best_time = min(st.exe_time, sol.best_time) if sol.best_time > -1 else st.exe_time
                sol.best_code_size = min(st.code_len, sol.best_code_size) if sol.best_code_size > -1 else st.code_len

            # 其他（判定罚时，但是只要AC过，就不再判定
            else:

                if not meet_ac:
                    if str(st.flag) in self.penaltys:
                        penalty += 1

        sol.submission, sol.accepted, sol.penalty = sub, ac, penalty

        if sol.first_ac_time is not None:
            delta = sol.first_ac_time - self.contest.start_time
            sol.used_time_real = delta.total_seconds()
            sol.used_time = self.penalty_time * penalty + delta.total_seconds()

            if sol.used_time_real < 0:
                sol.used_time_real = 0
            if sol.used_time < 0:
                sol.used_time = 0
        else:
            sol.used_time_real = 0
            sol.used_time = 0

        sol.save(force_update=True)

        # 一血评估
        sol_f = ContestModel.ContestSolution.objects.filter(
            contest=self.contest, problem=self.problem, author__role=0, accepted__gt=0).order_by('first_ac_time')
        if sol_f.exists():
            sol_f = sol_f[0]
            if sol_f == sol:
                sol.is_first_blood = True
            else:
                sol.is_first_blood = False
            sol.save(force_update=True)

    def proc_rank(self, author):

        """
        更新排行信息
        :param author:
        :return:
        """

        sol_list = ContestModel.ContestSolution.objects.filter(
            contest=self.contest, author=author
        )
        author.rank_timeused = 0
        author.rank_solved = 0
        rank_last_ac_time = None
        for item in sol_list:

            if item.accepted > 0:
                author.rank_timeused += item.used_time
                author.rank_solved += 1

            if rank_last_ac_time is None:
                rank_last_ac_time = item.first_ac_time
            else:
                if item.first_ac_time is not None:
                    rank_last_ac_time = max(rank_last_ac_time, item.first_ac_time)

        author.rank_last_ac_time = rank_last_ac_time
        author.save(force_update=True)
