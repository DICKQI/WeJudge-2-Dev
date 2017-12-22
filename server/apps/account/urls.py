from django.conf.urls import url
from .views import session
from .views import space

urlpatterns = [
    url(r'^wejudge/space/(?P<aid>\d+)/home$', space.wejudge.space, name='account.space'),
    url(r'^education/school/(?P<sid>\d+)/space/(?P<aid>\d+)/home$',
        space.education.space, name='account.education.space'),

    url(r'^wejudge/space/(?P<aid>\d+)/avator', space.wejudge.avator, name='account.space.avator'),
    url(r'^education/school/(?P<sid>\d+)/space/(?P<aid>\d+)/avator',
        space.education.avator, name='education.account.space.avator'),

    # === Session Manager API ===

    url(r'^api/wejudge/login.do$', session.wejudge.login_backend,
        name='api.account.login'),
    url(r'^api/wejudge/register.do$', session.wejudge.register,
        name='api.account.register'),
    url(r'^api/wejudge/logout.do$', session.wejudge.logout_backend,
        name='api.account.logout'),

    url(r'^api/contest/(?P<cid>\d+)/login.do$', session.contest.login_backend,
        name='api.contest.account.login'),
    url(r'^api/contest/(?P<cid>\d+)/logout.do$', session.contest.logout_backend,
        name='api.contest.account.logout'),
    url(r'^api/contest/(?P<cid>\d+)/master/check.json$', session.contest.check_master_login,
        name='api.contest.account.check.master'),
    url(r'^api/contest/(?P<cid>\d+)/master/login.do$', session.contest.login_use_master,
        name='api.contest.account.use.master.login'),

    url(r'^api/education/(?P<sid>\d+)/login.do$', session.education.login_backend,
        name='api.education.account.login'),
    url(r'^api/education/(?P<sid>\d+)/logout.do$', session.education.logout_backend,
        name='api.education.account.logout'),
    url(r'^api/education/(?P<sid>\d+)/master/check.json$', session.education.check_master_login,
        name='api.education.account.check.master'),
    url(r'^api/education/(?P<sid>\d+)/master/login.do$', session.education.login_use_master,
        name='api.education.account.use.master.login'),

    # === Space ===

    url(r'^api/wejudge/space/(?P<aid>\d+)/info.json$', space.wejudge.account_info,
        name='api.account.space.info'),

    url(r'^api/wejudge/space/(?P<aid>\d+)/info/save.do$', space.wejudge.save_account_infos,
        name='api.account.space.info.save'),
    url(r'^api/wejudge/space/(?P<aid>\d+)/headimg/upload.do$', space.wejudge.save_account_avatar,
        name='api.account.space.headimg.upload'),
    url(r'^api/wejudge/space/(?P<aid>\d+)/solutions/list.json$', space.wejudge.get_user_problem_solutions,
        name='api.account.space.solutions'),

    url(r'^api/education/school/(?P<sid>\d+)/space/(?P<aid>\d+)/info.json$',
        space.education.account_info, name='api.education.account.space.info'),
    url(r'^api/education/school/(?P<sid>\d+)/space/(?P<aid>\d+)/info/save.do$',
        space.education.save_account_infos, name='api.education.account.space.info.save'),
    url(r'^api/education/school/(?P<sid>\d+)/space/(?P<aid>\d+)/headimg/upload.do$',
        space.education.save_account_avatar, name='api.education.account.space.headimg.upload'),
    url(r'^api/education/school/(?P<sid>\d+)/space/(?P<aid>\d+)/solutions/list.json$',
        space.education.get_user_problem_solutions, name='api.education.account.space.solutions'),

    # === Oauth2 ===

    url(r'^oauth2/api/education/school/(?P<sid>\d+)/space/(?P<aid>\d+)/info.json$',
        space.education.oauth2_account_info, name='oauth2.api.education.account.space.info'),
    url(r'^oauth2/api/education/school/(?P<sid>\d+)/space/info.json$',
        space.education.oauth2_account_info, name='oauth2.api.education.account.space.info'),
]
