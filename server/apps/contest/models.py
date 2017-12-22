# -*- coding: utf-8 -*-
# coding:utf-8

import datetime
from wejudge.db import ModelConverter
import apps.account.models as AccountModel
import apps.problem.models as ProblemModel
from django.db import models

__author__ = 'lancelrq'


# 比赛服账户
class ContestAccount(AccountModel.AccountBase, models.Model, ModelConverter):

    wejudge_session_manager_name = 'contest'

    # 关联主账户
    master = models.ForeignKey(AccountModel.Account, null=True, blank=True)

    # 明文密码（一般不会有，如果由账户生成器处理的就会出现在这里，只能由管理员才能看到
    clear_password = models.CharField(max_length=255, blank=True, default="")

    # 账户角色： 0 - 参赛者，1 - 裁判，2-总管理员
    role = models.SmallIntegerField(default=0)

    # 归属比赛
    contest = models.ForeignKey('Contest')

    # 可以自由设置是否允许绑定主账户
    can_bind_master = models.BooleanField(default=True)

    # Rank!
    # 解决问题数量
    rank_solved = models.IntegerField(default=0)

    # 总计用时
    rank_timeused = models.FloatField(default=0)

    # 最后一次(First)AC时间
    # 其实因为如果没解决过问题的话，排什么也没有意义嘛，对于解决过问题的，这个一定不为空，所以这个设计是合理的。
    rank_last_ac_time = models.DateTimeField(null=True, blank=True, default=None)

    # 排行(由裁判手动统计，在比赛结束后展示）
    finally_rank = models.IntegerField(default=0)

    # 不参与排行
    ignore_rank = models.BooleanField(default=False)

    class Meta:
        verbose_name = "比赛服账户"
        verbose_name_plural = "比赛服账户"

    def __str__(self):
        from wejudge.const import system
        return 'id = %s ；昵称：%s ；真实姓名：%s；身份：%s；主账户：（%s）' % \
           (
               self.id, self.nickname, self.realname,
               system.WEJUDGE_CONTEST_ACCOUNT_ROLES.call(self.role), self.master
           )


# 比赛
class Contest(models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛信息"
        verbose_name_plural = "比赛信息"

    # 比赛名称
    title = models.CharField(max_length=100, blank=True, default="")

    # 比赛简介（暂时保留这个字段吧，估计要废弃）
    description = models.CharField(max_length=255, blank=True, default="")

    # 开始时间
    start_time = models.DateTimeField(null=True, blank=True)

    # 结束时间
    end_time = models.DateTimeField(null=True, blank=True)

    # 主办方
    sponsor = models.TextField(blank=True, default="")

    # 题目集合
    problems = models.ManyToManyField("ContestProblem", blank=True)

    # 评测状态关联
    judge_status = models.ManyToManyField('JudgeStatus', blank=True)

    # ===== 设置 =====

    # 排行榜名称显示
    rank_list_show_items = models.IntegerField(default=0)

    # 暂停比赛(暂停提交）
    pause = models.BooleanField(default=False)

    # 允许使用的语言(默认所有)
    lang = models.SmallIntegerField(default=0)

    # 罚时项目
    penalty_items = models.CharField(max_length=100, blank=True, default='1,2,3,4,5,6')

    # 罚时
    penalty_time = models.TimeField(default=datetime.time(0, 20, 0))

    # 封榜时间(Null则不封榜）
    rank_list_stop_at = models.DateTimeField(null=True, blank=True)

    # 隐藏题目标题
    hide_problem_title = models.BooleanField(default=False)

    # 启用实时简单代码查重
    cross_check = models.BooleanField(default=False)

    # 比赛结束后公开排行
    cross_check_public = models.BooleanField(default=False)

    # 比赛结束后公开排行显示的查重率
    cross_check_public_ratio = models.FloatField(default=0.8)

    # 记录保留阈值
    cross_check_ratio = models.FloatField(default=0.8)

    # 不需要查重的题目
    cross_check_ignore_problem = models.ManyToManyField('ContestProblem', blank=True, related_name='cc_ignore_problem')

    # 数据令牌(用于比赛只读数据获取操作
    access_token = models.CharField(max_length=100, blank=True, default="")

    # 开启打印资料的功能
    enable_printer_queue = models.BooleanField(default=False)

    # 开放注册模式（'register'为使用主账户注册，'edu_register'为使用教学账户注册，等等，留空为不开放注册）
    register_mode = models.CharField(max_length=100, blank=True, default="")

    # 归档锁定
    archive_lock = models.BooleanField(default=False)

    def __str__(self):
        return u"id = %d , 比赛名称：%s" % (self.id, self.title)


# 比赛题目设置
class ContestProblem(models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛题目设置"
        verbose_name_plural = "比赛题目设置"

    # 题目顺序
    index = models.IntegerField(default=0)

    # 题目关联
    entity = models.ForeignKey(ProblemModel.Problem, blank=True)

    # 通过题目数量
    accepted = models.IntegerField(default=0)

    # 提交题目数量
    submission = models.IntegerField(default=0)

    # 可用语言（继承父节点是业务实现，这里不做处理）
    lang = models.SmallIntegerField(default=0)

    # 评测模式（0-自动；1-半自动；2-手动）
    judger_mode = models.IntegerField(default=0)

    def __str__(self):
        return u"id = %s,  PID=%s" % (self.id, self.entity)


# 比赛题目解决情况
class ContestSolution(ProblemModel.SolutionBase, models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛题目-解决情况"
        verbose_name_plural = "比赛题目-解决情况"

        unique_together = (("author", "contest", "problem"),)

    # 提交者
    author = models.ForeignKey('ContestAccount', blank=True)

    # 归属比赛
    contest = models.ForeignKey("Contest", blank=True)

    # 对应的的题目
    problem = models.ForeignKey('ContestProblem', blank=True)

    # 提交状态
    judge_status = models.ManyToManyField('JudgeStatus', blank=True)

    # 是否为一血
    is_first_blood = models.BooleanField(default=False)

    def __str__(self):
        return "contestID=%s, userid=%s, pid=%s" % (self.contest.id, self.author.id, self.problem.id)


# 评测记录
class JudgeStatus(ProblemModel.JudgeStatusBase, models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛-评测记录"
        verbose_name_plural = "比赛-评测记录"

    # 对应题目
    problem = models.ForeignKey(ProblemModel.Problem, null=True, blank=True, related_name='contest_status_problem')

    # 对应虚拟题目(asgn_problem_item)
    virtual_problem = models.ForeignKey('ContestProblem', null=True, blank=True, related_name='contest_status_vproblem')

    # 提交者
    author = models.ForeignKey('ContestAccount', null=True, blank=True)

    def __str__(self):
        return u"id = %s,  pid = %s" % (self.id, self.problem.id)


# 比赛问答系统
class FAQ(models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛题目-问答系统"
        verbose_name_plural = "比赛题目-问答系统"

    # 归属比赛
    contest = models.ForeignKey("Contest")

    # 发起人
    author = models.ForeignKey('ContestAccount')

    # 提问主题(如果是孩子项则忽略）
    title = models.CharField(max_length=100, blank=True, default='')

    # 提问（或回答）内容
    content = models.TextField(blank=True, default='')

    # 提问发起时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 默认（或回答）为私有问答，如果裁判觉得这个问答适合公开，则会公开问答 （适用于根
    is_private = models.BooleanField(default=True)

    # 是否是根问题
    is_root = models.BooleanField(default=True)

    # 回复列表
    children = models.ManyToManyField('FAQ', blank=True)

    def __str__(self):
        return "faq[%d] = %s (by: %s)" % (self.id, self.title, self.author.nickname)


# 比赛公告
class Notice(models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛题目-公告"
        verbose_name_plural = "比赛题目-公告"

    # 归属比赛
    contest = models.ForeignKey("Contest")

    # 发布者
    author = models.ForeignKey('ContestAccount')

    # 内容
    content = models.TextField(blank=True, default='')

    # 发起时间
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "notice[%d] = %s (by: %s)" % (self.id, self.title, self.author.id)


# 代码查重模块
class ContestCodeCrossCheck(models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛-简单代码查重"
        verbose_name_plural = "比赛-简单代码查重"

    # 对应的的比赛
    contest = models.ForeignKey("Contest",blank=True)

    # 对应的的题目
    problem = models.ForeignKey("ContestProblem", blank=True)

    # 评测状态1
    source = models.ForeignKey('JudgeStatus', related_name="source_status")

    # 评测状态2
    target = models.ForeignKey('JudgeStatus', related_name="target_status2")

    # Levenshtein相似度
    levenshtein_similarity_ratio = models.FloatField(default=0)

    # Moss相似度
    moss_similarity_ratio = models.FloatField(default=0)

    def __str__(self):
        return u"%s -> %s: {levenshtein: %.3f%%}" % (
            self.source.id, self.target.id, self.levenshtein_similarity_ratio
        )


# 比赛打印代码功能实现（叶启权加的需求！）
class ContestPrinterQueue(models.Model, ModelConverter):

    class Meta:
        verbose_name = "比赛打印代码功能表"
        verbose_name_plural = "比赛打印代码功能表"

    # 对应的的比赛
    contest = models.ForeignKey("Contest", blank=True)

    # 提交者
    author = models.ForeignKey("ContestAccount", blank=True, null=True)

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 打印标题
    title = models.CharField(max_length=255, blank=True, default="")

    # 打印内容
    content = models.TextField(default="", blank=True)

    # 处理情况
    is_finish = models.BooleanField(default=False)

    def __str__(self):
        return "Id = %s" % self.id
