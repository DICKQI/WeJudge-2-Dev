# -*- coding: utf-8 -*-
# coding:utf-8

import os
import os.path
import json
import lorun
import types
import shutil
import apps.problem.models as ProblemModel
from .utils import syscall, compiler, _log, get_java_class_name
from wejudge.const import system
from wejudge.utils import tools
from wejudge.core import WeJudgeStorage, JudgeConfig, JudgeResult, JudgeResultDetailItem
import traceback
__author__ = 'lancelrq'

class JudgeSession(object):
    """
    判题Session
    :return:
    """

    def __init__(self, problem_id, status_id, options, prefix='problem', model=ProblemModel.JudgeStatus):
        """
        :param problem_id: Problem的根ID
        :param status_id: StatusID
        :param options: 评测选项
        :param prefix: 前缀，可用的值为problem | education | contest ，它将决定评测输出结果的存放点
        :param model: Status for model
        :return:
        """

        if prefix not in ('problem', 'education', 'contest', 'tcmaker'):
            prefix = 'problem'

        self.judge_result = JudgeResult()
        self._model = model
        self.options = options
        self.session_id = tools.uuid1()
        self.problem_id = str(problem_id)
        self.source_code = ""
        self.target_program = ""
        self.java_class_name = ""
        # 记录session_id
        self.options['session_id'] = self.session_id
        # 创建Session临时目录
        self.session_storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.TEMP_DIR, self.session_id)
        # 创建输出数据的目录
        self.output_storage = self.session_storage.get_child_storage("output")
        # 创建编译环境目录
        self.program_storage = self.session_storage.get_child_storage("program")
        # 载入数据目录
        self.problem_storage = WeJudgeStorage(
            system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA,
            str(self.problem_id), create_new=False
        )
        # 载入结果输出目录
        self.judge_result_storage = WeJudgeStorage(
            system.WEJUDGE_STORAGE_ROOT.JUDGE_RESULT, prefix
        ).get_child_storage(str(self.problem_id)).get_child_storage(str(status_id))
        # 载入配置
        judge_json_file = self.problem_storage.open_file("judge.json", "r")
        if judge_json_file is None:
            raise OSError("Load judge config file FAILED")
        self.config = JudgeConfig(judge_json_file.read())
        if self.config.special_judge != system.WEJUDGE_SPECIAL_JUDGE_DISABLED:
            self.special_judge = self.problem_storage.get_child_storage("special_judge")
        else:
            self.special_judge = self.problem_storage
        # 载入评测提交记录
        self.status = self._load_status(status_id)
        # 挂载虚拟只读环境
        if self.config.env_enable and not syscall("ln -s %s ./env" % self.problem_storage.get_folder_path("env")):
            raise OSError("Cannot mount judge_env")

    # 判题调用实现
    def judge(self, callback):
        """
        判题入口实现
        :param callback: 回调
        :return:
        """
        self.judge_result.status_id = self.status.id
        # self.judge_result.model = str(self._model)
        try:
            if not isinstance(callback, types.FunctionType):
                raise AttributeError("Callback not a function")
            # 获取用户源代码文件地址
            self.source_code = self._get_usercode_path()

            if self.config.judge_type == system.WEJUDGE_JUDGE_TYPE_NORMAL:
                # 正常模式预处理
                self._normal_judge()
            elif self.config.judge_type == system.WEJUDGE_JUDGE_TYPE_FILL:
                # 填空模式预处理
                self._fill_judge()
            else:
                raise AttributeError("Wrong Judge Type")
        except Exception as ex:
            self.judge_result.exitcode = system.WEJUDGE_JUDGE_EXITCODE.SE
            self.judge_result.ceinfo = str(ex)
            traceback.print_exc()


        callback(self, self.judge_result)

    # 清空Session
    def clean(self):
        """
        清空Session，清除后，请不要再次调用本对象的任何方法，否则将会出错
        :return:
        """
        shutil.rmtree(self.session_storage.get_current_path())
        return True

    # 载入评测状态信息
    def _load_status(self, status_id):
        """
        载入评测状态信息
        :param status_id:
        :return:
        """
        obj = self._model.objects.filter(id=status_id)
        if not obj.exists():
            raise OSError("Cannot load judge status")
        else:
            return obj[0]

    # 获取用户代码的地址
    def _get_usercode_path(self):
        """
        获取用户代码的地址
        :return:
        """
        return os.path.join(system.WEJUDGE_STORAGE_ROOT.CODE_SUBMIT, self.status.code_path)

    # 读取用户提交的代码
    def _load_usercode(self):
        """
        读取用户提交的代码
        :return:
        """
        source_code = os.path.join(system.WEJUDGE_STORAGE_ROOT.CODE_SUBMIT, self.status.code_path)
        fcode = open(source_code, "r")
        source_code = fcode.read()
        fcode.close()
        return source_code

    # 填空填空判题模式模式预处理
    def _fill_judge(self):
        """
        填空填空判题模式模式预处理
        :return:
        """
        lang = self.status.lang
        demo_case = self.config.demo_cases.get(str(lang), [])
        # 读取用户提交的代码
        source_code = json.loads(self._load_usercode())
        # 获取预设模板代码
        demo_code_file_name = "%s.demo" % lang
        demo_code_area_list = demo_case
        dc_storage = self.problem_storage.get_child_storage("code_cases")
        f1 = dc_storage.open_file(demo_code_file_name, "r")
        demo_source = f1.read()
        f1.close()
        # 创建编译目标代码文件
        target_name = "%s%s" % (tools.uuid1(), system.WEJUDGE_CODE_FILE_EXTENSION.get(lang, ''))
        code_target = self.session_storage.open_file(target_name, "w+")
        # 拼合代码
        for case in demo_code_area_list:
            handle = case.handle
            demo_source = demo_source.replace("/***## %s ##***/" % handle, source_code.get(handle, ""))
        # 写入目标
        code_target.write(demo_source)
        code_target.close()
        self.source_code = self.session_storage.get_file_path(target_name)
        return self._normal_judge()

    # 标准判题实现
    def _normal_judge(self):
        """
        正常判题模式
        :return:
        """
        lang = self.status.lang
        # 载入最终的代码
        fcode = open(self.source_code, "r")
        usercode = fcode.read()
        fcode.close()
        # 保存最终的代码到测试结果
        self.judge_result.finally_code = usercode
        # 编译代码
        cp_rel = self._compile_code(lang)
        if not cp_rel:
            return False
        # 对测试数据进行排序
        self.config.test_cases.sort(key=lambda x: x.order)
        # 拉取测试数据的Storage
        tc_storage = self.problem_storage.get_child_storage("test_cases")
        # 结果代码列表
        exitcodes = []
        # 计算有多少组有效数据
        cases_len = 0
        for case in self.config.test_cases:
            if not case.available:
                continue
            cases_len += 1
        # 判题轮询
        for case in self.config.test_cases:
            # 未启用的测试数据
            if not case.available:
                continue
            # 处理 TestCse
            stop_sig, exit_code = self._judge_testcase(tc_storage, case)
            if exit_code is not None:
                # 加入到退出列表
                exitcodes.append(exit_code)
            if not stop_sig:
                # 终止信号
                break

        pe_count = 0
        ac_count = 0
        wa_count = 0
        for exitcode in exitcodes:
            # 如果，不是AC、PE、WA
            if exitcode not in [
                system.WEJUDGE_JUDGE_EXITCODE.AC,
                system.WEJUDGE_JUDGE_EXITCODE.PE,
                system.WEJUDGE_JUDGE_EXITCODE.WA
            ]:
                # 直接应用
                self.judge_result.exitcode = exitcode
                return True

            # 如果遇到PE
            if exitcode == system.WEJUDGE_JUDGE_EXITCODE.PE:
                pe_count += 1
            # 如果遇到AC
            if exitcode == system.WEJUDGE_JUDGE_EXITCODE.AC:
                ac_count += 1
            # 如果遇到WA
            if exitcode == system.WEJUDGE_JUDGE_EXITCODE.WA:
                wa_count += 1

        # 在严格判题模式下，由于第一组数据不是AC就会直接报错，如果第一组数据PE，就直接报PE了，而后面的数据没运行。
        # 所以下面就改善这个情况
        t_count = pe_count + ac_count + wa_count
        # 如果样例没有跑完
        if t_count != cases_len:
            self.judge_result.exitcode = system.WEJUDGE_JUDGE_EXITCODE.WA
        # 如果样例跑完了，就按情况讨论
        else:
            if wa_count > 0:    # 如果存在WA，报WA
                self.judge_result.exitcode = system.WEJUDGE_JUDGE_EXITCODE.WA
            elif pe_count > 0:  # 这里不会再存在WA了，如果PE > 0，报PE
                self.judge_result.exitcode = system.WEJUDGE_JUDGE_EXITCODE.PE
            else:
                self.judge_result.exitcode = system.WEJUDGE_JUDGE_EXITCODE.AC

        return True

    # 处理每一个Test Case
    def _judge_testcase(self, tc_storage, case):
        """
        处理每一个Test Case
        :param tc_storage:      Test Case 存储点
        :param case:            Test Case
        :return:
        """
        if self.config.special_judge == system.WEJUDGE_SPECIAL_JUDGE_INTERACTIVE:
            # 交互式评测调用
            result = self._run_interactive(tc_storage, case)
        else:
            result = self._run(tc_storage, case)
        # 记录信息
        self.judge_result.details.append(result)
        self.judge_result.memused = max(result.memory_used, self.judge_result.memused)
        self.judge_result.timeused = max(result.time_used, self.judge_result.timeused)

        # 对于Python语言
        if self.status.lang in [
            system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.PYTHON2,
            system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.PYTHON3
        ]:
            if result.judge_result == system.WEJUDGE_JUDGE_EXITCODE.CE:
                self.judge_result.ceinfo += result.re_msg

        # 获取目标输出文件位置
        target_out_file_path = self.output_storage.get_file_path("%s.out" % case.handle)
        # 保存评测状态
        self.judge_result_storage.clone_from_file("%s.outdata" % case.handle, target_out_file_path)

        if result.judge_result != system.WEJUDGE_JUDGE_EXITCODE.AC:
            # 非严格模式，PE、WA继续判题
            if (not self.options.get('strict_mode', True)) and (result.judge_result in [
                system.WEJUDGE_JUDGE_EXITCODE.PE, system.WEJUDGE_JUDGE_EXITCODE.WA
            ]):
                return True, result.judge_result
            else:
                return False, result.judge_result

        return True, result.judge_result

    # 编译代码
    def _compile_code(self, lang):
        """
        编译代码
        :param lang:
        :return:
        """
        # 这三个语言是要编译的，其他的跳过
        if lang in [
            system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.GCC,
            system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.GCC_CPP,
            system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.JAVA
        ]:
            _log("RUN COMPILE [%s]" % self.source_code)
            source_code_list = [self.source_code]
            # Java语言处理
            if lang == system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.JAVA:
                self.java_class_name = get_java_class_name(self.judge_result.finally_code)
                if self.java_class_name is False:
                    self.judge_result.exitcode = system.WEJUDGE_JUDGE_EXITCODE.CE
                    self.judge_result.ceinfo = "Java类名称错误，请确认你的代码是否存在“public class 类名”，是否拼写错误，或者不是合法的Java标识符。"
                    return False
                # 编译文件夹目录的路径
                java_file_name = "%s.java" % self.java_class_name
                source_code_list = ["%s/%s" % (self.program_storage.get_current_path(), java_file_name)]
                self.target_program = self.program_storage.get_current_path()       # Java的包目录

                fp = self.program_storage.open_file(java_file_name, "w")            # 写入最终代码
                fp.write(self.judge_result.finally_code)
                fp.close()

            else:
                # 编译目标文件的路径
                self.target_program = self.program_storage.get_file_path("target")

            # GCC & GNU CPP
            if lang in (system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.GCC, system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.GCC_CPP):
                # 读取Library模块文件列表
                library_storage = self.problem_storage.get_child_storage("library")
                for item in self.config.library_cases:
                    tar = self.program_storage.get_file_path(item)
                    library_storage.clone_to_file(item, tar)
                    source_code_list.append(tar)

            # 注意第1个参数要传入1个数组，因为是代码源文件列表！
            rel, msg = compiler(
                source_code_list,
                self.target_program,
                system.WEJUDGE_COMPILER_COMMAND.get(lang)      # 注意转换，因为数据库中对于语言的定义是int类型
            )
            # 编译失败
            if not rel:
                self.judge_result.exitcode = system.WEJUDGE_JUDGE_EXITCODE.CE
                self.judge_result.ceinfo = msg
                return False
        else:
            self.target_program = self.source_code

        return True

    # 执行交互式评测
    def _run_interactive(self, tc_storage, case):
        """
        执行交互式评测
        :param tc_storage:      Test Case 存储点
        :param case:            Test Case
        :return:
        """
        _log("RUN INTERACTIVE TESTCASE[%s]" % case.handle)
        # 获取对应语言的运行参数
        run_args = self.__get_run_args()
        if run_args is None:
            raise OSError("Run Args Error")
        # 创建测试结果
        result = JudgeResultDetailItem()
        result.handle = case.handle
        # 获取时间限制
        tl, ml = self.__get_time_mem_limit()

        runcfg = {
            'args': run_args,  # 运行程序文件
            'fd_in': 0,
            'fd_out': 0,
            'timelimit': tl,
            'memorylimit': ml,
            'special_judge_checker': [
                self.special_judge.get_file_path(self.config.special_judger_program),
                tc_storage.get_file_path("%s.in" % case.handle),
                tc_storage.get_file_path("%s.out" % case.handle),
                self.output_storage.get_file_path("%s.out" % case.handle)
            ]
        }
        # 运行交互式评测
        rst = lorun.run_interactive(runcfg)

        _log("RUN INTERACTIVE FINISHED")
        # 获取运行数据
        result.re_signum = rst.get('re_signum', 0)
        result.re_call = rst.get('re_call', 0)
        result.re_file_flag = rst.get('re_file_flag', 0)
        result.re_file = rst.get('re_file', "")
        result.time_used = rst.get('timeused', 0)
        result.memory_used = rst.get('memoryused', 0)
        result.judge_result = rst.get('result', -1)
        return result

    # 执行lorun-run
    def _run(self, tc_storage, case, no_check=False):
        """
        执行lorun-run
        :param tc_storage:      Test Case 存储点
        :param case:            Test Case
        :param no_check:        禁用检查功能
        :return:
        """
        _log("RUN TESTCASE[%s]" % case.handle)
        # 打开测试用例文件
        in_file = tc_storage.open_file("%s.in" % case.handle, "r")
        target_out_file = self.output_storage.open_file("%s.out" % case.handle, "w+")
        err_out_file = self.output_storage.open_file("%s.err" % case.handle, "w+")
        # 获取对应语言的运行参数
        run_args = self.__get_run_args()
        if run_args is None:
            raise OSError("Run Args Error")
        # 创建测试结果
        result = JudgeResultDetailItem()
        result.handle = case.handle
        # 获取时间限制
        tl, ml = self.__get_time_mem_limit()

        runcfg = {
            'args': run_args,  # 运行程序文件
            'fd_in': in_file.fileno(),
            'fd_out': target_out_file.fileno(),
            'fd_err': err_out_file.fileno(),
            'timelimit': tl,
            'memorylimit': ml
        }
        # 运行程序
        rst = lorun.run(runcfg)
        # 关闭文件
        in_file.close()
        target_out_file.close()
        err_out_file.close()
        _log("RUN FINISHED")
        # 获取运行数据
        result.re_signum = rst.get('re_signum', 0)
        result.re_call = rst.get('re_call', 0)
        result.re_file_flag = rst.get('re_file_flag', 0)
        result.re_file = rst.get('re_file', "")
        result.time_used = rst.get('timeused', 0)
        result.memory_used = rst.get('memoryused', 0)
        result.re_msg = ""
        err_out_file = self.output_storage.open_file("%s.err" % case.handle, "r")
        # 获取stderr的输出
        if err_out_file is not None:
            result.re_msg = err_out_file.read()
            err_out_file.close()
        # 如果AC则执行数据检查
        if rst.get('result', -1) == 0:
            # 对于Python语言
            if self.status.lang in [
                system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.PYTHON2,
                system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.PYTHON3
            ]:
                # 如果有错误报告，直接报CE
                if len(result.re_msg) > 0 or result.re_msg.strip() != "":
                    if 'SyntaxError' in result.re_msg \
                            or 'IndentationError' in result.re_msg \
                            or 'ImportError' in result.re_msg:
                        result.judge_result = system.WEJUDGE_JUDGE_EXITCODE.CE
                        return result
                    else:
                        result.judge_result = system.WEJUDGE_JUDGE_EXITCODE.RE
                        return result
            # 如果禁用了数据检查，直接返回
            if no_check:
                result.judge_result = rst.get('result', -1)
                return result
            # 运行结束(RUN-AC)
            if self.config.special_judge == system.WEJUDGE_SPECIAL_JUDGE_CHECKER:
                # 需要special judge
                checkcfg = {
                    'args': run_args,  # 运行程序文件
                    'fd_in': 0,
                    'fd_out': 0,
                    'timelimit': tl,
                    'memorylimit': ml,
                    'special_judge_checker': [
                        self.special_judge.get_file_path(self.config.special_judger_program),
                        tc_storage.get_file_path("%s.in" % case.handle),
                        tc_storage.get_file_path("%s.out" % case.handle),
                        self.output_storage.get_file_path("%s.out" % case.handle)
                    ]
                }
                _log("RUN SPECLAI JUDGE")
                # 运行特殊评测检查器
                rst = lorun.run_checker(checkcfg)
                rel = rst.get("result", -1)
                # 如果无需运行通用检查器
                if rel != system.WEJUDGE_JUDGE_EXITCODE.SPJFIN:
                    result.judge_result = rel
                    return result

            # 只读打开运行结果文件
            ftemp = self.output_storage.open_file("%s.out" % case.handle, "r")
            # 只读打开测试数据输出样例文件
            fout = tc_storage.open_file("%s.out" % case.handle, "r")

            _log("RUN TEXT CHECKER")
            # 调用Lorun的检查模块检查答案错误
            rst = lorun.check(fout.fileno(), ftemp.fileno())
            # 释放文件
            fout.close()
            ftemp.close()
            result.judge_result = rst.get('result', -1)
            result.same_lines = rst.get('same_lines')
            result.total_lines = rst.get('total_lines')

        else:
            result.judge_result = rst.get('result', -1)

        return result

    # 返回资源限制内容
    def __get_time_mem_limit(self):
        """
        返回资源限制内容
        :param lang: 编译语言
        :return:
        """
        lang = str(self.status.lang)
        return self.config.time_limit.get(str(lang), 1000), self.config.mem_limit.get(str(lang), 32768)

    # 获取运行参数
    def __get_run_args(self):
        """
        获取运行参数
        :return:
        """
        # JAVA
        if self.status.lang == system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.JAVA:
            args = [
                'java', '-client',
                '-Dfile.encoding=utf-8', '-classpath', self.target_program,  # 注意， 这里self.target_program指代一个目录
                self.java_class_name
            ]
        # C\C++
        elif self.status.lang in [
            system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.GCC,
            system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.GCC_CPP
        ]:
            args = [self.target_program]
            pass
        # PYTHON 2
        elif self.status.lang == system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.PYTHON2:
            args = ["python", self.target_program]
        # PYTHON 3
        elif self.status.lang == system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.PYTHON3:
            args = ["python3", self.target_program]
        else:
            args = None
        return args