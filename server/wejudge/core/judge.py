# -*- coding: utf-8 -*-
# coding:utf-8
import json
__author__ = 'lancelrq'


class JudgeTestCaseItem(object):

    def __init__(self, items=None):

        if items is None:
            items = {}
        self.name = items.get("name", "")
        self.handle = items.get("handle", "")
        self.order = items.get("order", 0)
        self.update_time = items.get("update_time", 0)
        self.available = items.get("available", True)
        self.visible = items.get("visible", False)
        self.score_precent = items.get("score_precent", 0)
        self.pre_judge = items.get("pre_judge", False)

    def dump(self):
        return {
            "name": self.name,
            "handle": self.handle,
            "order": self.order,
            "update_time": self.update_time,
            "available": self.available,
            "visible": self.visible,
            "score_precent": self.score_precent,
            "pre_judge": self.pre_judge
        }

    def dump_json(self):
        return json.dumps(self.dump())

    def __repr__(self):
        return self.dump_json()


class JudgeDemoItem(object):
    def __init__(self, items=None):

        if items is None:
            items = {}
        self.name = items.get("name", "")
        self.handle = items.get("handle", "")
        self.score_precent = items.get("score_precent", 0)

    def dump(self):
        return {
            "name": self.name,
            "handle": self.handle,
            "score_precent": self.score_precent
        }

    def dump_json(self):
        return json.dumps(self.dump())

    def __repr__(self):
        return self.dump_json()


class JudgeConfig(object):
    """
    评测配置信息类
    """
    def __init__(self, config_json=None):
        """

        :param config_json: JSON data
        """
        from wejudge.const import system

        if config_json is not None:
            try:
                data = json.loads(config_json)
            except:
                raise OSError("Load judge config json FAILED")
        else:
            data = {}

        self.time_limit = data.get("time_limit", {
            "1": 1000,
            "2": 1000,
            "4": 2000,
            "8": 1000,
            "16": 1000
        })

        self.mem_limit = data.get("mem_limit", {
            "1": 32768,
            "2": 32768,
            "4": 262144,
            "8": 65536,
            "16": 65536
        })

        self.library_cases = data.get("library_cases", [])
        self.judge_type = data.get("judge_type", system.WEJUDGE_JUDGE_TYPE_NORMAL)
        self.env_enable = data.get("env_enable", False)
        self.special_judge = data.get("special_judge", system.WEJUDGE_SPECIAL_JUDGE_DISABLED)
        self.special_judger_program = data.get("special_judger_program", "")

        test_cases = []
        for case in data.get("test_cases", []):
            item = JudgeTestCaseItem(case)
            test_cases.append(item)
        self.test_cases = test_cases

        demo_cases = {}
        for key, val in data.get("demo_cases", {}).items():
            items = [JudgeDemoItem(x) for x in val]
            demo_cases[key] = items

        self.demo_cases = demo_cases

    def dump_demo_cases(self):
        return {k: [_.dump() for _ in v] for k, v in self.demo_cases.items()}

    def dump_test_cases(self):
        return [x.dump() for x in self.test_cases]

    def dump(self):
        return {
            "time_limit": self.time_limit,
            "mem_limit": self.mem_limit,
            "test_cases": self.dump_test_cases(),
            "demo_cases": self.dump_demo_cases(),
            "library_cases": self.library_cases,
            "judge_type": self.judge_type,
            "env_enable": self.env_enable,
            "special_judge": self.special_judge,
            "special_judger_program": self.special_judger_program
        }

    def dump_json(self):
        return json.dumps(self.dump())

    def __repr__(self):
        return self.dump_json()


class JudgeResultDetailItem(object):

    def __init__(self, items=None):

        if items is None:
            items = {}
        self.handle = items.get("handle", 0)
        self.judge_result = items.get("judge_result", 0)
        self.memory_used = items.get("memory_used", 0)
        self.time_used = items.get("time_used", 0)
        self.same_lines = items.get("same_lines", 0)
        self.total_lines = items.get("total_lines", 0)
        self.re_signum = items.get("re_signum", 0)
        self.re_call = items.get("re_call", 0)
        self.re_file = items.get("re_file", "")
        self.re_file_flag = items.get("re_file_flag", 0)
        self.re_msg = items.get("re_msg", "")

    def dump(self):
        return {
            "handle": self.handle,
            "judge_result": self.judge_result,
            "time_used": self.time_used,
            "memory_used": self.memory_used,
            "total_lines": self.total_lines,
            "same_lines": self.same_lines,
            "re_signum": self.re_signum,
            "re_call": self.re_call,
            "re_file": self.re_file,
            "re_file_flag": self.re_file_flag,
            "re_msg": self.re_msg
        }

    def dump_json(self):
        return json.dumps(self.dump())

    def __repr__(self):
        return self.dump_json()


class JudgeResult(object):
    """
    判题结果类
    """
    def __init__(self, config_json=None):
        if config_json is not None:
            try:
                data = json.loads(config_json)
            except:
                data = {}
        else:
            data = {}

        self.model = None       # 这个什么鬼？我自己都忘了，反正好像没啥用... 等稳定再删？
        self.finally_code = data.get("finally_code", 0)
        self.status_id = data.get("status_id", 0)
        self.exitcode = data.get("exitcode", -1)
        self.timeused = data.get("timeused", 0)
        self.memused = data.get("memused", 0)
        self.ceinfo = data.get("ceinfo", "")

        details = []
        for case in data.get("details", []):
            item = JudgeResultDetailItem(case)
            details.append(item)
        self.details = details

    def dump(self):
        return {
            "details": [x.dump() for x in self.details],
            "memused": self.memused,
            "timeused": self.timeused,
            "exitcode": self.exitcode,
            "ceinfo": self.ceinfo,
            "status_id": self.status_id,
            "finally_code": self.finally_code
        }

    def dump_json(self):
        return json.dumps(self.dump())

    def __repr__(self):
        return self.dump_json()