{% extends "contest/component/base.tpl" %}
{% load attr %}
{% block contest_navbar %}{% include "contest/component/navbar.tpl" %}{% endblock %}
{% block page_title %}管理面板 - {{ contest.title }} - {% endblock %}
{% block page_head %}
<link rel="stylesheet" href="/static/assets/jstree/themes/default/style.min.css">
{% endblock %}
{% block page_body %}
<div class="ui tab" data-tab="settings">
    <div id="settings_container"></div>
</div>
<div class="ui tab" data-tab="accounts">
    <div id="accounts_container"></div>
</div>
<div class="ui tab" data-tab="choose_problem">
    {% if not wejudge_session.master_logined %}
        <div class="ui error icon message">
            <i class="warning circle icon"></i>
            <div class="content">
                <div class="header">请登录主账户</div>
                <div class="description">由于比赛账户和WeJudge主账户隔离机制，在没有登录WeJudge账户的情况下，您将不能查看一些私有的题库。</div>
            </div>
        </div>
    {% else %}
        <div class="ui positive icon message">
            <i class="checkmark circle icon"></i>
            <div class="content">
                <div class="header">正在以WeJudge主账户【{{ wejudge_session.master.nickname }}】的身份查看当前题库</div>
            </div>
        </div>
    {% endif %}
    <div id="choose_container"></div>
</div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/assets/jstree/jstree.min.js"></script>
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    <script type="text/javascript">
        $(function () {
            {% if wejudge_session.account.role == 1%}
            var is_admin = true;
            var is_referee = true;
            {% elif wejudge_session.account.role == 2%}
            var is_admin = true;
            var is_referee = true;
            {% else %}
            var is_admin = false;
            var is_referee = false;
            {% endif %}

            wejudge.beans.register('contest_settings', function () {
                return wejudge.contest.contest.showContestSettings(
                    "settings_container",
                    {
                        get_settings: "{% url 'api.contest.settings.info' contest.id %}",
                        save_settings: "{% url 'api.contest.settings.save' contest.id %}",
                        confirm_rank: "{% url 'api.contest.rank.confirm' contest.id %}",
                        refresh_data: "{% url 'api.contest.settings.refresh.data' contest.id %}"
                    },
                    {
                        rank_board: "{% url 'contest.rankboard' contest.id %}"
                    }
                );
            });
            wejudge.beans.register('contest_accounts', function () {
                return wejudge.contest.contest.showContestAccount(
                    "accounts_container",
                    {
                        account_list: "{% url 'api.contest.accounts.list' contest.id %}",
                        edit_account: "{% url 'api.contest.account.edit' contest.id %}",
                        delete_account: "{% url 'api.contest.account.delete' contest.id %}",
                        upload_xls: "{% url 'api.contest.account.import.upload' contest.id %}"
                    },
                    {}
                );
            });
            wejudge.beans.register('choose_problem', function () {
                return wejudge.problem.problemset.showProblemChoosing(
                    "choose_container",
                    {
                        problemset:{
                            list_problemset: "{% url 'api.problem.set.list' %}",
                            list_problem: "{% url 'api.problem.set.problems.list' 0 %}"
                        },
                        classify: {
                            get_data: "{% url 'api.problemset.classification.data.wejudge' 0 %}"
                        },
                        jstree: {
                            get_data: "{% url 'api.problemset.classification.data' 0 %}"
                        },
                        save_choosing: "{% url 'api.contest.settings.choose.problem' contest.id %}"
                    },
                    {
                        view_problem: "{% url 'problem.view' 0 0 %}"
                    },
                    {

                    }
                );
            });
            $("#MainNavList>.item").tab({
                history: true,
                onLoad: function () {
                    var tab_name = $(this).attr("data-tab");
                    if (tab_name === "settings"){
                        wejudge.beans.getBean('contest_settings').load();
                    }else if (tab_name === "accounts"){
                        wejudge.beans.getBean('contest_accounts').load();
                    }
                    else if(tab_name === 'choose_problem'){
                        wejudge.beans.getBean('choose_problem').init();
                    }
                }
            });
        });
    </script>
{% endblock %}
