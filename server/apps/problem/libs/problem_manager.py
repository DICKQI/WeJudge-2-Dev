# -*- coding: utf-8 -*-
# coding:utf-8
import time
import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.utils import tools
from wejudge.const import system
import apps.problem.models as ProblemModel
from .workers import tcmaker
from .base import ProblemBaseController

__author__ = 'lancelrq'


class ProblemManagerController(ProblemBaseController):

    def __init__(self, request, response):
        super(ProblemManagerController, self).__init__(request, response)

    # ===== Problem Edit =====

    # 题目信息编辑实现
    def _edit_problem(self):
        """
        题目信息编辑实现
        :return:
        """

        is_new = False
        if self.problem is None:
            is_new = True

        parser = ParamsParser(self._request)
        title = parser.get_str("title", require=True, method="POST", errcode=2202)
        difficulty = parser.get_int("difficulty", 0, method="POST")
        description = parser.get_str("description", require=True, method="POST", errcode=2203)
        _input = parser.get_str("input", "", method="POST")
        output = parser.get_str("output", "", method="POST")
        sample_input = parser.get_str("sample_input", "", method="POST")
        sample_output = parser.get_str("sample_output", "", method="POST")
        hint = parser.get_str("hint", "", method="POST")
        source = parser.get_str("source", "", method="POST")

        if is_new:
            problem_type = parser.get_int("problem_type", require=True, method="POST")
        else:
            problem_type = 0

        if is_new:
            # 生成判题配置
            config = JudgeConfig()
            config.judge_type = problem_type
            config_data = config.dump_json()
            self.problem = ProblemModel.Problem()
            self.problem.problem_type = problem_type
            self.problem.judge_config = config_data
            # 写入用户配置
            user = self.session.account
            self.problem.author = user.master if hasattr(user, 'master') else user

        self.problem.title = title
        self.problem.difficulty = difficulty
        self.problem.description = description
        self.problem.input = _input
        self.problem.output = output
        self.problem.sample_input = sample_input
        self.problem.sample_output = sample_output
        self.problem.hint = hint
        self.problem.source = source

        self.problem.save()

        if is_new:
            if self.problem_set is not None:
                psitem = ProblemModel.ProblemSetItem()
                psitem.entity = self.problem
                psitem.problemset = self.problem_set
                psitem.save()
                self.problem_set.items.add(psitem)
                self.problem_set.items_count = self.problem_set.items.count()
                self.problem_set.save()

            self._init_problem_dir()

        return self.problem

    # 发布新题目
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(0)
    def create_problem(self):
        """
        发布新题目
        :return:
        """
        if not self.session.account.permission_publish_problem:
            return WeJudgeError(2200)
        return self._edit_problem()

    # 编辑题目
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def modify_problem(self):
        """
        编辑题目
        :return:
        """
        return self._edit_problem()

    # ==== Problemset Relation =====

    # 获取题目对于题目集合的关联
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(4)
    def get_problemset_relations(self):
        """
        获取题目对于题目集合的关联
        :return:
        """
        problemsets = ProblemModel.ProblemSet.objects.filter(items__entity=self.problem)
        return {
            "data": [pset.json(items=[
                'id', 'title', 'private', 'publish_private', 'manager', 'manager__nickname'
            ]) for pset in problemsets]
        }

    # 将题目推送到指定题目集(已内部控制权限)
    @ProblemBaseController.login_validator
    def publish_to_problemset(self):
        """
        将题目推送到指定题目集
        :return:
        """
        return self._publish_to_problemset(self.problem, self.problem_set)

    # 从题库中移除题目(已内部控制权限)
    @ProblemBaseController.login_validator
    def remove_from_problemset(self):
        """
        从题库中移除题目
        :return:
        """
        return self._remove_from_problemset(self.problem, self.problem_set)

    # ===== Judge Config =====

    # 获取评测设置信息
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(4)
    def get_judge_config(self):
        """
        获取评测设置信息
        :return:
        """
        return self._get_judge_config(self.problem)

    # 评测开关
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def toggle_judge(self):
        """
        评测开关
        :return:
        """
        if self.problem.pause_judge:
            # 如果目标是启用评测
            config = self._load_judge_configuation(self.problem)
            # 检查测试数据量
            if len(config.test_cases) == 0:
                raise WeJudgeError(2207)

        self.problem.pause_judge = not self.problem.pause_judge
        self.problem.save()
        return True

    # 保存评测设置
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def save_judge_config(self):
        """
        保存评测设置
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)

        special_judge = parser.get_int("special_judge", 0, method="POST")
        lang_list = parser.get_list("lang", method="POST")
        permission = parser.get_list("permission", method="POST")

        lang = 0
        for item in lang_list:
            if system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(item):
                lang = (lang | int(item))

        pcode = 0
        for p in permission:
            if p.isnumeric():
                p = int(p)
                pcode |= p

        self.problem.permission = pcode
        self.problem.lang = lang
        self.problem.save()

        config.special_judge = special_judge
        self._save_judge_configuation(config)
        self._dump_judge_configuation_to_file()

        return True

    # 保存特殊评测的程序代码
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def save_specical_judge_program(self):
        """
        保存特殊评测的程序代码
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)

        code_file = parser.get_file("uploadFile", require=True)
        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('special_judge')

        fp = dcstorage.open_file("judger.cpp", "wb")

        for chunk in code_file.chunks():
            fp.write(chunk)
        fp.close()

        spj_path = dcstorage.get_file_path("judger")

        from wejudge.judger.utils import compiler
        result, msg = compiler(
            [dcstorage.get_file_path("judger.cpp")],
            spj_path, 'g++ %s -o %s -ansi -fno-asm -Wall -lm --static'
        )
        if result:
            config.special_judger_program = 'judger'
            self._save_judge_configuation(config)
            self._dump_judge_configuation_to_file()

        return result, msg

    # ===== Answer Cases =====

    # 保存示例代码
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def save_answer_case(self):
        """
        保存示例代码
        :return:
        """
        parser = ParamsParser(self._request)
        lang = parser.get_int("lang", require=True, method="POST", errcode=2002)
        time_limit = parser.get_int("time_limit", 1000, method="POST")
        mem_limit = parser.get_int("mem_limit", 32768, method="POST")
        code = parser.get_str("code", "", method="POST")

        if not system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(lang):
            raise WeJudgeError(2002)

        storage = self._get_problem_storage(self.problem, "code_cases")
        fp = storage.open_file("%s.answer" % lang, "w")
        fp.write(code)
        fp.close()

        config = self._load_judge_configuation(self.problem)
        config.time_limit[str(lang)] = time_limit
        config.mem_limit[str(lang)] = mem_limit
        self._save_judge_configuation(config)
        self._dump_judge_configuation_to_file()

        return True

    # ===== Test Cases =====

    # 保存测试数据设置(或者新建）
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def save_test_cases_settings(self):
        """
        保存测试数据设置
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        handle = parser.get_str("handle", "", method="POST")
        is_new = parser.get_boolean("is_new", False, method="POST")
        name = parser.get_str('name', "", method="POST")
        score_precent = parser.get_int("score_precent", 0, method="POST")
        available = parser.get_boolean("available", True, method="POST")
        visible = parser.get_boolean("visible", False, method="POST")
        pre_judge = parser.get_boolean("pre_judge", False, method="POST")

        if is_new:
            jc = JudgeTestCaseItem()
            jc.handle = tools.gen_handle()
            jc.order = len(config.test_cases) + 1
        else:
            jc = self.__find_test_cases(config, handle)
            if jc is None:
                raise WeJudgeError(2204)
            # Pop
            config.test_cases.remove(jc)

        jc.name = name if name != "" else "Problem %s TestCase %s" % (self.problem.id, jc.order)
        jc.score_precent = score_precent
        if len(config.test_cases) == 0 and jc.score_precent == 0:
            jc.score_precent = 100
        jc.available = available
        jc.visible = visible
        jc.pre_judge = pre_judge
        jc.update_time = int(time.time())
        # Push
        config.test_cases.append(jc)

        scp = 0
        for tc in config.test_cases:
            scp += tc.score_precent
        if scp > 100 or scp < 0:
            raise WeJudgeError(2205)

        if is_new:
            pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
            dcstorage = pstorage.get_child_storage('test_cases')
            dcstorage.open_file("%s.in" % handle, 'w+').close()
            dcstorage.open_file("%s.out" % handle, 'w+').close()

        self._save_judge_configuation(config)
        self._dump_judge_configuation_to_file()

        return True

    # 删除测试数据
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def remove_test_cases(self):
        """
        删除测试数据
        :return:
        """
        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        handle = parser.get_str("handle", "", method="POST")
        jc = self.__find_test_cases(config, handle)
        if jc is None:
            raise WeJudgeError(2204)
        config.test_cases.remove(jc)

        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('test_cases')
        dcstorage.delete("%s.in" % handle)
        dcstorage.delete("%s.out" % handle)

        self._save_judge_configuation(config)
        self._dump_judge_configuation_to_file()

        return True

    # 获取测试数据的内容
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(4)
    def get_test_cases_content(self):
        """
        获取测试数据的内容
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        handle = parser.get_str("handle", "", method="GET")

        tc = self.__find_test_cases(config, handle)
        if tc is None:
            raise WeJudgeError(2204)

        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('test_cases')

        view = {
            "input": '',
            "output": ''
        }

        fnin = "%s.in" % handle
        fnout = "%s.out" % handle

        if dcstorage.exists(fnin):
            if dcstorage.get_file_size(fnin) > 1 * 1024 * 1024:
                raise WeJudgeError(2206)
            fin = dcstorage.open_file(fnin, 'r')
            view['input'] = fin.read()
            fin.close()

        if dcstorage.exists(fnout):
            if dcstorage.get_file_size(fnout) > 1 * 1024 * 1024:
                raise WeJudgeError(2206)
            fout = dcstorage.open_file(fnout, 'r')
            view['output'] = fout.read()
            fout.close()

        return view

    # 保存测试数据的内容
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def save_test_cases_content(self):
        """
        保存测试数据的内容
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        handle = parser.get_str("handle", "", method="GET")
        cin = parser.get_str("input", "", method="POST").replace("\r\n", '\n').replace("\r", "\n")
        cout = parser.get_str("output", "", method="POST").replace("\r\n", '\n').replace("\r", "\n")

        tc = self.__find_test_cases(config, handle)
        if tc is None:
            raise WeJudgeError(2204)

        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('test_cases')

        fnin = "%s.in" % handle
        fnout = "%s.out" % handle

        fin = dcstorage.open_file(fnin, 'w+')
        fin.write(cin)
        fin.close()

        fout = dcstorage.open_file(fnout, 'w+')
        fout.write(cout)
        fout.close()

        return True

    # 保存上传的测试数据的内容
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def upload_test_cases_content(self, type):
        """
        保存上传的测试数据的内容
        :param type: 输入或者输出?
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        handle = parser.get_str("handle", "", method="GET")

        tc = self.__find_test_cases(config, handle)
        if tc is None:
            raise WeJudgeError(2204)

        file = parser.get_file("uploadFile", require=True, max_size=100*1024*1024)

        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('test_cases')

        fn = "%s.%s" % (handle, type)
        fp = dcstorage.open_file(fn, "wb")

        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        # 清除UTF-8的BOM
        tools.clear_bom(dcstorage, fn)

        return True

    # 使用测试数据生成器生成目标输出结果
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def tcmaker_run(self):
        """
        使用测试数据生成器生成目标输出结果
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        lang = parser.get_int("lang", require=True, method="POST", errcode=2002)
        if not system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(lang):
            raise WeJudgeError(2002)

        if config.special_judge == system.WEJUDGE_SPECIAL_JUDGE_INTERACTIVE:
            raise WeJudgeError(2208)

        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('code_cases')

        code = ""

        if config.judge_type == system.WEJUDGE_JUDGE_TYPE_FILL:
            # 填空模式 处理
            if dcstorage.exists("%s.demo.answer" % lang):
                fp = dcstorage.open_file("%s.demo.answer" % lang, 'r')
                code = fp.read()
                fp.close()
            else:
                raise WeJudgeError(2209)
        else:
            if dcstorage.exists("%s.answer" % lang):
                fp = dcstorage.open_file("%s.answer" % lang, 'r')
                code = fp.read()
                fp.close()
            else:
                raise WeJudgeError(2209)

        code_path = self._save_code_upload(lang, code)

        status = ProblemModel.TCGeneratorStatus()
        status.lang = lang
        status.author = self.session.account
        status.problem = self.problem
        status.code_len = len(code)
        status.code_path = code_path
        status.auth_code = tools.gen_passwd(tools.gen_handle())
        status.save()

        tcmaker.delay(self.problem.id, status.id)

        return True

    # 获取测试数据生成器评测历史
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(4)
    def get_tcmaker_status(self):
        """
        获取测试数据生成器评测历史
        :return:
        """

        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        @WeJudgePagination(
            model_object=ProblemModel.TCGeneratorStatus.objects.filter(problem=self.problem),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_status_item(status):

            item = status.json(items=[
                "id", "flag", "lang", "create_time", "exe_time", "exe_mem", "code_len",
                "problem", "author", "problem_id", "author__nickname", "author__realname",
                "author__id", "author__sex", "author__username", "auth_code"
            ], timestamp=False)

            item['lang'] = system.WEJUDGE_PROGRAM_LANGUAGE_CALLED.get(item['lang'])
            return item

        data = proc_status_item()

        data['flag_desc'] = system.WEJUDGE_JUDGE_STATUS_DESC

        return data

    # 测试数据生成器回调
    def tcmaker_callback(self, tcsid):
        """
        测试数据生成器回调
        :param tcsid: TestCaseMaker StatusID
        :return:
        """
        parser = ParamsParser(self._request)
        auth_code = parser.get_str('auth_code', '')
        # 获取生成器的记录
        tc_status = ProblemModel.TCGeneratorStatus.objects.filter(id=tcsid)
        if not tc_status.exists():
            return "ERROR: TestCaseMaker Status don't exists."
        # 防止非法调用
        tc_status = tc_status[0]
        if tc_status.auth_code == "":
            return "ERROR: This status is EXPIRED."
        if tc_status.auth_code != auth_code:
            return "ERROR: Wrong `auth_code`"
        # 非AC状态不能写入数据
        if tc_status.flag != 0:
            return "ERROR: No allowed to replace testcases when it got no `AC` flag"

        # 打开输出结果目录
        jr_storage = WeJudgeStorage(
            system.WEJUDGE_STORAGE_ROOT.JUDGE_RESULT, 'tcmaker'
        ).get_child_storage(str(self.problem.id)).get_child_storage(str(tc_status.id))
        # 打开题目数据目录
        problem_storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        tc_storage = problem_storage.get_child_storage("test_cases")
        # 读取配置文件
        config = self._load_judge_configuation(self.problem)

        # 读取测试数据配置
        for tc in config.test_cases:
            otdfile = "%s.outdata" % tc.handle
            if jr_storage.is_file(otdfile):
                # 将数据拷入目标位置
                tc_storage.clone_from_file("%s.out" % tc.handle, jr_storage.get_file_path(otdfile))

        # 清理状态
        tc_status.auth_code = ""
        tc_status.save()
        return "OK! Written."

    # 查找测试数据项目
    def __find_test_cases(self, config, handle):
        """
        查找测试数据项目
        :param config: JudgeConfig
        :param handle:  测试数据的Handle
        :return:
        """
        for tc in config.test_cases:
            if tc.handle == handle:
                return tc
        return None

    # ===== Demo Cases =====

    # 保存填空示例代码
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def save_demo_cases_code(self):
        """
        保存填空示例代码
        :return:
        """
        parser = ParamsParser(self._request)
        lang = parser.get_int("lang", require=True, method="POST", errcode=2002)
        time_limit = parser.get_int("time_limit", 1000, method="POST")
        mem_limit = parser.get_int("mem_limit", 32768, method="POST")
        code = parser.get_str("code", "", method="POST")

        if not system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(lang):
            raise WeJudgeError(2002)

        storage = self._get_problem_storage(self.problem, "code_cases")
        fp = storage.open_file("%s.demo" % lang, "w")
        fp.write(code)
        fp.close()

        config = self._load_judge_configuation(self.problem)
        config.time_limit[str(lang)] = time_limit
        config.mem_limit[str(lang)] = mem_limit
        self._save_judge_configuation(config)
        self._dump_judge_configuation_to_file()

        return True

    # 保存填空用例设置(或者新建）
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def save_demo_cases_settings(self):
        """
        保存填空用例设置
        :return:
        """

        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        handle = parser.get_str("handle", "", method="POST")
        is_new = parser.get_boolean("is_new", False, method="POST")
        lang = parser.get_int("lang", require=True, method="POST", errcode=2002)
        name = parser.get_str('name', "", method="POST")
        code = parser.get_str('code', "", method="POST")

        dc = config.demo_cases.get(str(lang), [])

        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('code_cases')

        try:
            d = "{}"
            if dcstorage.exists("%s.demo.answer" % lang):
                fp = dcstorage.open_file("%s.demo.answer" % lang, 'r')
                d = fp.read()
                fp.close()
            demoanswer = json.loads(d)
        except:
            demoanswer = {}

        if is_new:
            jd = JudgeDemoItem()
            jd.handle = tools.gen_handle()
            jd.name = jd.handle
            dc.append(jd)
            demoanswer[jd.handle] = code
        else:
            old_dc = dc
            dc = []
            for jd in old_dc:
                if jd.handle != handle:
                    dc.append(jd)
                    continue
                jd.name = name if name != "" else jd.handle
                dc.append(jd)
                demoanswer[handle] = code

        config.demo_cases[str(lang)] = dc

        fp = dcstorage.open_file("%s.demo.answer" % lang, 'w+')
        fp.write(json.dumps(demoanswer))
        fp.close()

        self._save_judge_configuation(config)
        self._dump_judge_configuation_to_file()

        return True

    # 删除填空用例
    @ProblemBaseController.login_validator
    @ProblemBaseController.problem_privilege_validator(8)
    def remove_demo_cases(self):
        """
        删除填空用例
        :return:
        """
        config = self._load_judge_configuation(self.problem)

        parser = ParamsParser(self._request)
        handle = parser.get_str("handle", "", method="POST")
        lang = parser.get_int("lang", require=True, method="POST", errcode=2002)

        pstorage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
        dcstorage = pstorage.get_child_storage('code_cases')

        try:
            d = "{}"
            if dcstorage.exists("%s.demo.answer" % lang):
                fp = dcstorage.open_file("%s.demo.answer" % lang, 'r')
                d = fp.read()
                fp.close()
            demoanswer = json.loads(d)
        except:
            demoanswer = {}

        dc = config.demo_cases.get(str(lang), [])
        for jd in dc:
            if jd.handle == handle:
                dc.remove(jd)
                demoanswer.pop(handle)

        config.demo_cases[str(lang)] = dc

        fp = dcstorage.open_file("%s.demo.answer" % lang, 'w+')
        fp.write(json.dumps(demoanswer))
        fp.close()

        # remove handle from code
        fp = dcstorage.open_file("%s.demo" % lang, "r")
        demo = fp.read()
        fp.close()
        demo = demo.replace("/***## %s ##***/" % handle, "")
        fp = dcstorage.open_file("%s.demo" % lang, 'w+')
        fp.write(demo)
        fp.close()

        self._save_judge_configuation(config)
        self._dump_judge_configuation_to_file()

        return True
