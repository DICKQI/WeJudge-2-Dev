# -*- coding: utf-8 -*-
# coding:utf-8
import Levenshtein
from wejudge.core import *
from wejudge.const import system
import apps.contest.models as ContestModel


__author__ = 'lancelrq'


class ContestCodeCrossCheck(object):

    def __init__(self, contest_id, status_id):

        contest = ContestModel.Contest.objects.filter(id=contest_id)
        if not contest.exists():
            raise RuntimeError("Judge Status not Found.")

        self.contest = contest[0]

        status = self.contest.judge_status.filter(id=status_id)
        if not status.exists():
            raise RuntimeError("Judge Status not Found.")

        self.status = status[0]
        self.author = self.status.author
        self.problem = self.status.problem
        self.virtual_problem = self.status.virtual_problem

    def text_check(self):

        if self.author.role > 0:
            return "ADMIN ROLE NOT SUPPORT"
        if self.problem.problem_type != 0:
            return " PROBLEM TYPE NOT SUPPORT"

        status_list = self.contest.judge_status.filter(
            id__lt=self.status.id, flag=0, virtual_problem=self.virtual_problem
        ).exclude(author=self.author)

        submit_storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CODE_SUBMIT, '')

        source_status = self.status
        if not submit_storage.exists(source_status.code_path):
            raise OSError("Status %d Code File Not Found!")
        fp = submit_storage.open_file(source_status.code_path, 'r')
        source_code = fp.read()
        fp.close()

        for target_status in status_list:

            if not submit_storage.exists(target_status.code_path):
                raise OSError("Status %d Code File Not Found!")
            fp = submit_storage.open_file(target_status.code_path, 'r')
            target_code = fp.read()
            fp.close()

            ratio = self.levenshtein(source_code, target_code)
            print("%s -> %s (%.3f%%)" % (source_status.id, target_status.id, ratio))

            if ratio >= self.contest.cross_check_ratio:
                self.save_result(source_status, target_status, ratio)

        return "FINISH"

    def levenshtein(self, source, target):

        source = source.replace('\n', '').replace('\r', '').replace('\t', '').replace('\n', '')
        target = target.replace('\n', '').replace('\r', '').replace('\t', '').replace('\n', '')

        return Levenshtein.ratio(source, target)

    def save_result(self, source_status, target_status, ratio):

        cc = ContestModel.ContestCodeCrossCheck()
        cc.contest = self.contest
        cc.problem = self.virtual_problem
        cc.source = source_status
        cc.target = target_status
        cc.levenshtein_similarity_ratio = ratio
        cc.save()
