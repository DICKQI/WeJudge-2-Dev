
from django.conf.urls import url
from .views import contest
from .views import problem
from .views import status

urlpatterns = [
    # Contest Index
    url(r'^index$', contest.index, name='contest.index'),
    url(r'^(?P<cid>\d+)$', contest.contest, name='contest.contest'),
    url(r'^(?P<cid>\d+)/management$', contest.contest_management, name='contest.management'),
    url(r'^(?P<cid>\d+)/problem/(?P<pid>\d+)$', problem.view_problem, name='contest.problem'),
    url(r'^(?P<cid>\d+)/rank/board$', contest.rankboard, name='contest.rankboard'),
    url(r'^(?P<cid>\d+)/printer/page/(?P<pid>\d+)$', contest.printer_view, name='contest.printer.view'),
    url(r'^(?P<cid>\d+)/judge/status/(?P<sid>\d+)$', status.judge_status,
        name='contest.judge.status.detail'),

    # Contest API
    url(r'^api/list.json$', contest.get_contest_list,
        name='api.contest.list'),

    url(r'^api/create.do$', contest.create_contest,
        name='api.contest.create'),

    url(r'^api/contest/(?P<cid>\d+)/problems.json$', contest.get_problems_list,
        name='api.contest.problems.list'),

    url(r'^api/contest/(?P<cid>\d+)/problem/create.do$', problem.create_problem,
        name='api.contest.problem.create'),

    url(r'^api/contest/(?P<cid>\d+)/problem/(?P<pid>\d+).json$', problem.get_problem_body,
        name='api.contest.problem.body'),

    url(r'^api/contest/(?P<cid>\d+)/problem/(?P<pid>\d+)/submit.do$', problem.api_submit_code,
        name='api.contest.problem.judge.submit'),

    url(r'^api/contest/(?P<cid>\d+)/problem/(?P<pid>\d+)/judge/status/list.json$', problem.api_judge_status_list,
        name='api.contest.problem.judge.status.list'),

    url(r'^api/contest/(?P<cid>\d+)/problem/(?P<pid>\d+)/settings/save.json$', contest.save_contest_problem_setting,
        name='api.contest.problem.settings.save'),

    url(r'^api/contest/(?P<cid>\d+)/problem/add.do$', contest.add_contest_problem,
        name='api.contest.problem.add'),

    url(r'^api/contest/(?P<cid>\d+)/problem/(?P<pid>\d+)/remove.do$', contest.remove_contest_problem,
        name='api.contest.problem.remove'),

    url(r'^api/contest/(?P<cid>\d+)/problem/(?P<pid>\d+)/rejudge.do$', contest.rejudge_contest_problem,
        name='api.contest.problem.rejudge'),

    url(r'^api/contest/(?P<cid>\d+)/judge/status/(?P<sid>\d+)/rolling/result.json$', problem.api_rolling_judge_status,
        name='api.contest.judge.status.rolling'),

    url(r'^api/contest/(?P<cid>\d+)/judge/status/list.json$', contest.get_judge_status,
        name='api.contest.judge.status.list'),

    url(r'^api/contest/(?P<cid>\d+)/judge/status/(?P<sid>\d+)/detail.json$', status.get_judge_detail,
        name='api.contest.judge.status.detail'),

    url(r'^api/contest/(?P<cid>\d+)/judge/status/(?P<sid>\d+)/body.json$', status.get_judge_status,
        name='api.contest.judge.status.body'),

    url(r'^api/contest/(?P<cid>\d+)/judge/status/(?P<sid>\d+)/edit.do$', status.edit_judge_status,
        name='api.contest.judge.status.edit'),

    url(r'^api/contest/(?P<cid>\d+)/judge/status/(?P<sid>\d+)/rejudge.do$', status.rejudge_status,
        name='api.contest.judge.status.rejudge'),

    url(r'^api/contest/(?P<cid>\d+)/judge/status/(?P<sid>\d+)/delete.do$', status.delete_judge_status,
        name='api.contest.judge.status.delete'),

    url(r'^api/contest/(?P<cid>\d+)/rank/list.json$', contest.get_ranklist,
        name='api.contest.rank.list'),

    url(r'^api/contest/(?P<cid>\d+)/rank/board.json', contest.get_rank_board_datas,
        name='api.contest.rank.board'),

    url(r'^api/contest/(?P<cid>\d+)/rank/confirm.do$', contest.confirm_finally_rank,
        name='api.contest.rank.confirm'),

    url(r'^api/contest/(?P<cid>\d+)/faq/list.json$', contest.get_faq_list,
        name='api.contest.faq.list'),

    url(r'^api/contest/(?P<cid>\d+)/faq/create.do$', contest.new_faq,
        name='api.contest.faq.new'),

    url(r'^api/contest/(?P<cid>\d+)/faq/reply.do$', contest.reply_faq,
        name='api.contest.faq.reply'),

    url(r'^api/contest/(?P<cid>\d+)/faq/toggle.do$', contest.toggle_faq,
        name='api.contest.faq.toggle'),

    url(r'^api/contest/(?P<cid>\d+)/faq/delete.do$', contest.delete_faq,
        name='api.contest.faq.delete'),

    url(r'^api/contest/(?P<cid>\d+)/notice/list.json$', contest.get_notice_list,
        name='api.contest.notice.list'),

    url(r'^api/contest/(?P<cid>\d+)/notice/new.do$', contest.new_notice,
        name='api.contest.notice.new'),

    url(r'^api/contest/(?P<cid>\d+)/notice/delete.do$', contest.delete_notice,
        name='api.contest.notice.delete'),

    url(r'^api/contest/(?P<cid>\d+)/cross_check/list.json$', contest.get_cross_check_list,
        name='api.contest.cross_check.list'),

    url(r'^api/contest/(?P<cid>\d+)/cross_check/code.json$', contest.read_cross_check_code,
        name='api.contest.cross_check.code'),

    url(r'^api/contest/(?P<cid>\d+)/cross_check/delete.do$', contest.delete_cross_check_record,
        name='api.contest.cross_check.delete'),

    url(r'^api/contest/(?P<cid>\d+)/settings/info.json$', contest.get_contest_settings,
        name='api.contest.settings.info'),

    url(r'^api/contest/(?P<cid>\d+)/settings/save.do$', contest.save_contest_settings,
        name='api.contest.settings.save'),

    url(r'^api/contest/(?P<cid>\d+)/settings/refresh.data.do$', contest.refresh_contest_data,
        name='api.contest.settings.refresh.data'),

    url(r'^api/contest/(?P<cid>\d+)/settings/problems/choose.do$', contest.save_problem_choosing,
        name='api.contest.settings.choose.problem'),

    url(r'^api/contest/(?P<cid>\d+)/account/list.json$', contest.get_account_list,
        name='api.contest.accounts.list'),

    url(r'^api/contest/(?P<cid>\d+)/account/edit.do$', contest.edit_account,
        name='api.contest.account.edit'),

    url(r'^api/contest/(?P<cid>\d+)/account/delete.do$', contest.delete_account,
        name='api.contest.account.delete'),

    url(r'^api/contest/(?P<cid>\d+)/account/import/upload.do$', contest.xls_import_account,
        name='api.contest.account.import.upload'),

    url(r'^api/contest/(?P<cid>\d+)/account/register.do$', contest.user_register,
        name='api.contest.account.register'),

    url(r'^api/contest/(?P<cid>\d+)/account/change/passwd$', contest.user_changepwd,
        name='api.contest.account.passwd.change'),

    url(r'^api/contest/(?P<cid>\d+)/access/solutions/list.json$', contest.access_solution_list,
        name='api.contest.access.solutions.list'),

    url(r'^api/contest/(?P<cid>\d+)/access/accounts/list.json$', contest.access_contest_accounts,
        name='api.contest.access.accounts.list'),

    url(r'^api/contest/(?P<cid>\d+)/access/problems/list.json$', contest.access_contest_problems,
        name='api.contest.access.problems.list'),

    url(r'^api/contest/(?P<cid>\d+)/printer/queue/list.json$', contest.get_printer_queue,
        name='api.contest.printer.queue.list'),

    url(r'^api/contest/(?P<cid>\d+)/printer/queue/send.do$', contest.send_printer,
        name='api.contest.printer.queue.send'),

    url(r'^api/contest/(?P<cid>\d+)/printer/queue/delete.do$', contest.delete_printer_queue_item,
        name='api.contest.printer.queue.delete'),


]