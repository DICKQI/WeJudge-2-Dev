{% extends "education/component/base.tpl" %}
{% load nav_user_call %}
{% block edu_navbar %}{% include "education/component/navbar_asgn.tpl" %}{% endblock %}
{% block page_title %}{{ asgn.title }} - {{ school.name }} - {% endblock %}
{% block page_head %}
    {% if wejudge_session.account.role >= 2 %}
        <link rel="stylesheet" href="/static/assets/jstree/themes/default/style.min.css">
    {% endif %}
    <link rel="stylesheet" href="/static/codemirror/lib/codemirror.css">
    <style type="text/css">
    .CodeMirror {
        height: 300px;
    }
    img {
        max-width: 100%;
    }
    td.green{
        background-color: #dff0d8;
    }
    td.red{
        background-color: #f2dede;
    }

    #bg_particles{
        background: #3498db;
        height: auto;
        min-height: 100px;
        margin-bottom: 30px;
    }
    .wj_page_container{
        width:100%;
    }
    .my_page_container {
        width:95%;
        height: auto;
        margin: 0 auto;
    }
    .ui.inverted.stackable.menu{
        margin-bottom: 0;
    }
    .school_head_container{
        width: 80%;
        margin: 0 auto;
        padding-top: 10px;
    }
    .school_infos{
        color: #fff;
        text-shadow: 1px 1px 5px #333;
    }
    .school_infos h1{
        margin-top: 10px;
    }
    .pg-canvas{
        position: absolute;
    }
    </style>
{% endblock %}
{% block page_body %}
<div id="bg_particles">
    <div class="school_head_container">
        <div class="ui stackable grid">
            <div class="eight wide column school_infos">
                <h1>{{ asgn.title }}</h1>
                <p>发布者：{{ asgn.teacher.realname }}老师；满分：{{ asgn.full_score }}{% if asgn_vstatus == 0 %}；还剩<span id="asgn_deadline_time"></span>截止{% endif %}</p>
            </div>
            <div class="four wide column"></div>
            <div class="four wide column">
                <div class="ui segment">
                    <div class="ui grid">
                        <div class="ten wide column" style="padding: 20px;">
                            <h3> {{ wejudge_session.account_manager | nav_user_call }}</h3>
                            {% if wejudge_session.account.role == 0 %}
                                <span>{% if asgn_report.teacher_check %}<span style="color: blue" title="已批改">{{ asgn_report.finally_score }}</span>{% else %}<span style="color: red" title="未批改">{{ asgn_report.judge_score }}</span>{% endif %} / {{ asgn.full_score }}</span>
                            {% else %}
                            <h4></h4>
                            {% endif %}
                        </div>
                        <div class="six wide column">
                             <img class="ui centered aligned tiny circular image" src="{% url 'education.account.space.avator' school.id wejudge_session.account.id %}">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="my_page_container">
    {% include "breadcrumb.tpl" %}
    <br />
    <div class="ui tab active" data-tab="problems">
        {% if asgn.description != None and asgn.description != "" %}
        <div class="ui secondary segment">
        <h3>附加说明</h3>
        {{ asgn.description | safe }}
        </div>
        {% endif %}
        <div id="problems_list_container"></div>
    </div>
    <div class="ui tab" data-tab="status">
        <div id="status_list_container"></div>
    </div>
    <div class="ui tab" data-tab="answer">
        <div id="answer_container"></div>
    </div>
    <div class="ui tab" data-tab="ranklist">
        <div id="ranklist_container"></div>
    </div>
    <br />
</div>
    <div id="maccount_leader_container"></div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    <script type="text/javascript" src="/static/codemirror/lib/codemirror.js"></script>
    <script type="text/javascript" src="/static/codemirror/addon/autorefresh.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/clike/clike.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/javascript/javascript.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/python/python.js"></script>
    {% if wejudge_session.account.role >= 2 %}
    <script type="text/javascript" src="/static/assets/jstree/jstree.min.js"></script>
    {% endif %}
    <script type="text/javascript">
    $(function () {
        wejudge.beans.register('problems_list', function(){
            return wejudge.education.asgn.showAsgnProblemsList(
                "problems_list_container",
                {
                    problems_list: "{% url 'api.education.asgn.problems' school.id asgn.id %}",
                    save_problem_setting: "{% url 'api.education.asgn.problem.settings.save' school.id asgn.id 0 %}",
                    remove_problem: "{% url 'api.education.asgn.problem.remove' school.id asgn.id 0 %}",
                    rejudge_problem: "{% url 'api.education.asgn.problem.rejudge' school.id asgn.id 0 %}",
                    {% if wejudge_session.account.role >= 2 %}
                    problem_choosing:{
                        problemset:{
                            list_problemset: "{% url 'api.problem.set.list' %}",
                            list_problem: "{% url 'api.problem.set.problems.list' 0 %}"
                        },
                        jstree: {
                            get_data: "{% url 'api.problemset.classification.data' 0 %}"
                        },
                        save_choosing: "{% url 'api.education.asgn.problems.choosing.save' school.id asgn.id %}",
                        highlight_items: "{% url 'api.education.asgn.problems.choosing.history' school.id asgn.id %}"
                    }
                    {% endif %}
                },
                {
                    problem_view: "{% url 'education.asgn.problem.view' school.id asgn.id 0 %}",
                    problem_manager: "{% url 'problem.manager.judge' 0 0 %}",
                    {% if wejudge_session.account.role >= 2 %}
                    problem_choosing:{
                        view_problem: "{% url 'problem.view' 0 0 %}"
                    }
                    {% endif %}
                },
                {% if wejudge_session.account.role >= 2 %}true{% else %}false{% endif %}
            );
        });
        wejudge.beans.register('status_list', function(){
            return wejudge.problem.judgestatus.showStatusList(
                "status_list_container",
                {
                    list_status: "{% url 'api.education.asgn.judge.status.list' school.id asgn.id %}"
                },
                {
                    view_problem: "{% url 'education.asgn.problem.view' school.id asgn.id 0 %}",
                    view_detail: "{% url 'education.asgn.judge.status.detail' school.id asgn.id 0 %}"
                },
                {
                    realname:true,
                    full: true,
                    app_name: "education"
                }
            );
        });
        wejudge.beans.register('asgn_rank_list', function () {
            return wejudge.education.asgn.showAsgnRankList(
                "ranklist_container",
                {
                    ranklist: "{% url 'api.education.asgn.rank.list' school.id asgn.id %}"
                },
                {
                    view_problem: "{% url 'education.asgn.problem.view' school.id asgn.id 0 %}",
                    view_rank_board: "{% url 'education.asgn.rank.board' school.id asgn.id %}"
                },
                {
                    arrangements: eval('({{ arrangements | safe }})')
                }
            );
        });
        wejudge.beans.register('asgn_answer', function () {
            return wejudge.education.asgn.showAsgnAnswer(
                "answer_container",
                {
                    get_answer: "{% url 'api.education.asgn.answer' school.id asgn.id %}"
                },
                {

                }
            );
        });

        $("#NavList>.item").tab({
            history: true,
            cache: false,
            alwaysRefresh: true,
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if(tab_name == "problems"){
                    wejudge.beans.getBean('problems_list').load();
                } else if (tab_name == "status"){
                    wejudge.beans.getBean('status_list').load();
{#                } else if (tab_name == "report") {#}
{#                    wejudge.beans.getBean('asgn_report').load();#}
                } else if (tab_name == "answer") {
                    wejudge.beans.getBean('asgn_answer').load();
                } else if (tab_name == "ranklist"){
                    wejudge.beans.getBean('asgn_rank_list').load();
                }
            }
        });
        {% if asgn_vstatus == 0 %}
        window.wejudge.global.countdown_timer({{ asgn_vdec }}, 'asgn_deadline_time');
        {% endif %}
        {% if wejudge_session.logined and wejudge_session.account.master is None %}
        wejudge.education.school.showMasterAccountLeader(
            'maccount_leader_container',
            {
                register_leader: "{% url 'api.education.bind.master' school.id %}"
            }
        ).show();
        {% endif %}
    });
    </script>
{% endblock %}