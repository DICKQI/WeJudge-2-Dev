# -*- coding: utf-8 -*-
# coding:utf-8
import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.problem.models as ProblemModel
from .workers import judge
from .base import ProblemBaseController

__author__ = 'lancelrq'


class JudgeStatusController(ProblemBaseController):

    def __init__(self, request, response):
        super(JudgeStatusController, self).__init__(request, response)
        self.prefix = 'problem'

    # 测试数据细节权限检查器（可重写）
    def testcase_high_privilege(self):
        """
        测试数据细节权限检查器（可重写）

        通过这个检查器，则可以查看测试数据
        如果不能通过这个检查器，则看测试数据是否隐藏，如果隐藏，则不能查看测试数据，否则可以。
        :return:
        """
        return self.check_problem_privilege(4, throw=False)

    # 获取评测详情
    @ProblemBaseController.login_validator
    @ProblemBaseController.judge_status_privilege_validator
    def get_judge_detail(self):
        """
        获取评测详情
        :return:
        """
        status = self.status
        self.problem = self.status.problem

        config = self._load_judge_configuation(self.problem)
        config_content = config.dump()

        # 脱敏
        config_content['special_judger_program'] = ""
        config_content['library_cases'] = ""

        try:
            result_content = JudgeResult(self.status.result)
        except Exception as ex:
            raise WeJudgeError(2007)

        problem_storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        tc_storage = problem_storage.get_child_storage("test_cases")
        jr_storage = WeJudgeStorage(
            system.WEJUDGE_STORAGE_ROOT.JUDGE_RESULT, self.prefix
        ).get_child_storage(str(self.problem.id)).get_child_storage(str(status.id))

        result_detail_content = {}

        for tc in config.test_cases:

            if not tc.visible and not self.testcase_high_privilege():
                result_detail_content[tc.handle] = -1   # 测试数据被屏蔽
                continue

            item = None
            for i in result_content.details:
                if i.handle == tc.handle:
                    item = tc
                    break

            if item is None:
                result_detail_content[tc.handle] = -2   # 测试数据项目被删除或者不存在
                continue

            rel = {}

            infile = "%s.in" % item.handle
            insize = tc_storage.get_file_size(infile)
            if insize > 102400:
                rel['indata'] = -1
            elif insize == -1:
                rel['indata'] = -2
            else:
                fin = tc_storage.open_file(infile, 'r')
                rel['indata'] = fin.read()
                fin.close()

            outfile = "%s.out" % item.handle
            outsize = tc_storage.get_file_size(outfile)
            if outsize > 102400:
                rel['outdata'] = -1
            elif outsize == -1:
                rel['outdata'] = -2
            else:
                fout = tc_storage.open_file(outfile, 'r')
                rel['outdata'] = fout.read()
                fout.close()

            otdfile = "%s.outdata" % item.handle
            otdsize = jr_storage.get_file_size(otdfile)
            if otdsize > 102400:
                rel['userdata'] = -1
            elif otdsize == -1:
                rel['userdata'] = -2
            else:
                foutdata = jr_storage.open_file(otdfile, 'r')
                rel['userdata'] = foutdata.read()
                foutdata.close()

            result_detail_content[item.handle] = rel

        view = {
            "result": result_content.dump(),
            "config": config_content,
            "lang": status.lang,
            "langs_call": system.WEJUDGE_PROGRAM_LANGUAGE_CALLED,
            "desc": system.WEJUDGE_JUDGE_STATUS_DESC,
            "result_detail": result_detail_content
        }
        return view