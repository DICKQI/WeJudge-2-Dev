
from django.conf.urls import url
from .views import education
from .views import education
from .views import course
from .views import asgn
from .views import asgn_problem
from .views import asgn_status
from .views import repository

urlpatterns = [
    # Education（Maybe you have to choose your school, or use your last choose.
    url(r'^$', education.index, name='education.index'),

    url(r'^school/(?P<sid>\d+)$', education.school_index, name="education.school"),

    url(r'^school/(?P<sid>\w+)$', education.school_index, name="education.school"),

    url(r'^school/(?P<sid>\d+)/repository$', education.repository,
        name="education.school.repository"),

    url(r'^school/(?P<sid>\d+)/management$', education.management,
        name="education.school.management"),

    url(r'^school/(?P<sid>\d+)/repository/(?P<rid>\d+)$', repository.repository,
        name="education.repository.index"),

    # Education Course
    url(r'^school/(?P<sid>\d+)/course/(?P<cid>\d+)$', course.course,
        name='education.course.index'),

    url(r'^school/(?P<sid>\d+)/course/(?P<cid>\d+)/arrangements$', course.arrangements,
        name='education.course.arrangements'),

    url(r'^school/(?P<sid>\d+)/course/(?P<cid>\d+)/repository$', course.repository,
        name='education.course.repository'),

    url(r'^school/(?P<sid>\d+)/course/(?P<cid>\d+)/settings$', course.settings,
        name='education.course.settings'),

    # Education Asgn
    url(r'^school/(?P<sid>\d+)/asgn/(?P<aid>\d+)$', asgn.asgn_index,
        name='education.asgn.index'),

    url(r'^school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/manager$', asgn.asgn_manager,
        name='education.asgn.manager'),

    url(r'^school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/statistic$', asgn.asgn_statistic,
        name='education.asgn.statistic'),

    url(r'^school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/(?P<rid>\d+)$', asgn.asgn_report,
        name='education.asgn.report'),

    url(r'^school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problem/(?P<pid>\d+)$', asgn_problem.view_problem,
        name='education.asgn.problem.view'),

    url(r'^school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/rank/board$', asgn.asgn_rank_board,
        name='education.asgn.rank.board'),

    # Education Asgn Status

    url(r'^school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/(?P<status_id>\d+)$', asgn_status.judge_status,
        name='education.asgn.judge.status.detail'),

    # Education Index API
    url(r'^api/school/(?P<sid>\d+)/courses.json$', education.get_courses_list,
        name='api.education.courses.list'),

    url(r'^api/school/(?P<sid>\d+)/course_asgn/info.json$', education.api_course_asgn,
        name='api.education.course_asgn.info'),

    url(r'^api/school/(?P<sid>\d+)/account/list.json$', education.get_account_list,
        name='api.education.account.list'),

    url(r'^api/school/(?P<sid>\d+)/account/edit.do$', education.edit_account,
        name='api.education.account.edit'),

    url(r'^api/school/(?P<sid>\d+)/account/delete.do$', education.delete_account,
        name='api.education.account.delete'),

    url(r'^api/school/(?P<sid>\d+)/account/import.do$', education.xls_import_account,
        name='api.education.account.import'),

    url(r'^api/school/(?P<sid>\d+)/settings/info.json$', education.get_schools_info,
        name='api.education.settings.info'),

    url(r'^api/school/(?P<sid>\d+)/settings/sections/save.do$', education.save_sections_data,
        name='api.education.settings.sections.save'),

    url(r'^api/school/(?P<sid>\d+)/settings/yearterm/change.do$', education.change_year_terms,
        name='api.education.settings.yearterm.change'),

    url(r'^api/school/(?P<sid>\d+)/settings/save.do$', education.save_school_info,
        name='api.education.settings.save'),

    url(r'^api/school/(?P<sid>\d+)/search/student.json$', education.api_search_account([0]),
        name='api.education.search.student'),

    url(r'^api/school/(?P<sid>\d+)/search/teacher.json$', education.api_search_account([2, 3]),
        name='api.education.search.teacher'),

    url(r'^api/school/(?P<sid>\d+)/account/master/bind.do$', education.master_register_or_bind,
        name='api.education.bind.master'),

    # Education Course API
    url(r'^api/school/(?P<sid>\d+)/course/create.do$', education.create_course,
        name='api.education.course.create'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/delete$', course.delete_course,
        name='api.education.delete.course'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/asgns.json$', course.api_course_asgn,
        name='api.education.course.asgns'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/arrangements.json$', course.api_get_course_arrangements,
        name='api.education.course.arrangements'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/arrangement/(?P<arrid>\d+)/students.json$',
        course.api_get_students_by_arrangements, name='api.education.course.arrangement.students'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/arrangement/change.do$',
        course.api_change_arrangements, name='api.education.course.arrangement.change'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/arrangement/students/toggle.do$',
        course.api_toggle_student_to_arrangements, name='api.education.course.arrangement.toggle.student'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/settings.json$',
        course.get_course_settings_info, name='api.education.course.settings.info'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/settings/save.do$',
        course.save_course_settings, name='api.education.course.settings.save'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/assistants/toggle.do$',
        course.api_toggle_assistant_to_course, name='api.education.course.assistants.toggle'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/teachers/toggle.do$',
        course.api_toggle_teacher_to_course, name='api.education.course.teachers.toggle'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/repository/toggle.do$',
        course.api_toggle_repository_to_course, name='api.education.course.repository.toggle'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/arrangement/(?P<arrid>\d+)/student/import.do$',
        course.xls_student_to_arrangements, name='api.education.course.student.import'),

    url(r'api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/score/count.do$',
        course.asgn_score_count, name='api.education.course.score.counter'),

    # Education Asgn API
    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/asgn/create.do$',
        course.api_create_asgn, name='api.education.asgn.create'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/settings.json$',
        asgn.get_asgn_settings, name='api.education.asgn.settings'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/settings.do$',
        asgn.save_asgn_settings, name='api.education.asgn.settings.save'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/settings/delete$',
        asgn.delete_asgn, name='api.education.delete.asgn'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/settings/refresh_datas$',
        asgn.refresh_asgn_datas, name='api.education.asgn.refresh.datas'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problems.json$',
        asgn.asgn_problems_list, name='api.education.asgn.problems'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problems/choosing/save.do$',
        asgn.save_problem_choosing, name='api.education.asgn.problems.choosing.save'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problems/choosing/history.json$',
        asgn.get_problems_choosed, name='api.education.asgn.problems.choosing.history'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problem/(?P<pid>\d+)/rejudge.do$',
        asgn.rejudge_problems, name='api.education.asgn.problem.rejudge'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problem/(?P<pid>\d+).json$',
        asgn_problem.get_problem_body, name='api.education.asgn.problem.body'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problem/(?P<pid>\d+)/submit.do$',
        asgn_problem.api_submit_code, name='api.education.asgn.problem.judge.submit'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problem/(?P<pid>\d+)/judge/status/list.json$',
        asgn_problem.api_judge_status_list, name='api.education.asgn.problem.judge.status.list'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problem/(?P<pid>\d+)/settings/save.do$',
        asgn.save_asgn_problem_setting, name='api.education.asgn.problem.settings.save'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/problem/(?P<pid>\d+)/remove.do$',
        asgn.remove_asgn_problem, name='api.education.asgn.problem.remove'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/(?P<status_id>\d+)/rolling/result.json$',
        asgn_problem.api_rolling_judge_status, name='api.education.asgn.judge.status.rolling'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/list.json$',
        asgn.asgn_judge_status_list, name='api.education.asgn.judge.status.list'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/rank/list.json$',
        asgn.asgn_rank_list, name='api.education.asgn.rank.list'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/rank/boards/datas.json$',
        asgn.get_rank_board_datas, name='api.education.asgn.rank.boards.datas'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/(?P<rid>\d+).json$',
        asgn.get_asgn_report, name='api.education.asgn.report'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/list.json$',
        asgn.get_reports_list, name='api.education.asgn.report.list'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/impression/save.do$',
        asgn.save_asgn_report_impression, name='api.education.asgn.report.impression.save'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/attachment/upload.do$',
        asgn.upload_asgn_report_attchment, name='api.education.asgn.report.attachment.upload'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/(?P<rid>\d+)/attachment/download$',
        asgn.download_asgn_report_attchment, name='api.education.asgn.report.attachment.download'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/(?P<rid>\d+)/checkup/save.do$',
        asgn.save_asgn_report_checkup, name='api.education.asgn.report.checkup.save'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/report/batch/checkup/save.do$',
        asgn.save_asgn_report_checkup_batch, name='api.education.asgn.report.batch.checkup.save'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/answer.json$',
        asgn.get_answer, name='api.education.asgn.answer'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/visit/requirement.json$',
        asgn.get_visit_requirement, name='api.education.asgn.visit.requirement'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/visit/requirement/add.do$',
        asgn.add_visit_requirement, name='api.education.asgn.visit.requirement.add'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/visit/requirement/delete.do$',
        asgn.delete_visit_requirement, name='api.education.asgn.visit.requirement.delete'),

    # Education Asgn Status API
    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/(?P<status_id>\d+)/detail.json$',
        asgn_status.get_judge_detail, name='api.education.asgn.judge.status.detail'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/(?P<status_id>\d+)/body.json$',
        asgn_status.get_judge_status, name='api.education.asgn.judge.status.body'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/(?P<status_id>\d+)/edit.do$',
        asgn_status.edit_judge_status, name='api.education.asgn.judge.status.edit'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/(?P<status_id>\d+)/rejudge.do$',
        asgn_status.rejudge_status, name='api.education.asgn.judge.status.rejudge'),

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/judge/status/(?P<status_id>\d+)/delete.do$',
        asgn_status.delete_judge_status, name='api.education.asgn.judge.status.delete'),

    # Education Asgn Statistic API

    url(r'^api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/statistic/raw/datas.json$',
        asgn.get_statistic_data, name='api.education.asgn.statistic.raw.datas'),

    url(r'api/school/(?P<sid>\d+)/asgn/(?P<aid>\d+)/statistic/zip/code.do$' ,
        asgn.zip_the_codes ,name='api.education.asgn.statistic.zip.code'),

    # Repository API


    url(r'^api/school/(?P<sid>\d+)/repository/list.json$',
        repository.repositories_list, name='api.education.repository.list'),

    url(r'^api/school/(?P<sid>\d+)/course/(?P<cid>\d+)/repository/list.json$',
        repository.repositories_list, name='api.education.repository.list'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/info.json$',
        repository.repo_info, name='api.education.repository.info'),

    url(r'^api/school/(?P<sid>\d+)/repository/new.do$',
        repository.new_repo, name='api.education.repository.new'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/edit.do$',
        repository.edit_repo, name='api.education.repository.edit'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/delete.do$',
        repository.delete_repo, name='api.education.repository.delete'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/folders.json$',
        repository.get_folders_tree, name='api.education.repository.folders'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/files.json$',
        repository.get_files_map, name='api.education.repository.files'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/folders/new.do$',
        repository.repo_new_folder, name='api.education.repository.folders.new'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/files/upload.do$',
        repository.repo_upload_file, name='api.education.repository.files.upload'),

    url(r'^api/school/(?P<sid>\d+)/repository/(?P<rid>\d+)/filesystem/delete.do$',
        repository.repo_delete, name='api.education.repository.filesystem.delete'),
]
