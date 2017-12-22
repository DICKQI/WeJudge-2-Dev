# -*- coding: utf-8 -*-
# coding:utf-8
import os.path
from wejudge.core import *
from wejudge.utils import *
from wejudge.const import system
from wejudge.utils import tools
import apps.problem.models as ProblemModel
from django.db.models import Q
from .base import ProblemBaseController

__author__ = 'lancelrq'


class ProblemSetController(ProblemBaseController):

    def __init__(self, request, response):
        super(ProblemSetController, self).__init__(request, response)

    # 读取用户发布的题目
    @ProblemBaseController.login_validator
    def get_problems_by_logined_user(self):
        """
        读取用户发布的题目
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
            model_object=self._my_problems_filter(ProblemModel.Problem.objects.filter(author=self.session.account)),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_problems_item(problem):
            return problem.json(items=[
                "id", "title", "author", "difficulty", "author__nickname", "author__id"
            ])

        return proc_problems_item()

    # === problem set

    # 获取题目集列表
    def get_problemset_list(self):
        """
        获取题目集列表
        :return:
        """
        parser = ParamsParser(self._request)
        page = parser.get_int('page', 1)
        limit = parser.get_int('limit', 40)
        display = parser.get_int('display', system.WEJUDGE_PAGINATION_BTN_COUNT)

        pagination = {
            "page": page,
            "limit": limit,
            "display": display
        }

        account = self.session.account if self.session.is_logined() else None
        problem_sets = ProblemModel.ProblemSet.objects.filter()

        @WeJudgePagination(
            model_object=self._problemset_filter(problem_sets),
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 40),
            display=pagination.get("display", system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_problems_item(_problem):
            view_item = _problem.json(items=[
                "id", "title", "description", "image", "items_count",
                "manager", "manager__nickname", "manager__id", 'private', 'publish_private'
            ])
            view_item['editable'] = account is not None and (
                account.id == _problem.manager_id or account.permission_administrator
            )
            return view_item

        result = proc_problems_item()
        return result

    # 读取题目集中的题目列表
    @ProblemBaseController.problemset_privilege_validator
    def get_problems_list(self):
        """
        读取题目集中的题目列表
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

        pset = self.problem_set
        user = self.session.account

        @WeJudgePagination(
            model_object=self._problemset_list_filter(plist=pset.items),
            page=pagination.get("page", 1),
            limit=pagination.get("limit",  system.WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT),
            display=pagination.get("display",  system.WEJUDGE_PAGINATION_BTN_COUNT)
        )
        def proc_problems_item(_problem):
            return _problem

        result = proc_problems_item()
        problems_list = []

        if user is not None and len(result.get("data", [])) > 0:
            apvs = ProblemModel.AccountProblemVisited.objects.filter(
                author=user,
                problem__in=[x.entity for x in result.get("data", [])]
            )
            visited_list = {x.problem.id: [x.accepted, x.submission] for x in apvs}
            for problem in result.get("data", []):
                problem_entity = problem.entity
                v = visited_list.get(problem_entity.id, [0, 0])

                problems_list.append({
                    "problemset": pset.id,
                    "id": problem.id,
                    "entity": {
                        "id": problem_entity.id
                    },
                    "title": problem_entity.title,
                    "author": {
                        "nickname": problem_entity.author.nickname,
                        "id": problem_entity.author.id
                    },
                    "diff": problem_entity.difficulty,
                    "submission": problem.submission,
                    "accepted": problem.accepted,
                    "my_submission": v[1],
                    "my_accepted": v[0],
                })
        else:
            for problem in result.get('data', []):
                problem_entity = problem.entity
                problems_list.append({
                    "problemset": pset.id,
                    "id": problem.id,
                    "entity": {
                        "id": problem_entity.id
                    },
                    "title": problem_entity.title,
                    "author": {
                        "nickname": problem_entity.author.nickname,
                        "id": problem_entity.author.id
                    },
                    "diff": problem_entity.difficulty,
                    "submission": problem.submission,
                    "accepted": problem.accepted
                })
        result['data'] = problems_list
        return result

    # 读取题目集的评测历史
    @ProblemBaseController.problemset_privilege_validator
    def get_judge_status(self):
        """
        读取题目集的评测历史
        :return:
        """

        pset = self.problem_set
        model_obj = self._judge_status_filter(pset.judge_status)

        return self._get_judge_status(model_obj)

    # 移动题目到指定的分类（批量处理）
    @ProblemBaseController.login_validator
    @ProblemBaseController.problemset_manager_validator
    def problem_moveto_classify(self):
        """
        移动题目到指定的分类（批量处理）
        （分类信息已经获取）
        :return:
        """
        parser = ParamsParser(self._request)
        problem_ids = parser.get_list('batch_id', method='POST', require=True)
        for pid in problem_ids:
            pset_item = self.problem_set.items.filter(id=pid)
            if pset_item.exists():
                pset_item = pset_item[0]
                pset_item.classification = self.classify
                pset_item.save()
            else:
                continue

        return True

    # 推送题目到指定的题目集（批处理，权限已内部控制）
    @ProblemBaseController.login_validator
    def problem_moveto_problemset(self):
        """
        推送题目到指定的题目集（批量处理）
        :return:
        """
        parser = ParamsParser(self._request)
        problem_ids = parser.get_list('batch_id', method='POST', require=True)
        is_raw_id = parser.get_boolean('is_rw_id', False)
        target_pset_id = parser.get_int('target_pset_id', require=True)

        # 拿到目标题库
        target_pset = ProblemModel.ProblemSet.objects.filter(id=target_pset_id)
        if not target_pset.exists():
            raise WeJudgeError(2000)
        target_pset = target_pset[0]

        msg = []

        for pid in problem_ids:
            # 如果使用的是题库的关联ID
            if not is_raw_id:
                pset_item = self.problem_set.items.filter(id=pid)
                if pset_item.exists():
                    problem = pset_item[0].entity
                else:
                    continue
            else:
                # 使用题目原始ID
                problem = ProblemModel.Problem.objects.filter(id=pid)
                if problem.exists():
                    problem = problem[0]
                else:
                    continue

            # 执行推送，成功与否由下面的函数决定
            try:
                self._publish_to_problemset(problem, target_pset)
                msg.append("Problem %s, Successed." % problem.id)
            except WeJudgeError as wjerr:
                msg.append("Problem %s, Error: %s" % (problem.id, wjerr))

        return msg

    # 从题库中批量移除题目（批量处理，权限已内部控制）
    @ProblemBaseController.login_validator
    def problem_removefrom_problemset(self):
        """
        从题库中批量移除题目（批量处理）
        :return:
        """
        parser = ParamsParser(self._request)
        problem_ids = parser.get_list('batch_id', method='POST', require=True)

        msg = []

        for pid in problem_ids:
            pset_item = self.problem_set.items.filter(id=pid)
            if pset_item.exists():
                # 执行推送，成功与否由下面的函数决定
                try:
                    pset_item = pset_item[0]
                    self._remove_from_problemset(pset_item.entity, self.problem_set)
                    msg.append("Remove Problem %s, Successed." % pset_item.entity.id)
                except WeJudgeError as wjerr:
                    msg.append("Remove Problem %s, Error: %s" % (pset_item.entity.id, wjerr))
            else:
                continue

        return msg

    # == Manager

    # 创建题目集
    @ProblemBaseController.login_validator
    @ProblemBaseController.problemset_manager_validator
    def create_problemset(self):
        """
        创建题目集
        :return:
        """

        parser = ParamsParser(self._request)
        title = parser.get_str("title", method="POST", require=True, errcode=2103)
        description = parser.get_str("description", "", method="POST")
        publish_private = parser.get_boolean("publish_private", False, method="POST")
        private = parser.get_boolean("private", False, method="POST")

        ps = ProblemModel.ProblemSet()
        ps.title = title
        ps.description = description
        ps.image = "/static/images/pset_default.jpg"
        ps.manager = self.session.account
        ps.publish_private = publish_private
        ps.private = private
        ps.save()

        return ps.id

    # 编辑题目集信息
    @ProblemBaseController.login_validator
    @ProblemBaseController.problemset_manager_validator
    def modify_problemset(self):
        """
        编辑题目集信息
        :param psid: Problemset Id
        :return:
        """

        parser = ParamsParser(self._request)
        title = parser.get_str("title", method="POST", require=True, errcode=2103)
        description = parser.get_str("description", "", method="POST")
        image = parser.get_str("image", "", method="POST")
        publish_private = parser.get_boolean("publish_private", False, method="POST")
        private = parser.get_int("private", 0, min=0, max=2, method="POST")

        ps = self.problem_set
        ps.title = title
        ps.description = description
        ps.publish_private = publish_private
        ps.private = private
        if image.strip() != "":
            ps.image = image
        ps.save()

        return ps.id

    # 更改题目集的封面信息（上传接口）
    @ProblemBaseController.login_validator
    @ProblemBaseController.problemset_manager_validator
    def change_problemset_image(self):
        """
        更改题目集的封面信息（上传接口）
        :return:
        """

        parser = ParamsParser(self._request)
        image_file = parser.get_file("uploadImageFile", require=True, type=[
            "image/jpg", "image/jpeg", "image/png", "image/bmp"
        ])

        if image_file.size > 1 * 1024 * 1024:
            raise WeJudgeError(2104)

        file_name = image_file.name.split(os.path.sep)
        file_name = file_name[len(file_name) - 1 if len(file_name) > 1 else 0]
        ext = file_name.split('.')
        ext = ext[len(ext) - 1 if len(ext) > 1 else 0]

        ps = self.problem_set

        save_file_name = "%s.%s" % (ps.id, ext)
        storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMSET_THUMBS_DIR, "")
        fp = storage.open_file(save_file_name, "wb")
        for chunk in image_file.chunks():
            fp.write(chunk)
        fp.close()

        return "/resource/problemset_thumbs/%s" % save_file_name

    # 从题库中移除题目
    @ProblemBaseController.login_validator
    @ProblemBaseController.problemset_manager_validator
    def remove_from_problemset(self):
        """
        从题库中移除题目
        :return:
        """
        self.problem_set.items.remove(self.problem_set_item)
        self.problem_set.items_count = self.problem_set.items.count()
        self.problem_set.save()
        return True

    # === Classification System

    # 读取分类信息
    @ProblemBaseController.problemset_privilege_validator
    def get_classify(self, cid):
        if self.problem_set is None:
            raise WeJudgeError(2000)
        if cid == "0":
            self.classify = None
            return
        classify = ProblemModel.ProblemClassify.objects.filter(problemset=self.problem_set, id=cid)
        if classify.exists():
            self.classify = classify[0]
        else:
            raise WeJudgeError(2300)

    # 获取分类列表信息（jstree专用数据格式)
    @ProblemBaseController.problemset_privilege_validator
    def get_classify_list(self):
        """
        获取分类信息（jstree专用数据格式)
        :return:
        """
        parser = ParamsParser(self._request)
        cid = parser.get_str('id', '')
        # 妈蛋jstree传根节点的值是 “#” 字符
        try:
            cid = int(cid)
        except:
            cid = 0

        if cid > 0:
            clist = ProblemModel.ProblemClassify.objects.filter(problemset=self.problem_set, parent__id=cid)
        else:
            clist = ProblemModel.ProblemClassify.objects.filter(problemset=self.problem_set, parent=None)
        data = []
        for classify in clist:
            no_extend = ProblemModel.ProblemClassify.objects.filter(
                problemset=self.problem_set, parent__id=classify.id
            ).exists()
            data.append({
                "id": classify.id,
                "text": classify.title,
                "children": no_extend
            })
        if cid <= 0:
            data = [{
                "id": "0",
                "text": "根分类",
                "children": data,
                "state": {
                    "opened": True,
                    "selected": True
                }
            }]
        return data

    # 更改分类信息
    @ProblemBaseController.login_validator
    @ProblemBaseController.problemset_manager_validator
    def change_classify(self):
        """
        更改分类信息
        （分类信息已经获取）
        :return:
        """
        parser = ParamsParser(self._request)
        action = parser.get_str('action', require=True)             # get param
        title = parser.get_str('title', '', method="POST")

        if action == 'appendChild':
            if title.strip() == '':
                raise WeJudgeError(2301)
            c = ProblemModel.ProblemClassify()
            c.parent = self.classify
            c.problemset = self.problem_set
            c.title = title
            c.save()
            return c.id
        elif action == 'modify':
            if title.strip() == '':
                raise WeJudgeError(2301)
            if self.classify is None:
                raise WeJudgeError(2302)
            self.classify.title = title
            self.classify.save()
            return self.classify.id

        elif action == 'delete':
            if self.classify is None:
                raise WeJudgeError(2302)

            classify_ids = self._classify_get_children_all_nodes(self.classify.id)
            # 安全移除（把节点改到它的父节点）
            pset_items = self.problem_set.items.filter(classification__id__in=classify_ids)
            for pitem in pset_items:
                pitem.classification = self.classify.parent
                pitem.save()

            parent_id = self.classify.parent_id
            self.classify.delete()
            return parent_id

        else:
            raise WeJudgeError(1)

    # === Protected Methods

    # 题目过滤器
    def _problemset_list_filter(self, plist):
        """
        题目过滤器
        :param plist: ModelManager with Probelm
        :return:
        """

        parser = ParamsParser(self._request)
        keyword = parser.get_str('keyword', '')             # 关键字(标题）
        author_id = parser.get_str('author', '')            # 作者
        diff = parser.get_int('diff', -2)                   # 题目难度
        classify_id = parser.get_int('classify_id', 0)      # 题目难度
        desc = parser.get_boolean('desc', default=False)    # 倒序排序

        if diff > -1:
            plist = plist.filter(entity__difficulty=diff)

        if classify_id > 0:
            cids = list(set(self._classify_get_children_all_nodes(classify_id)))
            plist = plist.filter(classification_id__in=cids).distinct()

        if (author_id is not None) and (author_id.strip() != ""):
            if tools.is_numeric(author_id):
                plist = plist.filter(
                    Q(entity__author__nickname__contains=author_id) |
                    Q(entity__author__realname__contains=author_id) |
                    Q(entity__author__id=author_id)
                )
            else:
                plist = plist.filter(
                    Q(entity__author__nickname__contains=author_id) |
                    Q(entity__author__realname__contains=author_id)
                )

        if (keyword is not None) and (keyword.strip() != ""):
            if tools.is_numeric(keyword):
                plist = plist.filter(
                    Q(entity__title__contains=keyword) |
                    Q(entity__id=keyword) |
                    Q(id=keyword)
                )
            else:
                plist = plist.filter(
                    Q(entity__title__contains=keyword)
                )

        if desc:
            plist = plist.order_by('-entity__id')
        else:
            plist = plist.order_by('entity__id')

        return plist.all()

    # 我发布的题目过滤器
    def _my_problems_filter(self, plist):
        """
        我发布的题目过滤器
        :param plist: ModelManager with Probelm
        :return:
        """

        parser = ParamsParser(self._request)
        keyword = parser.get_str('keyword', '')  # 关键字(标题）
        diff = parser.get_int('diff', -2)  # 题目难度
        desc = parser.get_boolean('desc', default=True)  # 倒序排序

        if diff > -1:
            plist = plist.filter(difficulty=diff)

        if (keyword is not None) and (keyword.strip() != ""):
            if tools.is_numeric(keyword):
                plist = plist.filter(
                    Q(title__contains=keyword) |
                    Q(id=keyword)
                )
            else:
                plist = plist.filter(
                    Q(title__contains=keyword)
                )

        if desc:
            plist = plist.order_by('-id')

        return plist.all()

    # 题目集过滤器
    def _problemset_filter(self, plist):
        """
        题目集过滤器
        :param plist: ModelManager with ProbelmSet
        :return:
        """

        parser = ParamsParser(self._request)
        keyword = parser.get_str('keyword', '')          # 关键字(标题）
        author_id = parser.get_str('author_id', '')         # 作者
        desc = parser.get_boolean('desc', default=False)    # 倒序排序

        if self.session.is_logined():
            logined_account = self.session.account
            if logined_account.permission_publish_problem or logined_account.permission_create_problemset:
                pass
            else:
                # 如果没有发布权限，过滤掉不能看的题库
                plist = plist.filter(private=0)
        else:
            # 没有登录，过滤掉不能看的题库
            plist = plist.filter(private=0)

        if (author_id is not None) and (author_id.strip() != ""):
            if tools.is_numeric(author_id):
                plist = plist.filter(
                    Q(manager__nickname__contains=author_id) |
                    Q(manager__realname__contains=author_id) |
                    Q(manager__id=author_id)
                )
            else:
                plist = plist.filter(
                    Q(manager__nickname__contains=author_id) |
                    Q(manager__realname__contains=author_id)
                )

        if (keyword is not None) and (keyword.strip() != ""):
            plist = plist.filter(title__contains=keyword)

        if desc:
            plist = plist.order_by('-id')

        return plist.all()

    # 递归取得分类所有子节点
    def _classify_get_children_all_nodes(self, node_id):
        """
        递归取得分类所有子节点
        :param node_id: 目标父节点ID
        :return:
        """
        cids = [node_id]
        if node_id <= 0:
            clist = ProblemModel.ProblemClassify.objects.filter(problemset=self.problem_set, parent=None)
        else:
            clist = ProblemModel.ProblemClassify.objects.filter(problemset=self.problem_set, parent__id=node_id)

        for node in clist:
            cids.append(node.id)
            cids.extend(self._classify_get_children_all_nodes(node.id))

        return cids
