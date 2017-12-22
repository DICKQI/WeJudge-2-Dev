# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'


from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from wejudge.utils import tools
import apps.contest.models as ContestModel
import apps.problem.models as ProblemModel
from apps.contest.libs import ContestBaseController
from apps.problem.libs.base import ProblemBaseController


class ContestController(ContestBaseController, ProblemBaseController):

    def __init__(self, request, response, cid):
        super(ContestController, self).__init__(request, response, cid)

    # 创建比赛
    @staticmethod
    def create_contest(request, master_user):

        parser = ParamsParser(request)
        title = parser.get_str("title", require=True, method="POST", errcode=5251)
        start_time = parser.get_datetime("start_time", require=True, method="POST", errcode=5252)
        end_time = parser.get_datetime("end_time", require=True, method="POST", errcode=5253)
        sponsor = parser.get_str("sponsor", '', method="POST")

        contest = ContestModel.Contest()
        contest.title = title
        contest.start_time = start_time
        contest.end_time = end_time
        contest.sponsor = sponsor

        contest.save()

        mgr_account = ContestModel.ContestAccount()
        mgr_account.contest = contest
        mgr_account.username = 'admin'
        mgr_account.role = 2
        mgr_account.nickname = '比赛发起人'
        mgr_account.realname = '比赛发起人'
        mgr_account.master = master_user
        mgr_account.save()

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CONTEST_STORAGE, str(contest.id))

    # 保存比赛选题
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    def save_problem_choosing(self):
        """
        保存比赛选题
        :return:
        """
        parser = ParamsParser(self._request)
        problem_ids = parser.get_list("problem_ids", method="POST")

        result = {}

        for pid in problem_ids:
            problem = ProblemModel.Problem.objects.filter(id=pid)
            if not problem.exists():
                result[pid] = 1
                continue
            problem = problem[0]
            if self.contest.problems.filter(entity=problem).exists():
                result[pid] = 2
                continue
            # 检查如果题目被移除，那把该题目的信息再刷关联回去
            old_choose = ContestModel.ContestProblem.objects.filter(contest=self.contest, entity=problem)
            if old_choose.exists():
                old_choose = old_choose[0]
                self.contest.problems.add(old_choose)
            else:
                # 新建AProblem信息
                ap = ContestModel.ContestProblem()
                ap.entity = problem
                ap.contest = self.contest
                ap.index = self.contest.problems.count() + 1
                ap.lang = self.contest.lang
                ap.save()
                self.contest.problems.add(ap)

            self.contest.save()
            result[pid] = 3

        return result

    # 获取比赛列表（不用创建对象）
    @staticmethod
    def get_contest_list(request):
        """
        获取比赛列表（不用创建对象）
        :param request:
        :return:
        """

        parser = ParamsParser(request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', 20)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        @WeJudgePagination(
            model_object=ContestModel.Contest.objects.order_by('-id'),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 20),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_contest_item(_contest):
            view = _contest.json(items=(
                "title", "start_time", "end_time", "sponsor"
            ), timestamp=False)
            flag, delta = tools.check_time_passed(_contest.start_time, _contest.end_time)
            view['status'] = flag
            return view

        result = proc_contest_item()

        return result

    # 比赛设置信息
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    def get_contest_settings(self):
        """
        比赛设置信息
        :return:
        """
        cross_check_ignore_problem = [x.id for x in self.contest.cross_check_ignore_problem.all()]
        contest_info = self.contest.json(items=[
            'title', 'start_time', 'end_time', 'sponsor', 'pause', 'lang', 'access_token',
            'penalty_items', 'penalty_time', 'rank_list_stop_at', 'hide_problem_title', 'enable_printer_queue',
            'cross_check', 'cross_check_ratio', 'cross_check_public', 'cross_check_public_ratio',
            'archive_lock', 'register_mode', 'rank_list_show_items'
        ])
        contest_info['cross_check_ignore_problem'] = cross_check_ignore_problem
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CONTEST_STORAGE, str(self.contest.id))
        if storage.exists('intro.html'):
            fp = storage.open_file('intro.html','r')
            des = fp.read()
            fp.close()
        else:
            des = ''
        contest_info['description'] = des

        contest_view = {
            "contest": contest_info,
            "problems": [x.json(items=[
                "id", "entity", "entity__id", "entity__title", "index",
            ]) for x in self.contest.problems.order_by('index')]
        }
        return contest_view

    # 保存比赛设置
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    def save_contest_settings(self):
        """
        保存比赛设置
        :return:
        """
        parser = ParamsParser(self._request)
        lang_list = parser.get_list("lang", method="POST")
        title = parser.get_str("title", require=True,method="POST", errcode=5251)
        start_time = parser.get_datetime("start_time", require=True, method="POST", errcode=5252)
        end_time = parser.get_datetime("end_time", require=True, method="POST", errcode=5253)
        rank_list_stop_at = parser.get_datetime("rank_list_stop_at", None, require=False, method="POST", errcode=5254)
        penalty_time = parser.get_int("penalty_time", require=True, min=0, method="POST", errcode=5255)
        pause = parser.get_boolean("pause", False, method="POST")
        hide_problem_title = parser.get_boolean("hide_problem_title", False, method="POST")
        archive_lock = parser.get_boolean("archive_lock", False, method="POST")
        access_token = parser.get_str("access_token", "", method="POST")
        register_mode = parser.get_str("register_mode", "", method="POST")
        contest_description = parser.get_str("description","",method="POST")
        rank_list_show_items = parser.get_int("rank_list_show_items", require=True, min=0, max=2, method="POST")

        sponsor = parser.get_str("sponsor", '', method="POST")
        penalty_items = parser.get_list("penalty_items", method="POST")

        cross_check = parser.get_boolean("cross_check", False, method="POST")
        cross_check_ratio = parser.get_float("cross_check_ratio", require=True, min=0.0, max=1.0, method="POST", errcode=5256)
        cross_check_public = parser.get_boolean("cross_check_public", False, method="POST")
        cross_check_public_ratio = parser.get_float("cross_check_public_ratio", require=True, min=0.0, max=1.0, method="POST", errcode=5256)
        cross_check_ignore_problems = parser.get_list("cc_ig_problem", method="POST")

        enable_printer_queue = parser.get_boolean("enable_printer_queue", False, method="POST")

        penalty_items = ','.join(penalty_items)

        lang = 0
        for item in lang_list:
            if system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(item):
                lang = (lang | int(item))

        ph = penalty_time // 3600
        pm = (penalty_time // 60) % 60
        ps = penalty_time % 60

        import datetime
        penalty_time = datetime.time(ph, pm, ps)

        self.contest.title = title
        self.contest.lang = lang
        self.contest.start_time = start_time
        self.contest.end_time = end_time
        self.contest.penalty_time = penalty_time
        self.contest.sponsor = sponsor
        self.contest.penalty_items = penalty_items
        self.contest.hide_problem_title = hide_problem_title
        self.contest.access_token = access_token
        self.contest.penalty_items = penalty_items
        self.contest.pause = pause
        self.contest.cross_check = cross_check
        self.contest.cross_check_ratio = cross_check_ratio
        self.contest.cross_check_public = cross_check_public
        self.contest.cross_check_public_ratio = cross_check_public_ratio
        self.contest.rank_list_stop_at = rank_list_stop_at
        self.contest.enable_printer_queue = enable_printer_queue
        self.contest.register_mode = register_mode
        self.contest.archive_lock = archive_lock
        self.contest.rank_list_show_items = rank_list_show_items

        ignore_problems = self.contest.cross_check_ignore_problem.all()
        for ip in ignore_problems:
            if str(ip.id) not in cross_check_ignore_problems:
                self.contest.cross_check_ignore_problem.remove(ip)
            else:
                cross_check_ignore_problems.remove(str(ip.id))

        for pid in cross_check_ignore_problems:
            p = self.contest.problems.filter(id=pid)
            if p.exists():
                self.contest.cross_check_ignore_problem.add(p[0])

        self.contest.save()

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CONTEST_STORAGE,str(self.contest.id))
        fp = storage.open_file('intro.html','w')
        fp.write(contest_description)
        fp.close()

    # 获取比赛的题目列表
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    def get_contest_problems(self):
        """
        获取比赛的题目列表
        :return:
        """

        view_list = []

        user = self.session.account

        problems_list = self.contest.problems.order_by('index')

        field_list = [
            "id", "entity", "entity__title", "entity__id", "index", "accepted", "submission",
            "status_editable", "lang"
        ]
        if self.contest.hide_problem_title:
            field_list.remove("entity__title")

        for problem in problems_list:
            pitem = problem.json(items=field_list)
            if user.role == 0:
                sol = ContestModel.ContestSolution.objects.filter(contest=self.contest, author=user, problem=problem)
                if sol.exists():
                    sol = sol[0]
                    pitem["status"] = "%s / %s" % (sol.accepted, sol.submission)
                else:
                    pitem["status"] = None
            view_list.append(pitem)

        return {
            "data": view_list
        }

    # 保存题目的设置信息
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    def save_contest_problem_setting(self):
        """
        保存题目的设置信息
        :return:
        """
        parser = ParamsParser(self._request)
        lang_list = parser.get_list("lang", method="POST")
        index = parser.get_int("index", require=True, min=1, method="POST", errcode=5250)
        status_editable = parser.get_boolean("status_editable", True, method="POST")

        lang = 0
        for item in lang_list:
            if system.WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.exists(item):
                lang = (lang | int(item))

        self.contest_problem_item.index = index
        self.contest_problem_item.status_editable = status_editable
        self.contest_problem_item.lang = lang
        self.contest_problem_item.save()

        return True

    # 删除题目引用
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    @ContestBaseController.check_timepassed_validator(status__lt=0, errcode=5005, ignore_admin=False)
    def remove_contest_problem(self):
        """
        删除题目引用
        :return:
        """
        self.contest_problem_item.delete()

        return True

    # 添加题目引用
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    @ContestBaseController.check_timepassed_validator(status__lt=0, errcode=5005, ignore_admin=False)
    def add_contest_problem(self):
        """
        添加题目引用
        :return:
        """
        parser = ParamsParser(self._request)
        pid = parser.get_int("id", require=True, method="POST")

        p = ProblemModel.Problem.objects.filter(id=pid)
        if not p.exists():
            raise WeJudgeError(2001)

        if self.contest.problems.filter(entity__id=pid).exists():
            raise WeJudgeError(5263)

        p = p[0]

        cp = ContestModel.ContestProblem()
        cp.index = self.contest.problems.count() + 1
        cp.entity = p
        cp.lang = self.contest.lang
        cp.status_editable = False
        cp.save()

        self.contest.problems.add(cp)

        return True

    # 重判题目
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(2)
    def rejudge_contest_problem(self):
        """
        重判题目
        :return:
        """

        from .workers import contest_judge

        problem = self.contest_problem_item
        status_list = ContestModel.JudgeStatus.objects.filter(virtual_problem=problem, contest=self.contest)
        for status in status_list:
            contest_judge.delay(problem.entity.id, status.id, self.contest.id)

        return True

    # 比赛排行信息获取
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    def get_ranklist(self):
        """
        比赛排行信息获取
        :return:
        """


        if self.contest.rank_list_stop_at is not None:
            import json
            from django.utils.timezone import now

            storage = self.get_contest_storage()
            if self.contest.rank_list_stop_at <= now() and not storage.exists("rk1hrstop.snapshot"):
                from .workers import contest_ranklist_snapshot
                contest_ranklist_snapshot.delay(self.contest.id, "rk1hrstop.snapshot")

            # 启用：未登录，或者登陆身份为参赛者
            enable = (not self.session.is_logined()) or (self.session.account.role == 0)
            showtime = self.contest.end_time < now()

            if not showtime and enable and self.contest.rank_list_stop_at <= now():
                # 将要显示封榜情况
                if storage.exists("rk1hrstop.snapshot"):
                    try:
                        fp = storage.open_file("rk1hrstop.snapshot", 'r')
                        data = json.loads(fp.read())
                        fp.close()
                        return data
                    except:
                        raise WeJudgeError(5008)
                else:
                    raise WeJudgeError(5007)
            else:
                return ContestController.get_ranklist_data(self.contest)
        else:
            return ContestController.get_ranklist_data(self.contest)

    # 读取当前比赛的所有评测历史
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    def get_judge_status(self):
        """
        读取当前比赛的所有评测历史
        :return:
        """
        contest = self.contest

        status = contest.judge_status
        if self.check_rank_stop():
            status = status.filter(create_time__lte=self.contest.rank_list_stop_at)

        model_obj = self._judge_status_filter(status)

        hide_detail = not self.check_privilege(1, False)

        return self._get_judge_status(model_obj, hide_detail=hide_detail)

    # 获取FAQ列表
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    def get_faq_list(self):
        """
        获取FAQ列表
        :return:
        """

        def view_faq(_faq, is_root=True):
            view = _faq.json(items=[
                'id', 'author', 'author__id', 'author__nickname', 'author__username', 'title', 'content', 'is_private', 'create_time'
            ])
            if not is_root:
                return view

            children = []

            for c in _faq.children.order_by('id'):
                children.append(view_faq(c, False))

            view['children'] = children
            return view

        user = self.session.account
        faq_list = []

        if user.role in [1, 2]:
            faq_mine = ContestModel.FAQ.objects.filter(contest=self.contest, is_root=True).order_by('-id')
            for faq in faq_mine:
                faq_list.append(view_faq(faq))

        else:
            faq_public = ContestModel.FAQ.objects.filter(
                contest=self.contest, is_root=True, is_private=False
            ).order_by('-id')
            faq_mine = ContestModel.FAQ.objects.filter(
                contest=self.contest, is_root=True, author=user, is_private=True
            ).order_by('-id')

            for faq in faq_public:
                faq_list.append(view_faq(faq))
            for faq in faq_mine:
                faq_list.append(view_faq(faq))

        return faq_list

    # 回复FAQ
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status=0, errcode=5004)
    def reply_faq(self):
        """
        回复FAQ （不支持编辑！发错了自己删）
        :param fid:
        :return:
        """

        parser = ParamsParser(self._request)
        fid = parser.get_int("fid", require=True, method="POST")
        content = parser.get_str("content", require=True, method="POST", errcode=5212)

        user = self.session.account
        faq = self.get_faq(fid)

        if user.role not in [1, 2] and not faq.author == user:
            raise WeJudgeError(5211)

        reply = ContestModel.FAQ()
        reply.contest = self.contest
        reply.content = content
        reply.author = user
        reply.is_root = False
        reply.save()

        faq.children.add(reply)

    # 新建FAQ
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status=0, errcode=5004)
    def new_faq(self):
        """
        新建提问（不支持编辑！发错了自己删）
        :return:
        """
        user = self.session.account
        if user.role != 0:
            raise WeJudgeError(5211)

        parser = ParamsParser(self._request)
        title = parser.get_str("title", require=True, method="POST", errcode=5213)
        content = parser.get_str("content", '', method="POST")

        faq = ContestModel.FAQ()
        faq.contest = self.contest
        faq.content = content
        faq.author = user
        faq.is_root = True
        faq.is_private = True
        faq.title = title
        faq.content = content
        faq.save()

    # 删除FAQ
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status=0, errcode=5004)
    def delete_faq(self):
        """
        删除FAQ
        :return:
        """

        parser = ParamsParser(self._request)
        fid = parser.get_int("fid", require=True, method="GET")

        user = self.session.account
        faq = self.get_faq(fid, False)

        if user.role not in [1, 2] and not faq.author == user:
            raise WeJudgeError(5211)

        faq.delete()

    # 设置FAQ为公开或者私密
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status=0, errcode=5004)
    def change_faq_visable(self):
        """
        设置FAQ为公开或者私密
        :return:
        """

        parser = ParamsParser(self._request)
        fid = parser.get_int("fid", require=True, method="GET")

        user = self.session.account
        faq = self.get_faq(fid)

        if user.role not in [1, 2]:
            raise WeJudgeError(5211)

        faq.is_private = not faq.is_private
        faq.save()

    # 读取公告信息
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    def get_notice(self, nid):
        notice = ContestModel.Notice.objects.filter(contest=self.contest, id=nid)

        if notice.exists():
            return notice[0]
        else:
            raise WeJudgeError(5214)

    # 比赛公告
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    def get_notice_list(self):
        """
        获取FAQ列表
        :return:
        """

        notices = ContestModel.Notice.objects.filter(contest=self.contest).order_by('-id')
        return [x.json(items=[
            'id', 'author', 'author__nickname', 'content', 'create_time'
        ]) for x in notices]

    # 新建公告
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def new_notice(self):
        """
        新建公告（不支持编辑！发错了自己删）
        :return:
        """
        user = self.session.account

        parser = ParamsParser(self._request)
        content = parser.get_str("content", require=True, method="POST", errcode=5215)

        faq = ContestModel.Notice()
        faq.contest = self.contest
        faq.author = user
        faq.content = content
        faq.save()

    # 删除公告
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def delete_notice(self):
        """
        删除公告
        :return:
        """

        parser = ParamsParser(self._request)
        nid = parser.get_int("nid", require=True, method="GET")

        faq = self.get_notice(nid)

        faq.delete()

    # 获取比赛账户表
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def get_account_list(self):
        """
        获取比赛账户表
        :return:
        """
        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', 50)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        @WeJudgePagination(
            model_object=ContestModel.ContestAccount.objects.filter(contest=self.contest).order_by('-role'),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 50),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_item(_account):
            account = _account.json(items=[
                'id', 'role', 'clear_password', 'username', 'nickname',
                'realname', 'sex', 'finally_rank', 'ignore_rank', 'lock'
            ])
            return account

        account_view = proc_item()
        return account_view

    # 新增或编辑用户信息
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def edit_account(self):
        """
        新增或编辑用户信息
        :return:
        """
        parser = ParamsParser(self._request)
        uid = parser.get_int('id', require=True, method="POST")
        username = parser.get_str('username', require=True, method="POST", errcode=5257)
        password = parser.get_str('password', "", method="POST")
        nickname = parser.get_str('nickname', require=True, method="POST", errcode=5258)
        realname = parser.get_str('realname', require=True, method="POST", errcode=5259)
        role = parser.get_int('role', require=True, method="POST")
        sex = parser.get_boolean('sex', False, method="POST")
        ignore_rank = parser.get_boolean('ignore_rank', False, method="POST")
        save_clear_pwd = parser.get_boolean('save_clear_pwd', False, method="POST")

        uca = ContestModel.ContestAccount.objects.filter(contest=self.contest, username=username)

        if uid == 0:
            if uca.exists():
                raise WeJudgeError(5260)
            user = ContestModel.ContestAccount()
            user.contest = self.contest

            if password.strip() == "":
                password = tools.gen_random_pwd(8)

            if save_clear_pwd:
                user.clear_password = password

            user.password = tools.gen_passwd(password)

        else:
            user = ContestModel.ContestAccount.objects.filter(contest=self.contest, id=uid)
            if not user.exists():
                raise WeJudgeError(1000)

            user = user[0]

            if uca.exists() and uca[0] != user:
                raise WeJudgeError(5260)

            suser = self.session.account
            if user == suser:
                if role != suser.role:
                    raise WeJudgeError(5261)

            if password == "随机" or password == "random" or password == "rand":
                user.password = tools.gen_random_pwd(10)
                user.clear_password = user.password
            else:
                if password.strip() != "":

                    if save_clear_pwd:
                        user.clear_password = password

                    user.password = tools.gen_passwd(password)

        user.username = username
        user.nickname = nickname
        user.realname = realname
        user.role = role
        user.sex = 0 if sex else 1
        user.ignore_rank = ignore_rank
        user.save()

        # 新增或编辑用户信息

    # 从xls导入账户信息
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def xls_import_account(self):
        """
        从xls导入账户信息
        :return:
        """

        from django.db import transaction

        parser = ParamsParser(self._request)
        file = parser.get_file("uploadFile", require=True)

        storage = self.get_contest_storage()
        fp = storage.open_file("account.xls", "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        try:
            import xlrd
            xls_sheet = xlrd.open_workbook(storage.get_file_path("account.xls"))
            xls_table = xls_sheet.sheet_by_index(0)
            for i in range(2, xls_table.nrows):
                user_row = xls_table.row_values(i)
                team_id = user_row[0]
                if type(team_id) == float or type(team_id) == int:
                    team_id = str(int(team_id))
                if team_id.strip() == '':
                    continue
                team = ContestModel.ContestAccount.objects.filter(contest=self.contest, username=team_id)
                if team.exists():
                    team = team[0]
                    if user_row[1] == 'new':
                        password = tools.gen_random_pwd(10)
                        team.password = tools.gen_passwd(password)
                        team.clear_password = password

                    team.nickname = user_row[2]
                    team.realname = user_row[3]
                    team.sex = 0 if str(user_row[4]) == 'Y' else 1
                    team.ignore_rank = False if str(user_row[5]) == 'Y' else True
                    team.save()

                else:
                    logging.info("[tem:%s]" % team_id)
                    password = user_row[1]
                    if type(password) == float or type(password) == int:
                        password = str(int(password))
                    if password.strip() == "":
                        password = tools.gen_random_pwd(10)
                    try:
                        team = ContestModel.ContestAccount()
                        team.contest = self.contest
                        team.username = team_id
                        team.role = 0
                        team.nickname = user_row[2]
                        team.realname = user_row[3]
                        team.sex = 0 if str(user_row[4]) == 'Y' else 1
                        team.ignore_rank = False if str(user_row[5]) == 'Y' else True
                        team.password = tools.gen_passwd(password)
                        team.clear_password = password
                        team.locked = False
                        team.save()
                    except Exception as ex:
                        logging.info("[ERR]: %s" % str(ex) )
                        transaction.rollback()
                        continue
        except Exception as ex:
            logging.info("[XLS_ERR]: %s" % str(ex))
            return

    # 删除用户
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def delete_account(self):
        """
        删除用户
        :return:
        """

        parser = ParamsParser(self._request)
        uid = parser.get_int("id", require=True, method="GET")

        user = ContestModel.ContestAccount.objects.filter(contest=self.contest, id=uid)
        if not user.exists():
            raise WeJudgeError(1000)

        if user[0] == self.session.account:
            raise WeJudgeError(5262)

        user[0].delete()

    # 获取实时查重信息
    @ContestBaseController.login_validator
    def get_cross_check_list(self):
        """
        获取实时查重信息
        :return:
        """

        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', 50)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        if not self.check_privilege(role=1, throw=False):
            if not self.contest.cross_check_public:
                raise WeJudgeError(5217)

            self.check_timepassed(status=1, errcode=5006)
            cc_model = ContestModel.ContestCodeCrossCheck.objects.filter(
                contest=self.contest, levenshtein_similarity_ratio__gte=self.contest.cross_check_public_ratio
            ).order_by('-levenshtein_similarity_ratio')

        else:
            cc_model = ContestModel.ContestCodeCrossCheck.objects.filter(
                contest=self.contest).order_by('-levenshtein_similarity_ratio')

        @WeJudgePagination(
            model_object=cc_model,
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 50),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_item(_cc):
            cc = _cc.json(items=[
                'id', 'levenshtein_similarity_ratio', 'problem', 'problem__id', 'problem__index',
                'source', 'target', 'source__id', 'target__id', 'source__author',
                'source__author__nickname', 'source__author__realname','source__author__username',
                'target__author', 'target__author__username', 'target__author__nickname', 'target__author__realname'
            ])
            return cc

        cc_view = proc_item()
        return cc_view

    # 删除查重信息
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def delete_cross_check_record(self):
        """
        删除查重信息
        :return:
        """
        parser = ParamsParser(self._request)
        id = parser.get_int("id", require=True, method="GET")

        cc = ContestModel.ContestCodeCrossCheck.objects.filter(contest=self.contest, id=id)
        if not cc.exists():
            raise WeJudgeError(5216)

        cc[0].delete()

    # 查看查重代码对比
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def read_cross_check_code(self):
        """
        查看查重代码对比
        :return:
        """
        parser = ParamsParser(self._request)
        id = parser.get_int("id", require=True, method="GET")

        cc = ContestModel.ContestCodeCrossCheck.objects.filter(contest=self.contest, id=id)
        if not cc.exists():
            raise WeJudgeError(5216)

        cc = cc[0]

        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.CODE_SUBMIT, '')
        fp = storage.open_file(cc.source.code_path, 'r')
        code1 = fp.read()
        fp.close()

        fp = storage.open_file(cc.target.code_path, 'r')
        code2 = fp.read()
        fp.close()

        return {
            "source": {
                "code": code1,
                "status_id": cc.source.id
            },
            "target": {
                "code": code2,
                "status_id": cc.target.id
            }
        }

    # 确认最终排名
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def confirm_finally_rank(self):
        """
        确认最终排名
        :return:
        """
        accounts = ContestModel.ContestAccount.objects.filter(contest=self.contest, role=0) \
            .order_by('-rank_solved', 'rank_timeused')
        rank = 0
        for account in accounts:
            if account.ignore_rank:             # 不计算排名的
                continue
            if account.rank_solved == 0:        # 没过题的不排名
                continue
            rank += 1
            account.finally_rank = rank
            account.save()

    # 更新比赛服数据
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def refresh_contest_data(self):
        """
        更新比赛服数据
        :return:
        """
        from .workers import contest_refresh_all_data
        contest_refresh_all_data.delay(self.contest.id)

    # (Access)获取当前的SolutionList
    @ContestBaseController.check_readonly_access_token_validator
    def access_solution_list(self):
        """
        (Access)获取当前的SolutionList
        :return:
        """
        view_list = []

        solutions_list = ContestModel.ContestSolution.objects.filter(contest=self.contest)

        for solution in solutions_list:
            sitem = solution.json(items=[
                "id", "accepted", "submission", "penalty", "best_memory", "best_time",
                "best_code_size", "create_time", "first_ac_time", "is_first_blood",
                "used_time", "used_time_real", "author_id", "problem_id"
            ])
            view_list.append(sitem)

        return view_list

    # (Access)获取比赛的题目列表
    @ContestBaseController.check_readonly_access_token_validator
    def access_contest_problems(self):
        """
        (Access)获取比赛的题目列表
        :return:
        """

        view_list = []

        problems_list = self.contest.problems.order_by('index')

        for problem in problems_list:
            pitem = problem.json(items=[
                "id", "entity", "entity__title", "index", "accepted", "submission",
                "status_editable", "lang"
            ])
            view_list.append(pitem)

        return view_list

    # (Access)获取比赛的账户列表
    @ContestBaseController.check_readonly_access_token_validator
    def access_contest_accounts(self):
        """
        (Access)获取比赛的账户列表
        :return:
        """

        view_list = []

        account_list = ContestModel.ContestAccount.objects.filter(contest=self.contest)

        for account in account_list:
            aitem = account.json(items=[
                'id', 'username', 'nickname', 'realname', 'sex',
                'rank_solved', 'rank_timeused', 'finally_rank',
                'ignore_rank', 'role', 'clear_password'
            ])
            view_list.append(aitem)

        return view_list

    # 获取滚榜数据
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def get_rank_board_datas(self):
        """
        获取滚榜数据
        :return:
        """

        import time

        if self.contest.rank_list_stop_at is None:
            raise WeJudgeError(5009)

        contest = self.contest
        penalty_items = [int(i) for i in contest.penalty_items.split(",")]
        penalty_time = contest.penalty_time.hour * 3600 + contest.penalty_time.minute * 60 + contest.penalty_time.second
        contest_start_time = int(time.mktime(contest.start_time.timetuple()))

        #  缓存用户表
        user_list_table = ContestModel.ContestAccount.objects.filter(contest=self.contest, role=0)
        user_list = {user.id: {
            "username": user.username,
            "headimg": user.headimg,
            "nickname": "%s%s" % ("*" if user.ignore_rank else "", user.nickname),
            "realname": user.realname,
            "sex": user.sex
        } for user in user_list_table}

        # 获取题目数据
        cproblem_list = contest.problems.order_by("index")
        # 题目索引参照表
        cpindex_list = {}
        for cproblem in cproblem_list:
            cpindex_list[cproblem.id] = cproblem.index

        judge_status_lte_1hr = contest.judge_status.order_by("id").filter(create_time__lte=contest.rank_list_stop_at)
        judge_status_1hr = contest.judge_status.order_by("id").filter(create_time__gt=contest.rank_list_stop_at)
        judge_status_list_lte_1hr = []
        judge_status_list_1hr = {}

        for status in judge_status_lte_1hr:
            if status.author_id not in user_list.keys():
                continue
            judge_status_list_lte_1hr.append({
                "id": status.id,
                "problem_id": status.virtual_problem_id,
                "user_id": status.author_id,
                "flag": status.flag,
                "create_time": int(time.mktime(status.create_time.timetuple())),
            })
        for status in judge_status_1hr:
            if status.author_id not in user_list.keys():
                continue
            jitem = judge_status_list_1hr.get(str(status.author_id), {})
            pitem = jitem.get(str(status.virtual_problem_id), {
                'ac_flag': False,
                'ac_time': 0,
                'submit_count': 0,
                'ignore_count': 0,
            })
            if pitem['ac_flag'] is True:
                continue
            pitem['submit_count'] += 1
            create_time = int(time.mktime(status.create_time.timetuple()))

            if status.flag == 0:
                # AC
                pitem['ac_flag'] = True
                pitem['ac_time'] = create_time - contest_start_time
            elif status.flag > 0:
                if status.flag not in penalty_items:
                    pitem['ignore_count'] += 1

            jitem[str(status.virtual_problem_id)] = pitem
            judge_status_list_1hr[str(status.author_id)] = jitem

        return {
            "penalty_items": penalty_items,
            "penalty_time": penalty_time,
            "start_time": contest_start_time,
            "problem_indexs": cpindex_list,
            "problem_list": [cproblem.id for cproblem in cproblem_list],
            "judge_status_lte_1hr": judge_status_list_lte_1hr,
            "judge_status_1hr": judge_status_list_1hr,
            "user_list": user_list
        }

    # 发送打印资料请求
    @ContestBaseController.login_validator
    @ContestBaseController.check_timepassed_validator(status__gt=-1, errcode=5003)
    def send_printer(self):
        """
        发送打印资料请求
        :return:
        """
        user = self.session.account

        parser = ParamsParser(self._request)
        content = parser.get_str("content", method="POST")
        status_id = parser.get_int("status", 0, method="POST")
        action = parser.get_int("action", 0, method="POST")
        if action == 0:
            if status_id > 0:
                self.get_status(status_id)
                if self.status.author != user:
                    raise WeJudgeError(5220)
                try:
                    result_content = JudgeResult(self.status.result)
                except Exception as ex:
                    raise WeJudgeError(2007)

                print_title = "Print Solution %s Problem %s - %s" % (
                    self.status.id,
                    tools.gen_problem_index(self.status.virtual_problem.index),
                    self.status.problem.title
                )
                print_countent = result_content.finally_code
            else:
                raise WeJudgeError(5219)
        elif action == 1:
            if content.strip() == "":
                raise WeJudgeError(5219)
            print_title = "Print Competitor's Code"
            print_countent = content
        else:
            raise WeJudgeError(5219)

        pitem = ContestModel.ContestPrinterQueue()
        pitem.author = user
        pitem.content = print_countent
        pitem.title = print_title
        pitem.contest = self.contest
        pitem.is_finish = False
        pitem.save()

    # 获取打印资料请求列表
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def get_printer_queue(self):
        """
        获取打印资料请求列表
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
            model_object=ContestModel.ContestPrinterQueue.objects.filter(
                contest=self.contest
            ).order_by("is_finish", "-id"),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def get_queue_item(_item):
            return _item.json(items=[
                'id', 'content', 'title', 'is_finish', 'author',
                'author__nickname', 'author__username', 'create_time'
            ])

        return get_queue_item()

    # 获取打印资料正文
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def get_printer_queue_item(self, pid):
        """
        获取打印资料正文
        :return:
        """
        item = ContestModel.ContestPrinterQueue.objects.filter(contest=self.contest, id=pid)
        if item.exists():
            item = item[0]
            item.is_finish = True
            item.save()
            return item
        else:
            raise WeJudgeError(5221)

    # 删除打印请求
    @ContestBaseController.login_validator
    @ContestBaseController.check_privilege_validator(role=2)
    def delete_printer_queue_item(self):
        """
        删除打印请求
        :return:
        """
        parser = ParamsParser(self._request)
        pid = parser.get_int('pid', require=True, errcode=5221)
        item = ContestModel.ContestPrinterQueue.objects.filter(contest=self.contest, id=pid)
        if item.exists():
            item = item[0]
            item.delete()
        else:
            raise WeJudgeError(5221)

    # 比赛排行信息获取（实现）
    @staticmethod
    def get_ranklist_data(contest):
        """
        比赛排行信息获取（实现）
        :return:
        """

        # penalty_time = self.contest.penalty_time
        # penalty_time = penalty_time.hour * 3600 + penalty_time.minute * 60 + penalty_time.second

        accounts_solutions = {}
        count = 1

        # 对于这种可预知的大量查询，Django不会处理组合查询的，所以还是先查出来再走一次循环以节省与数据库交互的时间
        solutions = ContestModel.ContestSolution.objects.filter(contest=contest)
        for sol in solutions:
            a = accounts_solutions.get(sol.author_id, {})
            a[sol.problem_id] = sol.json(items=[
                'accepted', 'submission', 'penalty', 'best_memory',
                'best_time', 'best_code_size', 'first_ac_time',
                'is_first_blood', 'used_time', 'used_time_real'
            ])
            accounts_solutions[sol.author_id] = a

        account_view = []
        rank_model = ContestModel.ContestAccount.objects.filter(
            contest=contest, role=0
        ).order_by('-rank_solved', 'rank_timeused', 'rank_last_ac_time')

        for _account in rank_model:
            account = _account.json(items=[
                'id', 'username', 'nickname', 'realname', 'sex', 'rank_solved', 'rank_timeused', 'finally_rank',
                'ignore_rank', 'rank_last_ac_time'
            ])
            if contest.rank_list_show_items == 2:
                account['nickname'] = ''
                account['realname'] = ''
            elif contest.rank_list_show_items == 1:
                account['realname'] = ''
            account['solutions'] = accounts_solutions.get(_account.id, {})
            account['rank'] = count
            count += 1
            account_view.append(account)

        return {
            "data": account_view,
            "problems": [x.json(items=[
                "id", "index"
            ]) for x in contest.problems.order_by('index')],
            "contest": contest.json(items=[
                "start_time", "end_time", "penalty_time"
            ])
        }

    # 注册报名功能
    def user_register(self):

        if self.login_check(throw=False):
            raise WeJudgeError(5011)

        parser = ParamsParser(self._request)
        action = parser.get_str("action", '', method="POST")
        username = parser.get_str("username", require=True, method="POST", errcode=1101)
        nickname = parser.get_str("nickname", require=True, method="POST", errcode=1102)

        if self.contest.register_mode != action:
            raise WeJudgeError(5012)

        if action == 'register':
            if not self.session.master_logined:
                raise WeJudgeError(5013)

            if ContestModel.ContestAccount.objects.filter(username=username, contest=self.contest).exists():
                raise WeJudgeError(5014)

            if ContestModel.ContestAccount.objects.filter(master=self.session.master, contest=self.contest).exists():
                raise WeJudgeError(5015)

            master = self.session.master

            account = ContestModel.ContestAccount()
            account.contest = self.contest
            account.username = username
            account.nickname = nickname
            account.realname = master.realname
            account.can_bind_master = True
            account.master = master
            account.ignore_rank = False
            account.role = 0
            account.save()

    # 读取FAQ信息
    def get_faq(self, fid, force_root=True):
        """
        读取FAQ信息
        :param fid:
        :param force_root: 是否只查询根
        :return:
        """
        if force_root:
            faq = ContestModel.FAQ.objects.filter(contest=self.contest, id=fid, is_root=True)
        else:
            faq = ContestModel.FAQ.objects.filter(contest=self.contest, id=fid)

        if faq.exists():
            return faq[0]
        else:
            raise WeJudgeError(5210)

    # 通过北师珠教务系统认证来创建用户
    def _create_user_by_check_bnuz_jwc(self):
        """
        通过北师珠教务系统认证来创建用户
        :return:
        """

        parser = ParamsParser(self._request)
        username = parser.get_str("username", require=True, method="POST", errcode=1904)
        password = parser.get_str("password", require=True, method="POST", errcode=1905)

        if ContestModel.ContestAccount.objects.filter(username=username, contest=self.contest).exists():
            raise WeJudgeError(1906)

        from wejudge.utils.bnuz_connector import JWFZSpider, JWSpider

        # if JWFZSpider().login_validate(username, password):

        spider = JWSpider()
        if spider.login_validate(username, password):
            stuinfo = spider.get_student_info()

            account = ContestModel.ContestAccount()
            account.contest = self.contest
            account.username = username
            account.password = tools.gen_passwd(password)
            account.nickname = stuinfo.get('name')
            account.realname = stuinfo.get('name')
            account.sex = 0 if stuinfo.get('gender', '男') == '女' else 1
            account.can_bind_master = False
            account.ignore_rank = False
            account.role = 0
            account.save()

    # 用户更改密码
    @ContestBaseController.login_validator
    def user_changepwd(self):

        parser = ParamsParser(self._request)
        user_id = parser.get_int("user_id", require=True, method="POST")
        password = parser.get_str("password", require=True, method="POST", errcode=1006)
        repassword = parser.get_str("repassword", require=True, method="POST", errcode=1008)

        if password != repassword:
            raise WeJudgeError(1007)

        if user_id != self.session.account.id:
            raise WeJudgeError(8)

        self.session.account.password = tools.gen_passwd(password)
        self.session.account.save()
