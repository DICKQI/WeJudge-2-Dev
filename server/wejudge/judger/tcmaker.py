# -*- coding: utf-8 -*-
# coding:utf-8

import os
import os.path
import apps.problem.models as ProblemModel
from wejudge.const import system
from .judge import JudgeSession
__author__ = 'lancelrq'


class TCMakerSession(JudgeSession):
    """
    判题Session
    :return:
    """

    def __init__(self, problem_id, status_id, options):
        """
        :param problem_id: Problem的根ID
        :param status_id: StatusID
        :param options: 评测选项
        :return:
        """
        super(TCMakerSession, self).__init__( problem_id, status_id, options, "tcmaker", ProblemModel.TCGeneratorStatus)

    # 处理每一个Test Case
    def _judge_testcase(self, tc_storage, case):
        """
        处理每一个Test Case
        :param tc_storage:      Test Case 存储点
        :param case:            Test Case
        :return:
        """
        # 未启用的测试数据
        if not case.available:
            return True, None
        if self.config.special_judge == system.WEJUDGE_SPECIAL_JUDGE_INTERACTIVE:
            raise AttributeError("TCMaker is not allowed to do interactive judge.")
        else:
            result = self._run(tc_storage, case, no_check=True)
        # 记录信息
        self.judge_result.details.append(result)
        self.judge_result.memused = max(result.memory_used, self.judge_result.memused)
        self.judge_result.timeused = max(result.time_used, self.judge_result.timeused)

        # 获取目标输出文件位置
        target_out_file_path = self.output_storage.get_file_path("%s.out" % case.handle)
        # 保存评测状态
        self.judge_result_storage.clone_from_file("%s.outdata" % case.handle, target_out_file_path)
        return True, result.judge_result
