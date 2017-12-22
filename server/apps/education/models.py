# -*- coding: utf-8 -*-
# coding:utf-8

import datetime
from django.db import models
import apps.account.models as AccountModel
import apps.problem.models as ProblemModel
from wejudge.db import ModelConverter

__author__ = 'lancelrq'


# 学校表
class EduSchool(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学-学校"
        verbose_name_plural = "教学-学校"

    # 学校名称
    name = models.CharField(max_length=50)

    # 学校缩写
    short_name = models.CharField(max_length=10, default="", db_index=True)

    # 学校标志
    logo = models.CharField(max_length=255, blank=True, default="")

    # 学校简介
    description = models.CharField(max_length=100, blank=True, default="")

    # 当前学期
    now_term = models.ForeignKey("EduYearTerm", blank=True, null=True)

    # 最大的教学周数
    max_week = models.SmallIntegerField(default=17)

    # 学校首页Banner主题色
    banner_style = models.CharField(default="#cccccc", null=True, blank=True, max_length=255)

    # 课堂节数和安排（JSON）
    sections = models.TextField(default='{}')

    # 锁定功能
    locked = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


# 学院表
class EduAcademy(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学-学院"
        verbose_name_plural = "教学-学院"

    # 归属学校
    school = models.ForeignKey('EduSchool')

    # 学院名称
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


# 院系表
class EduDepartment(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学-院系"
        verbose_name_plural = "教学-院系"

    # 归属学院
    academy = models.ForeignKey('EduAcademy')

    # 院系名称
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


# 专业表
class EduMajor(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学-专业"
        verbose_name_plural = "教学-专业"

    # 归属院系
    department = models.ForeignKey('EduDepartment')
    # 专业名称
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


# 按理来说学年学期是学校的制度，所以自动分配关联到学校
class EduYearTerm(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学-学年学期"
        verbose_name_plural = "教学-学年学期"

    # 归属学校
    school = models.ForeignKey('EduSchool')

    # 学年度,如果为2016则视作2016-2017年度
    year = models.SmallIntegerField(default=2016, null=False, blank=False)

    # 学期
    term = models.SmallIntegerField(default=1, null=False, blank=False)

    def __str__(self):
        return "%s-%s年度第%s学期" % (self.year, self.year+1, self.term)


# 教学系统马甲账户
class EduAccount(AccountModel.AccountBase, models.Model, ModelConverter):

    wejudge_session_manager_name = 'education'

    # 关联主账户
    master = models.ForeignKey(AccountModel.Account, null=True, blank=True)

    # 账户角色： 0 - 学生，1 - 助教（这个权限默认不会有），2 - 老师， 3 - 教务
    role = models.SmallIntegerField(default=0)

    # 归属学校
    school = models.ForeignKey('EduSchool')

    # 归属学院
    academy = models.ForeignKey('EduAcademy', blank=True, null=True)

    # 归属院系
    department = models.ForeignKey('EduDepartment', blank=True, null=True)

    # 归属专业
    major = models.ForeignKey('EduMajor', blank=True, null=True)

    class Meta:
        verbose_name = "教学系统 马甲账户"
        verbose_name_plural = "教学系统 马甲账户"

    def __str__(self):
        from wejudge.const import system
        return 'id = %s ；昵称：%s ；真实姓名：%s；身份：%s；主账户：（%s）' % \
        (
            self.id, self.nickname, self.realname,
            system.WEJUDGE_EDU_ACCOUNT_ROLES.call(self.role), self.master
        )


# 教学账户排行榜情况统计
class EduAccountRankList(models.Model, ModelConverter):

    # 教学账户关联
    account = models.ForeignKey('EduAccount')

    submission = models.IntegerField(default=0)

    accepted = models.IntegerField(default=0)

    penalty = models.IntegerField(default=0)

    solved = models.IntegerField(default=0)

    ratio = models.FloatField(default=0)

    wrong = models.IntegerField(default=0)


# 课程表
class Course(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学-课程"
        verbose_name_plural = "教学-课程"

    # 课程名称
    name = models.CharField(max_length=255, blank=True, default="")

    # 课程简介
    description = models.CharField(max_length=255, blank=True, default="")

    # 学年学期
    term = models.ForeignKey('EduYearTerm')

    # 归属学校
    school = models.ForeignKey('EduSchool')

    # 归属学院
    academy = models.ForeignKey('EduAcademy')

    # 归属院系
    department = models.ForeignKey('EduDepartment', blank=True, null=True)

    # 归属专业
    major = models.ForeignKey('EduMajor', blank=True, null=True)

    # 课程排课信息
    arrangements = models.ManyToManyField('Arrangement', blank=True)

    # 学生信息(选课信息, 废弃)
    students = models.ManyToManyField('EduAccount', blank=True, related_name="course_student")

    # 任课教师列表
    teacher = models.ManyToManyField('EduAccount', blank=True, related_name="course_teacher")

    # 助教名单
    assistants = models.ManyToManyField('EduAccount', blank=True, related_name="course_assistants")

    # 教学资源仓库列表
    repositories = models.ManyToManyField('Repository', blank=True)

    # 课程创建者（主干老师）
    author = models.ForeignKey('EduAccount', null=True, blank=True)

    def __str__(self):
        return u"%s.【%s】 %s" % (self.id, self.term, self.name)


# 排课信息表
class Arrangement(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学-课程-排课"
        verbose_name_plural = "教学-课程-排课"

    # 排课名称
    name = models.CharField(max_length=50, blank=True, default="")

    # 周几
    day_of_week = models.IntegerField(default=0)

    # 开始周
    start_week = models.IntegerField(default=0)

    # 结束周
    end_week = models.IntegerField(default=0, null=False, blank=False)

    # 单双周
    odd_even = models.IntegerField(default=0, null=False, blank=False)

    # 开始节
    start_section = models.IntegerField(default=0, null=False, blank=False)

    # 结束节
    end_section = models.IntegerField(default=0, null=False, blank=False)

    # 开始时间(24小时)
    start_time = models.TimeField(default=datetime.time())

    # 结束时间(24小时)
    end_time = models.TimeField(default=datetime.time())

    # 学生信息(选课信息)
    students = models.ManyToManyField('EduAccount', blank=True)

    def __getattr__(self, item):
        if item == 'toString':
            return self.toString()
        else:
            return self.__getattribute__(item)

    def toString(self):
        DAY_OF_WEEK = ["日", "一", "二", "三", "四", "五", "六", "日"]
        if self.odd_even == 1:
            odd = "【单周】"
        elif self.odd_even == 2:
            odd = "【双周】"
        else:
            odd = ""
        return "%s周%s 第%d-%d节 (%d-%d周)" % (
            odd, DAY_OF_WEEK[self.day_of_week], self.start_section, self.end_section, self.start_week, self.end_week
        )

    def __str__(self):
        return "[%s]%s" % (self.id, self.toString())


# 作业数据表
class Asgn(models.Model, ModelConverter):

    class Meta:
        verbose_name = "作业信息"
        verbose_name_plural = "作业信息"

    # 作业名称
    title = models.CharField(max_length=255, default="")

    # 作业发布老师
    teacher = models.ForeignKey("EduAccount", null=True, blank=True, related_name='teacher')

    # 作业描述
    description = models.TextField(default="")

    # 关联课程
    course = models.ForeignKey("Course")

    # 作业包含的题目
    problems = models.ManyToManyField('AsgnProblem', blank=True, related_name='asgn_items')

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 给分上限
    full_score = models.FloatField(default=0)

    # 评测语言
    lang = models.SmallIntegerField(default=0)

    # 评测状态关联
    judge_status = models.ManyToManyField('JudgeStatus', blank=True)

    # 排课权限控制
    access_control = models.ManyToManyField('AsgnAccessControl', blank=True)

    # 排行榜信息缓存(json)
    rank_list = models.TextField(default="")

    # 排行榜信息缓存时间
    rank_list_cache_time = models.IntegerField(default=0)

    #
    # # 黑名单
    # black_list = models.ManyToManyField("EduAccount", blank=True, related_name='black_list')

    # 隐藏题目标题
    hide_problem_title = models.BooleanField(default=False)

    # 隐藏学生提交的代码
    hide_student_code = models.BooleanField(default=False)

    # 归档保护
    archive_lock = models.BooleanField(default=False)

    # 参考答案代码公开时间（如果为空则表示不公开）
    public_answer_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "ID=%s, name=%s" % (self.id, self.title)


# 作业访问权限请求（调课管理）
class AsgnVisitRequirement(models.Model, ModelConverter):

    class Meta:
        verbose_name = "作业访问权限-调课请求"
        verbose_name_plural = "作业访问权限-调课请求"

    # 调课学生
    author = models.ForeignKey('EduAccount')

    # 作业
    asgn = models.ForeignKey("Asgn")

    # 排课目标信息
    arrangement = models.ForeignKey("Arrangement")

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)


# 题目的解决情况
class Solution(ProblemModel.SolutionBase, models.Model, ModelConverter):

    class Meta:
        verbose_name = "作业题目的解决情况"
        verbose_name_plural = "作业题目的解决情况"

        unique_together = (("author", "asgn", "problem"),)

    # 提交者
    author = models.ForeignKey("EduAccount")

    # 对应的作业
    asgn = models.ForeignKey('Asgn')

    # 对应的的题目
    problem = models.ForeignKey("AsgnProblem", null=True, blank=True)

    # 提交状态（多个）
    judge_status = models.ManyToManyField("JudgeStatus", blank=True)

    # 判题机给分
    score = models.FloatField(default=0)

    def __str__(self):
        return "ID=%s, asgnid=%s, stuid=%s, pid=%s, create_time=%s" % \
               (self.id, self.asgn_id, self.author_id, self.problem_id, self.create_time)


# 实验报告信息表
class AsgnReport(models.Model, ModelConverter):

    class Meta:
        verbose_name = "作业实验报告信息"
        verbose_name_plural = "作业实验报告信息"

        unique_together = (("author", "asgn"),)

    # 提交者
    author = models.ForeignKey("EduAccount")

    # 对应的作业
    asgn = models.ForeignKey('Asgn')

    # 评测机得分
    judge_score = models.FloatField(default=0)

    # 最终得分
    finally_score = models.FloatField(default=0)

    # 通过题目数量
    ac_counter = models.IntegerField(default=0)

    # 提交题目数量
    submission_counter = models.IntegerField(default=0)

    # 解决题目数量
    solved_counter = models.IntegerField(default=0)

    # 学生感想
    impression = models.TextField(blank=True, null=True)

    # 首次进入作业时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 首次进入作业时间（以进入作业时归属排课为准，取最早时间，排课发生调整不会影响这个值
    start_time = models.DateTimeField(null=True, blank=True)

    # 报告最后修改时间
    modify_time = models.DateTimeField(auto_now=True)

    # 老师是否批阅？
    teacher_check = models.BooleanField(default=False)

    # 老师的批语
    teacher_remark = models.TextField(null=True, blank=True)

    # 是否为优秀作业
    excellent = models.BooleanField(default=False)

    # 是否公开该学生的代码
    public_code = models.BooleanField(default=False)

    # 附件上传
    attachment = models.CharField(max_length=255, null=True, blank=True, default="")

    # Rank!
    # 解决问题数量
    rank_solved = models.IntegerField(default=0)

    # 总计用时
    rank_timeused = models.FloatField(default=0)

    def __str__(self):
        return "ID=%s, asgnid=%s, stuid=%s" % (self.id,self.asgn.id, self.author.id)


# 作业题目信息
class AsgnProblem(models.Model, ModelConverter):

    class Meta:
        verbose_name = "作业题目项信息"
        verbose_name_plural = "作业题目项信息"

    # 归属题目
    asgn = models.ForeignKey('Asgn', null=True, blank=True, related_name="item_of_asgn")

    # 题目关联
    entity = models.ForeignKey(ProblemModel.Problem)

    # 题目顺序
    index = models.IntegerField(default=0, db_index=True)

    # 通过题目数量
    accepted = models.IntegerField(default=0)

    # 提交题目数量
    submission = models.IntegerField(default=0)

    # 是否必做
    require = models.BooleanField(default=False)

    # 评测机给分
    score = models.FloatField(default=0)

    # 可用评测语言
    lang = models.SmallIntegerField(default=0)

    # 严格模式（默认关闭）
    strict_mode = models.BooleanField(default=False)

    # 错答最高给分(百分比)
    max_score_for_wrong = models.IntegerField(default=100)

    # 隐藏参考答案
    hidden_answer = models.BooleanField(default=False)

    def __getattr__(self, item):
        if item == 'judge_ratio':
            if self.accepted != 0:
                ratio = (self.accepted * 1.0) / self.submission * 100
            else:
                ratio = 0
            return '%.2lf%% (%s / %s)' % (ratio, self.accepted, self.submission)
        else:
            return self.__getattribute__(item)

    def __str__(self):
        return u"id = %s,  PID=%s" % (self.id, self.entity)


# 作业访问权限控制
class AsgnAccessControl(models.Model, ModelConverter):

    class Meta:
        verbose_name = "作业访问权限-控制"
        verbose_name_plural = "作业访问权限-控制"

    # 指向某个排课信息
    arrangement = models.ForeignKey("Arrangement")

    # 开始时间
    start_time = models.DateTimeField(null=True, blank=True)

    # 结束时间
    end_time = models.DateTimeField(null=True, blank=True)

    # 是否启用
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return u"id = %s,  arrangement = %s" % (self.id, self.arrangement)


# 作业系统的评测记录
class JudgeStatus(ProblemModel.JudgeStatusBase, models.Model, ModelConverter):

    class Meta:
        verbose_name = "作业评测记录"
        verbose_name_plural = "作业评测记录"

    # 对应题目
    problem = models.ForeignKey(ProblemModel.Problem, null=True, blank=True, related_name='asgn_status_problem')

    # 对应虚拟题目(asgn_problem_item)
    virtual_problem = models.ForeignKey('AsgnProblem', null=True, blank=True, related_name='asgn_status_vproblem')

    # 提交者
    author = models.ForeignKey('EduAccount', null=True, blank=True)

    def __str__(self):
        return u"id = %s,  pid = %s" % (self.id, self.problem.id)


# 教学资源仓库
class Repository(models.Model, ModelConverter):

    class Meta:
        verbose_name = "教学资源仓库"
        verbose_name_plural = "教学资源仓库"

    # 归属学校
    school = models.ForeignKey("EduSchool", blank=True, null=True)

    # 拥有者
    author = models.ForeignKey('EduAccount', blank=True, null=True)

    # 仓库名称
    title = models.CharField(max_length=255, blank=True, null=True)

    # 仓库最大容量(默认1G，字节)
    max_size = models.IntegerField(blank=False, null=False, default=1073741824)

    # 仓库当前容量(字节)
    cur_size = models.IntegerField(blank=False, null=False, default=0)

    # 公开等级：0-私有（课程可见），1-登录可见，2-任何人可见
    public_level = models.IntegerField(default=0)

    def __str__(self):
        return u'Repository: id = %d, author = %s, title = %s' % (self.id, self.author.nickname, self.title)

#
# # 教学资源仓库的文件系统
# class RepositoryFS(models.Model, ModelConverter):
#
#     class Meta:
#         verbose_name = "教学资源仓库文件系统表"
#         verbose_name_plural = "教学资源仓库文件系统表"
#
#     # 归属仓库
#     repository = models.ForeignKey('Repository', blank=True, null=True)
#
#     # 父节点（为NULL则是根节点下的文件）
#     parent = models.ForeignKey('RepositoryFS', db_index=True, blank=True, null=True, related_name='parent_node')
#
#     #  子节点
#     children = models.ManyToManyField('RepositoryFS', blank=True, related_name='children_nodes')
#
#     # 是否为目录
#     is_dir = models.BooleanField(default=False)
#
#     # 排序索引，一般不用设置
#     index = models.IntegerField(default=0)
#
#     # 文件名称
#     name = models.CharField(max_length=255, default="")
#
#     # 文件大小
#     size = models.IntegerField(default=0)
#
#     # 下载次数
#     download_count = models.IntegerField(default=0)
#
#     # 文件准确路径（保密）
#     entity = models.TextField(default="")
#
#     def __str__(self):
#         return u'id = %d, entity = %s' % (self.id, self.entity)