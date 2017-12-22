
from django.conf.urls import url
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from .views import problemset
from .views import problem
from .views import problem_manager
from .views import status

urlpatterns = [
    # ProblemSet
    url(r'^set/index$', lambda request: HttpResponseRedirect(reverse('problem.set.list')), name="problem.index"),
    url(r'^set/list$', problemset.view_list, name='problem.set.list'),
    url(r'^set/(?P<psid>\d+)$', problemset.view_problemset, name='problem.set.view'),
    url(r'^set/problem/create$', lambda request: HttpResponseRedirect(reverse('problem.set.create.problem', args=(0,))),
        name="problem.set.create.problem.private"),
    url(r'^set/(?P<psid>\d+)/problem/create$', problemset.publish_problem, name='problem.set.create.problem'),

    # Problem
    url(r'^set/(?P<psid>\d+)/problem/(?P<pid>\d+)$',
        problem.view, name='problem.view'),

    # Problem Manager
    url('^set/(?P<psid>\d+)/problem/(?P<pid>\d+)/manager/judge$', problem_manager.judge_manager,
        name='problem.manager.judge'),
    url('^set/(?P<psid>\d+)/problem/(?P<pid>\d+)/manager/modify$', problem_manager.problem_editor,
        name='problem.manager.modify'),
    url('^set/(?P<psid>\d+)/problem/(?P<pid>\d+)/manager/relation$', problem_manager.problemset_relation,
        name='problem.manager.problemset.relation'),

    # Status
    url('^set/judge/status/(?P<sid>\d+)$', status.judge_status,
        name='problem.judge.status'),

    # ProblemSet API
    url(r'^set/api/list.json$', problemset.api_list_data, name='api.problem.set.list'),
    url(r'^set/(?P<psid>\d+)/api/info.json$', problemset.api_get_problemset_info,
        name='api.problem.set.info'),
    url(r'^set/(?P<psid>\d+)/api/problems/list.json$', problemset.api_problems_list_data,
        name='api.problem.set.problems.list'),
    url(r'^set/api/mine/problems/list.json$', problemset.api_problems_list_by_logined_user,
        name='api.problem.mine.problems.list'),
    url(r'^set/api/manager/create.do$', problemset.api_mgr_create_problemset,
        name='api.manager.problem.set.create'),
    url(r'^set/(?P<psid>\d+)/api/manager/modify.do$', problemset.api_mgr_modify_problemset,
        name='api.manager.problem.set.modify'),
    url(r'^set/(?P<psid>\d+)/api/manager/image/upload.do$', problemset.api_mgr_upload_problemset_image,
        name='api.manager.problem.set.image.upload'),
    url(r'^set/(?P<psid>\d+)/api/manager/problem/(?P<pid>\d+)/remove.do$', problemset.api_remove_from_problemset,
        name='api.manager.problem.set.remove.problem'),
    # == BATCH
    url(r'^set/(?P<psid>\d+)/classification/problems/moveto/classify/(?P<cid>\d+).do$',
        problemset.problem_moveto_classify, name='api.problemset.classification.problems.moveto'),
    url(r'^set/(?P<psid>\d+)/problems/moveto.do$',
        problemset.problem_moveto_problemset, name='api.problemset.problems.moveto'),
    url(r'^set/(?P<psid>\d+)/problems/remove.do$',
        problemset.problem_removefrom_problemset, name='api.problemset.problems.remove'),


    # Classification System API
    url(r'^set/(?P<psid>\d+)/classification/data.json$', problemset.get_classify_list,
        name='api.problemset.classification.data'),
    url(r'^set/(?P<psid>\d+)/classification/data.wejudge.json$', problemset.get_classify_list_wejudge,
        name='api.problemset.classification.data.wejudge'),
    url(r'^set/(?P<psid>\d+)/classification/change/classify/(?P<cid>\d+).do$',
        problemset.change_classify, name='api.problemset.classification.change'),


    # Problem API
    url(r'^set/api/problem/code/indent.do$', problem.api_code_indent,
        name='api.manager.code.indent'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/body.json$', problem.api_get_body,
        name='api.problem.view.body'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/submit.do$', problem.api_submit_code,
        name='api.problem.judge.submit'),

    url(r'^set/api/problem/(?P<pid>\d+)/code/drafts/get.json$', problem.get_code_drafts,
        name='api.problem.code.drafts.get'),
    url(r'^set/api/problem/(?P<pid>\d+)/code/drafts/save.do$', problem.save_code_draft,
        name='api.problem.code.drafts.save'),

    url(r'^set/api/problem/(?P<pid>\d+)/statistics/info.json$', problem.api_get_statistics,
        name='api.problem.statistics.info'),

    # Problem Manager API
    url(r'^set/(?P<psid>\d+)/api/problem/create.do$', problem_manager.create_problem,
        name='api.problem.manager.create'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/modify.do$', problem_manager.modify_problem,
        name='api.problem.manager.modify'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/config.json$',
        problem_manager.get_judge_config, name='api.problem.manager.get.judge.config'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/config/save.do$',
        problem_manager.save_judge_config, name='api.problem.manager.save.judge.config'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/judge/toggle.do$',
        problem_manager.toggle_judge, name='api.problem.manager.judge.toggle'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/special/judger/save.do$',
        problem_manager.save_specical_judge_program, name='api.problem.manager.special.judger.save'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/answer/save.do$',
        problem_manager.save_answer_case, name='api.problem.manager.answer.save'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/testcases/save.do$',
        problem_manager.save_test_cases_settings, name='api.problem.manager.test.cases.save'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/testcases/remove.do$',
        problem_manager.remove_test_cases, name='api.problem.manager.test.cases.remove'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/testcases/data.json$',
        problem_manager.get_test_cases_content, name='api.problem.manager.test.cases.data'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/testcases/data/save.do$',
        problem_manager.save_test_cases_content, name='api.problem.manager.test.cases.data.save'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/testcases/data/(?P<type>in|out)/upload.do$',
        problem_manager.upload_test_cases_content, name='api.problem.manager.test.cases.data.upload'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/testcases/maker/history.json$',
        problem_manager.get_tcmaker_status, name='api.problem.manager.test.cases.maker.history'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/testcases/maker/run.do$',
        problem_manager.tcmaker_run, name='api.problem.manager.test.cases.maker.run'),
    url(r'^set/api/problem/(?P<pid>\d+)/manager/testcases/maker/(?P<tcsid>\d+)/callback.do$',
        problem_manager.tcmaker_callback, name='api.problem.manager.test.cases.maker.callback'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/democases/save_code.do$',
        problem_manager.save_demo_cases_code, name='api.problem.manager.demo.case.code.save'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/democases/save.do$',
        problem_manager.save_demo_cases_settings, name='api.problem.manager.demo.case.save'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/democases/remove.do$',
        problem_manager.remove_demo_cases, name='api.problem.manager.demo.case.remove'),

    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/relations.json$',
        problem_manager.get_problemset_relations, name='api.problem.manager.relations'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/relations/publish.do$',
        problem_manager.publish_to_problemset, name='api.problem.manager.relations.public'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/manager/relations/remove.do$',
        problem_manager.remove_from_problemset, name='api.problem.manager.relations.remove'),



    # Judge Status API
    url(r'^set/api/judge/status/(?P<sid>\d+)/rolling/result.json$',
        problem.api_rolling_judge_status, name='api.problem.judge.status.rolling'),
    url(r'^set/api/judge/status/(?P<sid>\d+)/detail/result.json$',
        status.get_judge_detail, name='api.problem.judge.status.detail.result'),
    url(r'^set/(?P<psid>\d+)/api/judge/status/list.json$',
        problemset.api_judge_status_list, name='api.problemset.judge.status.list'),
    url(r'^set/(?P<psid>\d+)/api/problem/(?P<pid>\d+)/judge/status/list.json$',
        problem.api_judge_status_list, name='api.problem.judge.status.list'),

]
