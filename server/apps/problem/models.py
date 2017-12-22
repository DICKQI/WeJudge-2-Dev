# -*- coding: utf-8 -*-
# coding:utf-8

import json
from django.db import models
from wejudge.db import ModelConverter
import apps.account.models as AccountModel

__author__ = 'lancelrq'

WENUM_PROBLEM_DIFF = (
    (0, '未分级'),
    (1, '1星'),
    (2, '2星'),
    (3, '3星'),
    (4, '4星'),
    (5, '5星'),
)

WENUM_PROBLEM_TYPE = (
    (0, '正常模式'),
    (1, '代码填空模式'),
    (2, '手动批改模式')           # 仅供教学使用
)


# 题目数据原始表
class Problem(models.Model, ModelConverter):
    """
    题目数据原始表
    """

    class Meta:
        verbose_name = "题目-信息表"
        verbose_name_plural = "题目-信息表"

    # 题目名称
    title = models.CharField(max_length=255, default="")

    # 题目作者
    author = models.ForeignKey(AccountModel.Account, null=True, blank=True)

    # 题目难度(0-5, 0表示未分级)
    difficulty = models.SmallIntegerField(default=0, choices=WENUM_PROBLEM_DIFF)

    # 单组测试数据（用来提示用户需不需要写while scanf)
    single_testcase = models.BooleanField(default=False)

    # 题目创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 题目更新时间
    update_time = models.DateTimeField(auto_now=True)

    """ === 题目内容部分 === """

    # 题目说明
    description = models.TextField(default="")

    # 输入要求
    input = models.TextField(default="", blank=True)

    # 输出要求
    output = models.TextField(default="", blank=True)

    # 输入样例
    sample_input = models.TextField(default="", blank=True)

    # 输出样例
    sample_output = models.TextField(default="", blank=True)

    # 小贴士
    hint = models.TextField(default="", blank=True)

    # 题目来源
    source = models.TextField(default="", blank=True)

    # 题目类型
    problem_type = models.SmallIntegerField(default=0, choices=WENUM_PROBLEM_TYPE)

    # 允许使用的语言 (0 默认为所有语言都支持)
    lang = models.SmallIntegerField(default=0)

    # 权限（枚举
    permission = models.SmallIntegerField(default=7)        # Default: rjd- (1 | 2 | 4)

    """ === 评测选项 === """

    # 评测选项配置信息（JSON），文件也会存一份
    judge_config = models.TextField(default="")

    # 暂停评测
    pause_judge = models.BooleanField(default=True)

    def __str__(self):
        return u"%d. %s" % (self.id, self.title)

    def __getattr__(self, item):
        if item == 'judge_ratio':
            if self.ac != 0:
                ratio = (self.ac * 1.0) / self.total * 100
            else:
                ratio = 0
            return '%.2lf%% (%s / %s)' % (ratio, self.ac, self.total)
        else:
            return self.__getattribute__(item)


# 账户题目访问计数器缓存
class AccountProblemVisited(models.Model, ModelConverter):
    """
    账户题目访问计数器缓存
    """

    class Meta:
        verbose_name = "账户题目访问计数器缓存"
        verbose_name_plural = "账户题目访问计数器缓存"

    # 操作账户
    author = models.ForeignKey(AccountModel.Account)

    # 对应题目
    problem = models.ForeignKey('Problem')

    # 提交代码的次数
    submission = models.IntegerField(default=0)

    # 代码通过的次数
    accepted = models.IntegerField(default=0)

    # 更新时间
    update_time = models.DateTimeField(auto_now=True)


# 题目集合的项目
class ProblemSetItem(models.Model, ModelConverter):
    """
    题目集合的项目

    标准题库集内的题目ID显示的是题目实体的ID
    """

    class Meta:
        verbose_name = "题目集-题目项"
        verbose_name_plural = "题目集-题目项"

    # 归属题目
    problemset = models.ForeignKey('ProblemSet', null=True, blank=True, related_name="item_of_problemset")

    # 题目实体
    entity = models.ForeignKey('Problem')

    # 顺序
    index = models.IntegerField(default=0)

    # 通过题目数量
    accepted = models.IntegerField(default=0)

    # 提交题目数量
    submission = models.IntegerField(default=0)

    # 题目所属分类
    classification = models.ForeignKey('ProblemClassify', blank=True, null=True)

    def __str__(self):
        return "id=%s, entity=(%s), pset=(%s)" % (self.id, self.entity, self.problemset)


# 题目集合
class ProblemSet(models.Model, ModelConverter):
    """
    题目集合
    """

    class Meta:
        verbose_name = "题目集"
        verbose_name_plural = "题目集"

    # 题库名称
    title = models.CharField(max_length=255, default="")

    # 题库说明
    description = models.TextField(default="")

    # 题库图片文件
    image = models.CharField(max_length=255, default="")

    # 题库关联题目
    items = models.ManyToManyField('ProblemSetItem', blank=True, related_name='pset_items')

    # 题目数量
    items_count = models.IntegerField(default=0)

    # 评测记录
    judge_status = models.ManyToManyField('JudgeStatus', blank=True, related_name='pset_judge_status')

    # 私有权限(0-公开；1-高级共享；2-完全私有）
    private = models.IntegerField(default=0)

    # 是否只允许自己发布题目
    publish_private = models.BooleanField(default=True)

    # 题库管理员
    manager = models.ForeignKey(AccountModel.Account, related_name='pset_manager', blank=True, null=True)

    def __str__(self):
        return "id=%s, title=%s" % (self.id, self.title)


# 分类信息
class ProblemClassify(models.Model, ModelConverter):

    class Meta:
        verbose_name = "题目分类"
        verbose_name_plural = "题目分类"

    # 归属题集
    problemset = models.ForeignKey('ProblemSet')

    # 分类标题
    title = models.CharField(max_length=255, default="")

    # 父分类节点
    parent = models.ForeignKey('ProblemClassify', null=True, blank=True)

    def __str__(self):
        return u"%s (id = %d)" % (self.title, self.id)


# Solution的基础表
class SolutionBase(models.Model, ModelConverter):
    """
    Solution的基础表
    """

    # 通过计数器
    accepted = models.IntegerField(default=0)

    # 提交计数器
    submission = models.IntegerField(default=0)

    # 罚时计数器
    penalty = models.IntegerField(default=0)

    # 最优内存占用
    best_memory = models.IntegerField(default=-1)

    # 最优时间使用
    best_time = models.IntegerField(default=-1)

    # 最小代码数量
    best_code_size = models.IntegerField(default=-1)

    # 第一次访问时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 第一次AC的时间
    first_ac_time = models.DateTimeField(null=True, blank=True)

    # 总用时（包括罚时）
    used_time = models.FloatField(default=0)

    # 真实用时（不包括罚时）
    used_time_real = models.FloatField(default=0)

    class Meta:
        # 不创建当前Model的数据表
        abstract = True


# 题目集的Solution
class ProblemSetSolution(SolutionBase, models.Model, ModelConverter):

    class Meta:
        verbose_name = "题目集的题目解决情况"
        verbose_name_plural = "题目集的题目解决情况"

        unique_together = (("problemset", "problem", "virtual_problem", "author"),)

    # 归属题目集
    problemset = models.ForeignKey('ProblemSet')

    # 对应题目
    problem = models.ForeignKey('Problem')

    # 对应虚拟题目
    virtual_problem = models.ForeignKey('ProblemSetItem')

    # 提交者
    author = models.ForeignKey(AccountModel.Account)

    def __str__(self):
        return u"id = %s,  pid = %s, aid = %s" % (self.id, self.problem_id, self.author_id)


# 评测状态详情基础表
class JudgeStatusBase(models.Model, ModelConverter):
    """
    评测状态详情基础表
    """

    # 评测状态
    flag = models.SmallIntegerField(default=-2)

    # 评测语言
    lang = models.SmallIntegerField(default=0)

    # 提交时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 最大运行时间（毫秒）
    exe_time = models.IntegerField(default=0)

    # 最大内存占用（KB）
    exe_mem = models.IntegerField(default=0)

    # 代码长度（字节）
    code_len = models.IntegerField(default=0)

    # 代码文件位置
    code_path = models.CharField(max_length=255, default="")

    # 评测结果
    result = models.TextField(blank=True, null=True, default="")

    class Meta:
        # 不创建当前Model的数据表
        abstract = True


# 题目集合的评测记录
class JudgeStatus(JudgeStatusBase, ModelConverter):
    """
    题目集合的评测记录
    """

    class Meta:
        verbose_name = "评测状态"
        verbose_name_plural = "评测状态"

    # 对应题目
    problem = models.ForeignKey('Problem', null=True, blank=True)

    # 对应虚拟题目
    virtual_problem = models.ForeignKey('ProblemSetItem', null=True, blank=True)

    # 提交者
    author = models.ForeignKey(AccountModel.Account, null=True, blank=True)

    def __str__(self):
        return u"id = %s,  pid = %s" % (self.id, self.problem.id)


# 测试数据自动生成器记录
class TCGeneratorStatus(JudgeStatusBase, ModelConverter):
    """
    测试数据自动生成器记录
    """

    class Meta:
        verbose_name = "题目-测试数据生成队列"
        verbose_name_plural = "题目-测试数据生成队列"

    # 提交者
    author = models.ForeignKey(AccountModel.Account)

    # 对应的题目
    problem = models.ForeignKey('Problem')

    # 回调用的安全代码
    auth_code = models.CharField(max_length=200, default="")

    def __str__(self):
        return u"id = %d, problem_id = %d" % (self.id, self.problem.id)


class CodeDrafts(models.Model, ModelConverter):
    """
    用户草稿箱
    草稿箱单个用户单个题目最多保存3条，超过数量将自动删除最旧的那条
    """

    class Meta:
        verbose_name = "用户草稿箱"
        verbose_name_plural = "用户草稿箱"

    # 提交者
    author = models.ForeignKey(AccountModel.Account)

    # 对应的题目
    problem = models.ForeignKey('Problem')

    # 保存的内容
    content = models.TextField(blank=True, default="")

    # 使用的语言(仅显示)
    lang = models.SmallIntegerField(default=0)

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"DraftID=%s Create By UserID=%s in Problem %s" % (self.id, self.author.id, self.problem.id)
