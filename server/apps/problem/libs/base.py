# -*- coding: utf-8 -*-
# coding:utf-8

import json
from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from wejudge.utils import tools
from django.db.models import Q
import apps.problem.models as ProblemModel

__author__ = 'lancelrq'


class ProblemBaseController(WeJudgeControllerBase):

    def __init__(self, request, response):
        self.problem_set = None
        self.problem_set_item = None
        self.problem = None
        self.status = None
        self.classify = None
        super(ProblemBaseController, self).__init__(request, response)

    # 读取题目集的信息
    def get_problemset(self, psid):
        """
        读取题目集的信息
        :param psid:
        :return:
        """
        item = ProblemModel.ProblemSet.objects.filter(id=psid)
        if item.exists():
            self.problem_set = item[0]
        else:
            raise WeJudgeError(2000)                # 找不到题目集

    # 获取problem信息
    def get_problem(self, pid):
        """
        获取problem信息
        :param pset:    ProblemSet对象
        :param pid:     如果pset对象不为None，则视作是Problemset Item的id，否则视作Problem Entity的id
        :return:
        """
        pset = self.problem_set
        if pset is None:
            problem_item = ProblemModel.Problem.objects.filter(id=pid)
        else:
            problem_item = pset.items.filter(id=pid)

        if not problem_item.exists():
            raise WeJudgeError(2001)  # 找不到题目信息

        problem_item = problem_item[0]
        self.problem_set_item = problem_item if hasattr(problem_item, "entity") else None
        self.problem = problem_item.entity if hasattr(problem_item, "entity") else problem_item

    # 获取Status信息
    def get_status(self, sid):
        """
        获取Status信息
        :param sid:
        :return:
        """
        status_item = ProblemModel.JudgeStatus.objects.filter(id=sid)
        if status_item.exists():
            self.status = status_item[0]
        else:
            raise WeJudgeError(2004)

    # 获取评测历史
    def _get_judge_status(self, model_obj=None, hide_detail=False):
        """
        获取评测历史
        :param model_obj:   继承JudgeStatusBase的模型接口
        :param hide_detail: 隐藏时间、内存和代码，这个对于比赛服是有用的
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
            model_object=model_obj,
            page=pagination.get("page", 1),
            limit=pagination.get("limit", system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_status_item(status):

            item = status.json(items=[
                "id", "flag", "lang", "create_time", "exe_time", "exe_mem", "code_len",
                "problem", "author", "problem_id", "author__nickname", "author__realname",
                "author__id", "author__sex", "virtual_problem", "virtual_problem__id",
                "virtual_problem__index", "author__username"
            ], timestamp=False)
            item['strict_mode'] = True
            if status.virtual_problem is not None:
                if hasattr(status.virtual_problem, 'strict_mode'):
                    item['strict_mode'] = status.virtual_problem.strict_mode
            if hide_detail:
                item['exe_time'] = '---'
                item['exe_mem'] = '---'
                item['code_len'] = '---'

            item['lang'] = system.WEJUDGE_PROGRAM_LANGUAGE_CALLED.get(item['lang'])
            return item

        data = proc_status_item()

        data['flag_desc'] = system.WEJUDGE_JUDGE_STATUS_DESC

        return data

    # 评测历史过滤器
    def _judge_status_filter(self, status_list):
        """
        评测历史过滤器
        :param status_list:
        :return:
        """
        parser = ParamsParser(self._request)
        keyword = parser.get_str('problem_id', '')
        author_id = parser.get_str('author_id', '')
        flag = parser.get_int('flag', -3)
        asc = parser.get_boolean('asc', default=False)

        if flag > -3:
            status_list = status_list.filter(flag=flag)

        if (author_id is not None) and (author_id.strip() != ""):
            status_list = status_list.filter(
                Q(author__nickname=author_id) |
                Q(author__realname=author_id) |
                Q(author__username=author_id)
            )

        if (keyword is not None) and (keyword.strip() != ""):

            if tools.is_numeric(keyword):
                status_list = status_list.filter(
                    Q(problem__title__contains=keyword) |
                    Q(problem__id=keyword) |
                    Q(virtual_problem__id=keyword)
                )
            else:
                idx = tools.char_to_index(keyword)
                if idx > 0:
                    status_list = status_list.filter(
                        Q(virtual_problem__index=idx)
                    )
                else:
                    status_list = status_list.filter(
                        Q(problem__title__contains=keyword)
                    )

        if asc:
            status_list = status_list.order_by('id')
        else:
            status_list = status_list.order_by('-id')

        return status_list.all()

    # ==== 功能部分 ====

    # 保存代码，返回保存的地址
    def _save_code_upload(self, lang, code):
        """
        保存代码，返回保存的地址
        :param code:        代码内容
        :param lang:        评测语言ID
        :return:
        """
        problem_id = self.problem.id
        file_uuid = tools.uuid1()
        file_name = "%s%s" % (file_uuid, system.WEJUDGE_CODE_FILE_EXTENSION.get(lang))
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CODE_SUBMIT, str(problem_id))
        storage = storage.get_child_storage(str(lang))
        storage = storage.get_child_storage(file_uuid[0])
        fp = storage.open_file(file_name, "w")
        fp.write(code)
        fp.close()
        return storage.get_file_path(file_name)

    # dump评测配置信息到文件
    def _dump_judge_configuation_to_file(self):
        """
        将Judge配置信息Dump到文件
        :return:
        """
        try:
            root_storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(self.problem.id))
            fp = root_storage.open_file("judge.json", "w")
            fp.write(self.problem.judge_config)
            fp.close()
        except Exception as ex:
            logging.error("写入Judge配置信息到文件失败! [%s] " % str(ex))
            return False

    # load评测配置信息
    def _load_judge_configuation(self, problem):
        """
        载入JudgeConfig
        :return:
        """
        try:
            config = JudgeConfig(problem.judge_config)
            return config
        except Exception as ex:
            logging.error("读取题目配置信息失败 [%s] " % str(ex))
            return None

    # save评测配置信息
    def _save_judge_configuation(self, config):
        """
        载入JudgeConfig
        :return:
        """
        try:
            self.problem.judge_config = config.dump_json()
            self.problem.save()
            return True
        except Exception as ex:
            logging.error("读取题目配置信息失败 [%s] " % str(ex))
            return False

    # 获取题目配置的Storage
    def _get_problem_storage(self, problem, package=None):
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(problem.id))
        if package is not None:
            return storage.get_child_storage(package)
        else:
            return storage

    # 获取评测设置信息
    def _get_judge_config(self, problem):
        """
        获取评测设置信息
        :return:
        """
        config = self._load_judge_configuation(problem)
        config_content = config.dump()

        config_content['pause_judge'] = problem.pause_judge
        config_content['permission'] = problem.permission
        config_content['lang'] = problem.lang

        code_storage = self._get_problem_storage(problem, "code_cases")

        # 填空模式
        if problem.problem_type == system.WEJUDGE_JUDGE_TYPE_FILL:

            dc_list = config.dump_demo_cases()
            demo_code_list = {}
            demo_answer_list = {}

            for k, v in dc_list.items():
                # k 是编译语言的代码，通过此代码获取到该语言的.demo文件，以及.demo.answer文件
                # v 是表示测试用例的列表，是一个列表！（这里也不怎么需要这个参数，放着先）
                fn_demo = "%s.demo" % k
                fn_answer = "%s.demo.answer" % k

                if code_storage.exists(fn_demo):
                    fp = code_storage.open_file(fn_demo)
                    demo_code_list[k] = fp.read()
                    fp.close()

                if code_storage.exists(fn_answer):
                    fp = code_storage.open_file(fn_answer)
                    # 由于存在多组数据，所以是以json方式存储的
                    try:
                        demo_answer_list[k] = json.loads(fp.read())
                    except:
                        demo_answer_list[k] = ""
                    fp.close()

            # DemoCases的答案映射列表
            config_content["demo_answer_cases"] = demo_answer_list
            config_content["demo_code_cases"] = demo_code_list

        elif problem.problem_type == system.WEJUDGE_JUDGE_TYPE_NORMAL:
            # 标准模式下，所有的代码示例文件都是以.answer结尾
            answer_list = {}
            for k in system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.langs():
                fn = "%s.answer" % k
                if code_storage.exists(fn):
                    fp = code_storage.open_file(fn)
                    answer_list[k] = fp.read()
                    fp.close()
            config_content["answer_cases"] = answer_list

        return config_content

    # 初始化题目配置目录
    def _init_problem_dir(self):
        """
        初始化题目配置目录
        :param problem_entity: Problem Entity
        :return:
        """
        try:
            root_storage = self._get_problem_storage(self.problem)
            root_storage.new_folder("test_cases")
            root_storage.new_folder("env")
            root_storage.new_folder("special_judge")
            root_storage.new_folder("library")
            root_storage.new_folder("code_cases")

            fp = root_storage.open_file("judge.conf", "w")
            fp.write(self.problem.judge_config)
            fp.close()
        except Exception as ex:
            logging.error("初始化题目配置目录失败! [%s] " % str(ex))
            return False

        return True

    # 将题目推送到指定题目集(已内部控制权限)
    def _publish_to_problemset(self, problem, target_pset):
        """
        将题目推送到指定题目集
        :return:
        """
        user = self.session.account

        if not user.permission_administrator:
            # 如果不是题目作者，不能执行这个操作
            if problem.author != user:
                raise WeJudgeError(2102)
            # 如果是题目作者，但是不是这个"已禁用推送题目的题目集"的管理员
            if target_pset.publish_private and target_pset.manager != user:
                raise WeJudgeError(2107)

        # 推送题目已经存在
        if target_pset.items.filter(entity=problem).exists():
            raise WeJudgeError(2105)

        # 检查如果题目被移除，那把该题目的信息再刷关联回去
        old_choose = ProblemModel.ProblemSetItem.objects.filter(problemset=target_pset, entity=problem)
        if old_choose.exists():
            old_choose = old_choose[0]
            target_pset.items.add(old_choose)

        else:
            # 新建AProblem信息
            pi = ProblemModel.ProblemSetItem()
            pi.entity = problem
            pi.problemset = target_pset
            pi.save()
            target_pset.items.add(pi)

        target_pset.items_count = target_pset.items.count()
        target_pset.save()

    # 从题库中移除题目(已内部控制权限)
    def _remove_from_problemset(self, problem, target_pset):
        """
        从题库中移除题目
        :return:
        """
        user = self.session.account
        # 如果不是管理员、题目作者或者是题库管理员，那就抛异常
        if not user.permission_administrator and problem.author != user and target_pset.manager != user:
            raise WeJudgeError(2106)

        p = target_pset.items.filter(entity=problem)
        if not p.exists():
            raise WeJudgeError(2001)

        target_pset.items.remove(p[0])
        target_pset.items_count = target_pset.items.count()
        target_pset.save()
        return True

    # ==== 权限部分 ====

    # 题目库管理权限检查实现（在别的地方可以重写！）
    def check_problemset_manager_privilege(self, throw=True):
        """
        题目库管理权限检查实现
        :param throw: 错误是否抛出
        :return:
        """
        if self.session.account.permission_administrator:
            return True
        if self.problem_set is not None:
            # 如果题目集是当前用户创建的，无论如何都具有管理权限
            if self.problem_set.manager == self.session.account:
                return True
            else:
                if throw:
                    raise WeJudgeError(2101)
                else:
                    return False
        else:
            # 创建题目集的时候
            if not self.session.account.permission_create_problemset:
                # 检查用户是否有管理题目集的权限
                if throw:
                    raise WeJudgeError(2101)
                else:
                    return False
        return True

    # 题目访问和管理权限检查实现（在别的地方可以重写！）
    def check_problem_privilege(self, privilege_code=1, throw=True):
        """
        题目访问和管理权限检查实现
        :param throw:
        :param privilege_code: 权限请求值，定义如下：
        > 0 == 不请求权限
        > 1 == read    访问题目内容，查看统计
        > 2 == judge   提交评测
        > 4 == data    访问题目示例代码、测试数据、设置等，同时也运行访问所有此题目的评测历史详情
        > 8 == write   修改题目内容、示例代码、测试数据、设置等
        :return:
        """
        user = self.session.account
        # 系统管理员无限权限
        if user is not None and user.permission_administrator:
            return True
        # 如果是修改和管理题目
        if self.problem is not None:
            if user is not None and self.problem.author == user:
                # 如果题目的作者是当前登录账户的话
                return True
            else:
                if privilege_code == 0:
                    return True
                if privilege_code > 0:
                    if privilege_code > 2:
                        # 这一步是要检查管理权限的
                        if user is not None and user.permission_publish_problem:
                            if tools.check_privilege(privilege_code, self.problem.permission):
                                # 检查混合权限请求
                                return True
                    else:
                        # 这一步不需要检查管理权限
                        if tools.check_privilege(privilege_code, self.problem.permission):
                            # 检查混合权限请求
                            return True
        # 如果是新建题目
        else:
            # 检查用户是否有发布题目的权限
            if user.permission_publish_problem:
                return True

        if throw:
            raise WeJudgeError(2201)
        else:
            return False

    # 题目集访问权限检查实现（在别的地方可以重写！）
    def check_problemset_privilege(self, throw=True):
        """
        题目访问和管理权限检查实现
        :param throw:
        :return:
        """
        user = self.session.account
        # 系统管理员无限权限
        if user is not None and user.permission_administrator:
            return True

        if self.problem_set is not None:
            # 完全私有模式
            if self.problem_set.private == 2:
                if user == self.problem_set.manager:
                    return True
            # 高级共享
            elif self.problem_set.private == 1:
                # 如果有发布题目或创建题集的权限，就允许查看
                if user is not None and user.permission_publish_problem:
                    return True
                if user is not None and user.permission_create_problemset:
                    return True
            else:
                return True
        else:
            # 不在题库的模式：如果是发布者
            if self.problem.author == self.session.account:
                return True
            else:
                raise WeJudgeError(2001)

        if throw:
            raise WeJudgeError(2100)
        else:
            return False

    # 评测历史访问权限鉴定（可重写）
    def judge_status_privilege(self, throw=True):
        """
        评测历史访问权限鉴定（可重写）
        :param throw:
        :return:
        """
        status = self.status
        user = self.session.account  # master
        problem = self.status.problem  # ProblemEntity
        if status.author == user:
            return True
        else:
            # 对于非评测归属用户

            # 用户是题目发布者
            if user == problem.author or user.permission_administrator:
                return True
            # 用户是拥有发布题目权限的，那就看有没有阅读数据的权限
            if user.permission_publish_problem and tools.check_privilege(4, problem.permission):
                return True

        if throw:
            raise WeJudgeError(2008)
        else:
            return False

    # 题目访问和管理权限检查器
    @staticmethod
    def problem_privilege_validator(privilege_code):
        """
        题目访问和管理权限检查器
        :return:
        """
        def d(func):
            def wrapper(*args, **kwargs):
                self = args[0]
                self.check_problem_privilege(privilege_code=privilege_code)
                return func(*args, **kwargs)
            return wrapper
        return d

    # 题目集访问权限检查装饰器
    @staticmethod
    def problemset_privilege_validator(func):
        """
        题目集访问权限检查装饰器
        :return:
        """
        def wrapper(*args, **kwargs):
            self = args[0]
            self.check_problemset_privilege()
            return func(*args, **kwargs)

        return wrapper

    # 题目库管理权限检查装饰器
    @staticmethod
    def problemset_manager_validator(func):
        """
        题目库管理权限检查器
        :return:
        """

        def wrapper(*args, **kwargs):
            self = args[0]
            self.check_problemset_manager_privilege()
            return func(*args, **kwargs)

        return wrapper


    # 评测历史访问权限鉴定装饰器
    @staticmethod
    def judge_status_privilege_validator(func):
        """
        评测历史访问权限鉴定装饰器
        :return:
        """
        def wrapper(*args, **kwargs):
            self = args[0]
            self.judge_status_privilege()
            return func(*args, **kwargs)

        return wrapper
