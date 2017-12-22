# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'

import os
import re
import json
import shutil
import logging
from wejudge.core import *
from wejudge.const import system
from django.utils.timezone import datetime
import apps.problem.models as ProblemModels
import apps.account.models as AccountModels
import apps.education.models as EducationModels
import apps.contest.models as ContestModels


students_cache = []

contest = ContestModels.Contest.objects.get(id=13)

courses = EducationModels.Course.objects.filter(id__in=[18,19, 20, 21,22,23,24])
for course in courses:
    arrs = course.arrangements.all()
    for arr in arrs:
        for stu in arr.students.all():
            username = stu.username
            if username in students_cache:
                continue
            c = ContestModels.ContestAccount()
            c.contest = contest
            c.username = username
            c.password = "1e77c00131d49d6518d7eba2f8ebe70ada7a1ac9d8e8fe7f3bd07f9d9ab635ca"
            c.nickname = stu.nickname
            c.realname = stu.realname
            c.sex = stu.sex
            c.save()
            print("%s Done." % stu.username)
            students_cache.append(stu.username)

#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \n%(message)s',
#     datefmt='%a, %d %b %Y %H:%M:%S',
#     filename='./export.log',
#     filemode='w'
#  )
#
#
# def log(msg):
#     logging.info(msg)
#     print(msg)
#
# # ==========================================
#
# fp = open("/data/tf/accounts.log", 'r')
# accounts_log = json.loads(fp.read())
# fp.close()
# fp = open("/data/tf/asgns.log", 'r')
# asgns_log = json.loads(fp.read())
# fp.close()
#
#
# def get_edu_account(author):
#     if author == "acm":
#         aid = 1331              # 6275
#     else:
#         aa = accounts_log.get(author)
#         if aa is None:
#             return None
#         aid = aa.get('edu')
#
#     a = EducationModels.EduAccount.objects.filter(id=aid)
#     return a[0] if a.exists() else None
#
# datas = os.listdir('/tmp/oj1/tf/solutions')
# page_count = len(datas)
# for page in range(1, page_count+1):
#     print("PAGE %s" % page)
#     fp = open(os.path.join('/tmp/oj1/tf/solutions', "%s.json" % page), 'r')
#     jsolutions = json.loads(fp.read())
#     fp.close()
#     for item in jsolutions:
#         sol = EducationModels.Solution()
#         author = get_edu_account(item.get('author_id'))
#         if author is None:
#             continue  # 抛弃不存在的用户的数据
#         asgn_id = item.get('asgn_id', 0)
#         asgn_item = asgns_log.get(str(asgn_id), {})
#         asgn = EducationModels.Asgn.objects.filter(id=asgn_item.get('id'))
#         if not asgn.exists():
#             continue
#         asgn = asgn[0]
#         asgn_problem = asgn_item.get('problems')
#         vproblem = EducationModels.AsgnProblem.objects.filter(id=asgn_problem.get(str(item.get('problems_id'))))
#         if not vproblem.exists():   # 抛弃题目不存在的
#             continue
#         sol.asgn = asgn
#         sol.author = author
#         sol.problem = vproblem[0]
#         sol.score = item.get('score', 0)
#         sol.accepted = item.get('accepted', 0)
#         sol.submission = item.get('submission', 0)
#         sol.penalty = sol.submission - sol.accepted
#         sol.save()
#
# print("SOL Done.")
#
# fp = open(os.path.join('/tmp/oj1/tf/reports.json'), 'r')
# reports = json.loads(fp.read())
# fp.close()
# cnt = 0
# for item in reports:
#     try:
#         report = EducationModels.AsgnReport()
#         author = get_edu_account(item.get('student_id'))
#         if author is None:
#             continue  # 抛弃不存在的用户的数据
#         asgn_id = item.get('asgn_id', 0)
#         asgn_item = asgns_log.get(str(asgn_id), {})
#         asgn = EducationModels.Asgn.objects.filter(id=asgn_item.get('id'))
#         if not asgn.exists():
#             continue
#         asgn = asgn[0]
#         report.asgn = asgn
#         report.author = author
#         report.judge_score = item.get('judge_score', 0)
#         report.finally_score = item.get('finally_score', 0)
#         report.ac_counter = item.get('ac_counter', 0)
#         report.submission_counter = item.get('submission_counter', 0)
#         report.solved_counter = item.get('solved_counter', 0)
#         report.solved_counter = item.get('solved_counter', 0)
#         report.impression = item.get('impression', "")
#         report.teacher_check = item.get('teacher_check', False)
#         report.teacher_remark = item.get('teacher_remark', "")
#         report.save()
#     except:
#         print("Err At: %s" % cnt)
#
#     cnt += 1
#     if cnt % 1000 == 0:
#         print(cnt)
#
# print("Done.")



#
# fp = open("/data/tf/accounts.log", 'r')
# accounts_log = json.loads(fp.read())
# fp.close()
# fp = open("/data/tf/asgns.log", 'r')
# asgns_log = json.loads(fp.read())
# fp.close()
#
#
# def get_edu_account(author):
#     if author == "acm":
#         aid = 1331              # 6275
#     else:
#         aa = accounts_log.get(author)
#         if aa is None:
#             return None
#         aid = aa.get('edu')
#
#     a = EducationModels.EduAccount.objects.filter(id=aid)
#     return a[0] if a.exists() else None
#
#
# def get_account(author):
#     if author == "acm":
#         aid = 2
#     elif author == "admin" or author == "padmin":
#         aid = 1
#     else:
#         aa = accounts_log.get(author)
#         if aa is None:
#             return None
#         aid = aa.get('wejudge')
#     a = AccountModels.Account.objects.filter(id=aid)
#     return a[0] if a.exists() else None
#
# SOURCE_CODE_EXTENSION = {
#     'gcc': 1,
#     'gcc-cpp': 2,
#     'java': 4
# }
#
# # 载入评测数据
# datas = os.listdir('/tmp/oj1/tf/status')
# page_count = len(datas)
# for page in range(1, page_count+1):
#     fp = open(os.path.join('/tmp/oj1/tf/status', "%s.json" % page), 'r')
#     jstatus = json.loads(fp.read())
#     fp.close()
#     for item in jstatus:
#         if item.get('flag') < 0:    # 除掉以前那些队列中什么的
#             continue
#         if item.get('id') <= 137548:
#             continue
#         callback = item.get('callback')
#         prov = callback.get('provider', '')
#         prov_id = callback.get('id', '')
#         if prov == "contest":       # 抛弃比赛的数据
#             continue
#
#         if prov == "asgn":  # 根据不同的系统查找不同的用户关联信息
#             author = get_edu_account(item.get('author_id'))
#             if author is None:
#                 continue  # 抛弃不存在的用户的数据
#             loga = asgns_log.get(str(prov_id))
#             if loga is None:     # 抛弃不存在的作业的数据
#                 continue
#             apids = loga.get('problems')
#             vproblem = EducationModels.AsgnProblem.objects.filter(id=apids.get(str(item.get('problem_id'))))
#             if not vproblem.exists(): # 抛弃题目不存在的
#                continue
#             vproblem = vproblem[0]
#             status = EducationModels.JudgeStatus()
#             status.problem = vproblem.entity
#             status.virtual_problem = vproblem
#             status.author = author
#         else:
#             author = get_account(item.get('author_id'))
#             if author is None:
#                 continue  # 抛弃不存在的用户的数据
#             vproblem = ProblemModels.ProblemSetItem.objects.filter(entity__id=item.get('problem_id'))
#             if not vproblem.exists():   # 抛弃题目不存在的
#                continue
#             vproblem = vproblem[0]
#             status = ProblemModels.JudgeStatus()
#             status.problem = vproblem.entity
#             status.virtual_problem = vproblem
#             status.author = author
#
#         status.flag = item.get('flag')
#         status.lang = SOURCE_CODE_EXTENSION.get(item.get('lang'), 1)
#         status.exe_time = item.get('exe_time')
#         status.exe_mem = item.get('exe_mem')
#         status.code_len = item.get('code_len')
#         try:
#             rel = json.loads(item.get('result'))
#
#         except:
#             rel = None
#         try:
#             fp = open(os.path.join("/tmp/oj1/code_submits", item.get('code_path')), "r")
#             code = fp.read()
#             fp.close()
#         except:
#             code = ""
#
#         cv_path = '/tmp/oj1/judgeouts/%s/' % item.get('id')
#         result = JudgeResult()
#         result.finally_code = code
#         if rel is not None:
#             result.ceinfo = rel.get('ce_info', '')
#             result.exitcode = rel.get('exitcode', -1)
#             result.timeused = rel.get('timeused', 0)
#             result.memused = rel.get('memused', 0)
#             dtl = rel.get('result', {})
#             if dtl is not None:
#                 for k, v in dtl.items():
#                     d = JudgeResultDetailItem()
#                     d.handle = k
#                     d.judge_result = v.get('result', -1)
#                     d.memory_used = v.get('memoryused', 0)
#                     d.time_used = v.get('timeused', 0)
#                     d.re_signum = v.get('re_signum', 0)
#                     d.re_call = v.get('re_call', 0)
#                     d.re_file = v.get('re_file', '')
#                     d.re_file_flag = v.get('re_file_flag', 0)
#                     result.details.append(d)
#
#             status.result = result.dump_json()
#         else:
#             status.result = {}
#         status.save()
#
#         try:
#             if os.path.exists(cv_path) and os.path.isdir(cv_path):
#                 storage = WeJudgeStorage(
#                     system.WEJUDGE_STORAGE_ROOT.JUDGE_RESULT, "education" if prov == 'asgn' else "problem"
#                 )
#                 storage = storage.get_child_storage(str(vproblem.entity_id))
#                 flag = shutil.copytree(cv_path, storage.get_folder_path(str(status.id)))
#                 log("写入输出数据成功 [%s] " % flag)
#         except Exception as ex:
#             log("写入评测结果数据失败!%s" % str(ex))
#
#         if prov == "asgn":      # 上面已经检查过一次了，这里不用检查了
#             loga = asgns_log.get(str(prov_id))
#             aid = loga['id']
#             asgn = EducationModels.Asgn.objects.get(id=aid)
#             asgn.judge_status.add(status)
#         else:
#             vproblem.problemset.judge_status.add(status)
#
#         log("Status %s => %s [Done]" % (item.get('id'), status.id))


# code = ""
# try:
#
# except:
#     code = ""


# fp = open("/data/tf/accounts.log", 'r')
# accounts_log = json.loads(fp.read())
# fp.close()
#
# def get_edu_account(author):
#     if author == "acm":
#         aid = 1
#     else:
#         aid = accounts_log.get(author).get('edu')
#     return EducationModels.EduAccount.objects.get(id=aid)
#
# # 载入教学数据
# fp = open("/tmp/oj1/tf/education.json", 'r')
# education_json = json.loads(fp.read())
# fp.close()
# # 日志
# log_fp = open("/data/tf/courses.log", 'w+')
# courses_log = {}
# # 导入课程
# school = EducationModels.EduSchool.objects.get(id=1)
# academy = EducationModels.EduAcademy.objects.get(id=1)
# TERM_ID = {
#     2014: {
#         1: 1,
#         2: 2
#     },
#     2015: {
#         1: 3,
#         2: 4
#     },
#     2016: {
#         1: 5,
#         2: 6
#     },
#     2017: {
#         1: 7
#     }
# }
# courses = education_json.get('courses')
# for item in courses:
#     print("Course: %s - %s" % (item.get('id'), item.get('name')))
#     term = EducationModels.EduYearTerm.objects.get(id=TERM_ID[item.get('year')][item.get('term')])
#     course = EducationModels.Course(term=term)
#     author = get_edu_account(item.get('teacher_id'))
#     course.school = school
#     course.author = author
#     course.name = item.get('name')
#     course.academy = academy
#     course.save()
#     course.teacher.add(author)
#     courses_log[item.get('id')] = course.id
# log_fp.write(json.dumps(courses_log))
# log_fp.close()
# # 导入作业
# log_fp = open("/data/tf/asgns.log", 'w+')
# asgns_log = {}
# asgns_list = education_json.get('asgns')
# for item in asgns_list:
#     print("Asgn: %s - %s" % (item.get('id'), item.get('name')))
#     asgn = EducationModels.Asgn()
#     author = get_edu_account(item.get('author_id'))
#     course = EducationModels.Course.objects.get(id=courses_log[item.get('course_id')])
#     asgn.teacher = author
#     asgn.course = course
#     asgn.title = item.get('name')
#     asgn.description = item.get('remark')
#     asgn.create_time = item.get('create_time')
#     asgn.full_score = item.get('full_score')
#     asgn.hide_problem_title = item.get('hideProblemTitle')
#     asgn.hide_student_code = item.get('hideProblemSubCode')
#     asgn.save()
#     aproblems = item.get('problems')
#     aproblems_log = {}
#     for apitem in aproblems:
#         ap = EducationModels.AsgnProblem()
#         ap.asgn = asgn
#         ap.entity = ProblemModels.Problem.objects.get(id=apitem.get('problem_id'))
#         ap.index = apitem.get('index')
#         ap.accepted = apitem.get('accepted')
#         ap.submission = apitem.get('submission')
#         ap.require = apitem.get('require')
#         ap.score = apitem.get('score')
#         ap.strict_mode = apitem.get('ignore_pe')
#         ap.max_score_for_wrong = apitem.get('pe_score')
#         ap.save()
#         asgn.problems.add(ap)
#         aproblems_log[apitem.get('problem_id')] = ap.id
#
#     asgns_log[item.get('id')] = {
#         'id': asgn.id,
#         'problems': aproblems_log
#     }
#
# log_fp.write(json.dumps(asgns_log))
# log_fp.close()

#
# # 导入题目信息
# fp = open("/tmp/oj1/tf/problems.json", 'r')
# problems_json = json.loads(fp.read())
# fp.close()
# pset = ProblemModels.ProblemSet.objects.filter(id=1)[0]
# # 读取分类
# fp = open("/data/tf/classify.log", 'r')
# classify_log = json.loads(fp.read())
# fp.close()
# # 读取用户
# fp = open("/data/tf/accounts.log", 'r')
# accounts_log = json.loads(fp.read())
# fp.close()
# for item in problems_json:
#     log("Problem: %s" % item.get('id'))
#     problem = ProblemModels.Problem()
#     problem.id = item.get('id')
#     problem.title = item.get('title')
#     author = item.get('author_id', 'admin')
#     if author == "acm":
#         author = 2
#     elif author == "admin" or author == 'padmin':
#         author = 1
#     else:
#         author = accounts_log.get(author).get('wejudge')
#     problem.author = AccountModels.Account.objects.get(id=author)
#     problem.difficulty = item.get('difficulty')
#     problem.create_time = datetime.fromtimestamp(item.get('create_time'))
#     problem.description = item.get('description')
#     problem.input = item.get('input')
#     problem.output = item.get('output')
#     problem.sample_input = item.get('sample_input')
#     problem.sample_output = item.get('sample_output')
#     problem.hint = item.get('hint')
#     problem.source = item.get('source')
#     problem.description = item.get('description')
#     problem.pause_judge
#     if item.get('disable_edit_by_other'):
#         problem.permission = 3
#     config = JudgeConfig()
#     config.judge_type = 0
#     config.time_limit[1] = item.get('c_time_limit', 1000)
#     config.time_limit[2] = item.get('c_time_limit', 1000)
#     config.time_limit[4] = item.get('java_time_limit', 2000)
#     config.mem_limit[1] = item.get('c_time_limit', 32768)
#     config.mem_limit[2] = item.get('c_time_limit', 32768)
#     config.mem_limit[4] = item.get('java_time_limit', 262144)
#     for td in item.get('test_datas', []):
#         tcitem = JudgeTestCaseItem()
#         tcitem.handle = td.get('handle')
#         tcitem.order = td.get('order')
#         tcitem.name = td.get('name')
#         tcitem.update_time = td.get('update_time')
#         tcitem.available = td.get('available')
#         tcitem.visible = td.get('visible')
#         tcitem.score_precent = td.get('score_precent')
#         config.test_cases.append(tcitem)
#     problem.judge_config = config.dump_json()
#     problem.save()
#     pitem = ProblemModels.ProblemSetItem()
#     pitem.problemset = pset
#     pitem.entity = problem
#     if item.get('classification', None) is not None:
#         print(item.get('classification', None))
#         pitem.classification = ProblemModels.ProblemClassify.objects.get(id=classify_log.get(str(item.get('classification'))))
#     pitem.save()
#     pset.items.add(pitem)
#
#     # 保存配置文件
#     root_storage = WeJudgeStorage(system.WEJUDGE_STORAGE_ROOT.PROBLEMS_DATA, str(problem.id))
#     try:
#         root_storage.new_folder("test_cases")
#         root_storage.new_folder("env")
#         root_storage.new_folder("special_judge")
#         root_storage.new_folder("library")
#         root_storage.new_folder("code_cases")
#         fp = root_storage.open_file("judge.json", "w")
#         fp.write(problem.judge_config)
#         fp.close()
#     except Exception as ex:
#         log("写入Judge配置信息到文件失败! [%s] " % str(ex))
#
#     # 保存参考答案代码
#     SOURCE_CODE_EXTENSION = {
#         'gcc': 1,
#         'gcc-cpp': 2,
#         'java': 4
#     }
#     try:
#         if item.get('demo_code') is None or item.get('demo_code').strip() == "":
#             log("此题没有参考答案代码")
#         else:
#             demo_code = json.loads(item.get('demo_code'))
#             lang = SOURCE_CODE_EXTENSION[demo_code.get('lang')]
#             code = demo_code.get('content')
#             storage = root_storage.get_child_storage("code_cases")
#             fp = storage.open_file("%s.answer" % lang, "w")
#             fp.write(code)
#             fp.close()
#     except Exception as ex:
#         log("写入参考答案数据失败! [%s] " % str(ex))
#
#     # 转移测试数据
#     for td in item.get('test_datas', []):
#         try:
#                 storage = root_storage.get_child_storage("test_cases")
#                 infile = "/tmp/oj1/testdatas/%s/%s.in" % (problem.id, td.get('handle'))
#                 outfile = "/tmp/oj1/testdatas/%s/%s.out" % (problem.id, td.get('handle'))
#                 if not os.path.exists(infile):
#                     storage.open_file("%s.in" % td.get('handle'), "w+").close()
#                 else:
#                     storage.clone_from_file("%s.in" % td.get('handle'), infile)
#                 if not os.path.exists(outfile):
#                     storage.open_file("%s.out" % td.get('handle'), "w+").close()
#                 else:
#                     storage.clone_from_file("%s.out" % td.get('handle'), outfile)
#         except Exception as ex:
#             log("写入测试数据[%s]失败! [%s] " % (td.get('handle'), str(ex)))
#
# pset.items_count = pset.items.count()
# pset.save()
# print("Done.")

# # 导入题目分类信息
# fp = open("/tmp/oj1/tf/classify.json", 'r')
# problems_json = json.loads(fp.read())
# fp.close()
# # 打开日志
# fp = open("/data/tf/classify.log", 'w+')
# classify_log = {}
# # 打开题库数据
# pset = ProblemModels.ProblemSet.objects.filter(id=1)[0]
# for item in problems_json:
#     print(item)
#     # 读取分类信息
#     c = ProblemModels.ProblemClassify()
#     c.problemset = pset
#     c.title = item.get('title')
#     if item.get('parent_id', None) is not None:
#         c.parent = ProblemModels.ProblemClassify.objects.filter(id=classify_log.get(item.get('parent_id')))[0]
#     c.save(force_insert=True)
#     classify_log[item.get('id')] = c.id
#
# fp.write(json.dumps(classify_log))
# fp.close()

#
# # 导入用户信息
# fp = open("/tmp/oj1/tf/accounts.json", 'r')
# accounts_json = json.loads(fp.read())
# fp.close()
# # 导入日志
# fp = open("/data/tf/accounts.log", 'w+')
# accounts_log = {}
# # 初始化
# school = EducationModels.EduSchool.objects.filter(id=1)[0]
#
# for item in accounts_json:
#     role = item.get('role')
#     headimg = item.get('headimg', None)
#     if headimg is None:
#         headimg = ""
#     if role in [1, 2]:       # 学生, 老师
#         # 主账户
#         a = AccountModels.Account()
#         a.username = "bnuz_%s" % item.get('id')
#         a.password = item.get('password')
#         a.sex = item.get('sex')
#         a.nickname = remove_emoji(item.get('nickname'))
#         a.realname = item.get('realname')
#         a.email = item.get('email')
#         a.email_validated = item.get('email_validated')
#         a.motto = item.get('motto')
#         if role == 2:
#             a.permission_publish_problem = True
#             a.permission_create_problemset = True
#             a.permission_create_contest = True
#         a.save()
#         a.headimg = "wejudge/%s%s" % (
#             a.id, ".jpg" if '.jpg' in headimg else '.png'
#         ) if headimg != "" else None
#         a.save()
#
#         # 教学账户
#         ea = EducationModels.EduAccount()
#         ea.school = school
#         ea.master = a
#         ea.role = 0 if role == 1 else 2
#         ea.username = item.get('id')
#         # ea.password = item.get('password')    不需要了
#         ea.sex = item.get('sex')
#         ea.nickname = remove_emoji(item.get('nickname'))
#         ea.realname = item.get('realname')
#         ea.email = item.get('email')
#         ea.motto = item.get('motto')
#         ea.save()
#         ea.headimg = "education/%s%s" % (
#             ea.id, ".jpg" if '.jpg' in headimg else '.png'
#         ) if headimg != "" else None
#         ea.save()
#
#         # 复制头像：
#         if headimg != "":
#             ff = open('/tmp/oj1/resource/headimg/%s' % headimg, 'rb')
#             fo = open('/data/resource/headimg/wejudge/%s%s' % (
#                 a.id, ".jpg" if '.jpg' in headimg else '.png'
#             ), 'wb')
#             fe = open('/data/resource/headimg/education/%s%s' % (
#                 ea.id, ".jpg" if '.jpg' in headimg else '.png'
#             ), 'wb')
#             fo.write(ff.read())
#             fe.write(ff.read())
#             fo.close()
#             fe.close()
#             ff.close()
#
#         # 写入历史记录
#         accounts_log[item.get('id')] = {
#             'edu': ea.id,
#             'wejudge': a.id
#         }
#
#         log("%s => %s [edu : %s]" % (item.get('id'), a.id, ea.id))
#
#     elif role == 3:     # 特殊有效账户
#         a = AccountModels.Account()
#         a.username = item.get('id')
#         a.password = item.get('password')
#         a.sex = item.get('sex')
#         a.nickname = remove_emoji(item.get('nickname'))
#         a.realname = item.get('realname')
#         a.email = item.get('email')
#         a.email_validated = item.get('email_validated')
#         a.motto = item.get('motto')
#         a.save()
#
#         accounts_log[item.get('id')] = {
#             'wejudge': a.id
#         }
#         log("%s => %s" % (item.get('id'), a.id))
#
#     else:
#         continue
#
#
# fp.write(json.dumps(accounts_log))
# fp.close()


