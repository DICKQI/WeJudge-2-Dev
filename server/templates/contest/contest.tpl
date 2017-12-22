{% extends "contest/component/base.tpl" %}
{% load attr %}
{% block contest_navbar %}{% include "contest/component/navbar.tpl" %}{% endblock %}
{% block page_title %}{{ contest.title }} - {% endblock %}
{% block page_head %}
    <link rel="stylesheet" href="/static/codemirror/lib/codemirror.css">
    <link rel="stylesheet" href="/static/assets/clock.css">
    <style type="text/css">
    td.green{
        background-color: #dff0d8;
    }
    td.red{
        background-color: #f2dede;
    }
    td.blue{
        background-color: #d9edf7;
    }
    img{
        max-width: 100%;
    }
    #bg_particles{
        background: #3498db;
        height: auto;
        min-height: 200px;
        margin-bottom: 30px;
    }
    .wj_page_container{
        width:100%;
    }
    .my_page_container {
        width:95%;
        min-height: 100%;
        height: auto;
        margin: 0 auto;
    }
    .ui.inverted.stackable.menu{
        margin-bottom: 0;
    }
    .school_head_container{
        width: 80%;
        margin: 0 auto;
        padding-top: 50px;
    }
    .school_infos{
        color: #fff;
        text-shadow: 1px 1px 5px #333;
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
            <div class="ten wide column school_infos">
                <h1>{{ contest.title }}</h1>
                <h3> {{ contest.start_time|date:"Y年m月d日 H:i:s"  }} - {{ contest.end_time|date:"Y年m月d日 H:i:s" }}</h3>
            </div>
            <div class="two wide column"></div>
            <div class="four wide column">
                {% if wejudge_session.logined %}
                <div class="ui segment">
                    <div class="ui grid">
                        <div class="ten wide column" style="padding: 8%;">
                            <h3>{{ wejudge_session.account.nickname | truncatechars:10 }}<br/><small>{{ wejudge_session.account.realname }}</small></h3>
                        </div>
                        <div class="six wide column">
                             <img class="ui centered aligned tiny circular image" src="{% if wejudge_session.account.headimg != None and wejudge_session.account.headimg != "" %}{{ wejudge_session.account.headimg }}{% else %}/static/images/user_placeholder.png{% endif %}">
                        </div>
                    </div>
                </div>
                {% else %}
                    <div class="ui segment">
                        <div class="ui grid">
                            <div class="ten wide column" style="padding: 8%;" onclick="wejudge.global.login('education')">
                                <h3>请登录<br /><small>以使用更多功能</small></h3>
                            </div>
                            <div class="six wide column">
                                 <img class="ui centered aligned tiny circular image" src="/static/images/user_placeholder.png">
                            </div>
                        </div>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
<div class="my_page_container">
    {% include "breadcrumb.tpl" %}
    <div class="ui basic segment" style="min-height: 100%; margin-top:0;">
        <!-- 这里是container的内容 -->
        <div class="ui tab active" data-tab="home">
            <div class="ui stackable grid">
                <div class="six wide column">
                    {% if not wejudge_session.logined %}
                        {% if contest.register_mode == 'register'   %}
                        {% if wejudge_session.master_logined %}
                            <div class="ui message">
                                <div class="header">欢迎您，{{ wejudge_session.master.nickname }}({{ wejudge_session.master.username }})</div>
                                本次比赛可以使用WeJudge主账号报名
                            </div>
                        {% else %}
                            <div class="ui message">
                                <div class="header">可以使用WeJudge主账号报名</div>
                                请先 <a href="javascript:void(0)" onclick="wejudge.global.login('master')">登录主账号</a>！
                            </div>
                        {% endif %}
                        {% endif %}
                         <div id="contest_login_container" style="margin: 0 auto; width: 350px"></div>
                    {% endif %}
                    <div id="notice_container"></div>
                </div>
                <div class="ui vertical divider" style="left: 37.5%;"><i class="hashtag icon"></i></div>
                <div class="ten wide column">
                    {{ index_view | safe }}
                </div>
            </div>
        </div>
        {% if wejudge_session.logined %}
        <div class="ui tab" data-tab="problems">
            <div id="problems_list_container"></div>
        </div>
        <div class="ui tab" data-tab="status">
            <div id="status_list_container"></div>
        </div>
        {% endif %}
        <div class="ui tab" data-tab="ranklist">
            <div id="ranklist_container"></div>
            <br />
            <i class="info circle icon"></i> 排行榜严格按照ACM比赛规则。出于性能考虑，自动刷新时间设定为60秒，如果需要强制刷新，请使用浏览器的刷新按钮。
        </div>

        {% if wejudge_session.logined %}
        <div class="ui tab" data-tab="faq">
            <div id="faq_container"></div>
        </div>
        <div class="ui tab" data-tab="cross_check">
            <div id="cross_check_container"></div>
        </div>
            <div class="ui tab" data-tab="printer_queue">
            <div id="printer_queue_container"></div>
        </div>
        <div class="ui tab" data-tab="settings">
            <div id="settings_container"></div>
        </div>
        <div class="ui tab" data-tab="account">
            <div id="account_container"></div>
        </div>
        {% endif %}
    </div>

</div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/assets/jcrop/js/jquery.Jcrop.min.js"></script>
    <script type="text/javascript" src="/static/assets/jquery.particleground.min.js"></script>
    <script type="text/javascript" src="/static/codemirror/lib/codemirror.js"></script>
    {% if wejudge_session.logined and wejudge_session.account.role == 2 %}
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    {% endif %}
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
            {% if not wejudge_session.logined %}
                 wejudge.contest.contest.showContestLogin(
                    "contest_login_container",
                    {
                        submit: "" // 嘛...不小心在wejudge.global里边注册有登录接口了，所以..无视这个吧。
                    },
                    {
                        register_mode: "{% if contest.register_mode == 'register' %}{% if wejudge_session.master_logined %}{{ contest.register_mode }}{% endif %}{% endif %}"
                    }
                );
            {% endif %}
{##}
{#            {% if not wejudge_session.logined and wejudge_session.master_logined and contest.register_mode == 'register' %}#}
{#                wejudge.contest.contest.showContestRegister(#}
{#                    "contest_register_container"#}
{#                );#}
{#            {% endif %}#}

            // Register the modules
            wejudge.beans.register('contest_rank_list', function () {
                return wejudge.contest.contest.showContestRankList(
                    "ranklist_container",
                    {
                        ranklist: "{% url 'api.contest.rank.list' contest.id %}"
                    },
                    {
                        view_problem: "{% url 'contest.problem' contest.id 0 %}"
                    },
                    is_referee
                );
            });
            wejudge.beans.register('contest_notice', function () {
                return wejudge.contest.contest.showContestNotice(
                    "notice_container",
                    {
                        notice_list: "{% url 'api.contest.notice.list' contest.id %}",
                        create_notice: "{% url 'api.contest.notice.new' contest.id %}",
                        delete_notice: "{% url 'api.contest.notice.delete' contest.id %}"
                    },
                    {

                    },
                    is_admin
                );
            });
            {% if wejudge_session.logined %}
            wejudge.beans.register('contest_problems_list', function () {
                return wejudge.contest.contest.showContestProblemsList(
                    "problems_list_container",
                    {
                        problems_list: "{% url 'api.contest.problems.list' contest.id %}",
                        save_problem_setting: "{% url 'api.contest.problem.settings.save' contest.id 0 %}",
                        remove_problem: "{% url 'api.contest.problem.remove' contest.id 0 %}",
                        rejudge_problem: "{% url 'api.contest.problem.rejudge' contest.id 0 %}"
                    },
                    {
                        problem_view: "{% url 'contest.problem' contest.id 0 %}",
                        manager_view: "{% url 'problem.manager.judge' 0 0 %}"
                    },
                    is_admin
                );
            });
            wejudge.beans.register('contest_status', function(){
                return wejudge.problem.judgestatus.showStatusList(
                    "status_list_container",
                    {
                        list_status: "{% url 'api.contest.judge.status.list' contest.id %}"
                    },
                    {
                        view_problem: "{% url 'contest.problem' contest.id 0 %}",
                        view_detail: "{% url 'contest.judge.status.detail' contest.id 0 %}"
                    },
                    {
                        realname: true,
                        nickname: true,
                        userid: true,
                        full: true,
                    }
                );
            });
            wejudge.beans.register('contest_faq', function () {
                return wejudge.contest.contest.showContestFAQ(
                    "faq_container",
                    {
                        faq_list: "{% url 'api.contest.faq.list' contest.id %}",
                        create_faq: "{% url 'api.contest.faq.new' contest.id %}",
                        reply_faq: "{% url 'api.contest.faq.reply' contest.id %}",
                        toggle_faq: "{% url 'api.contest.faq.toggle' contest.id %}",
                        delete_faq: "{% url 'api.contest.faq.delete' contest.id %}"
                    },
                    {

                    },
                    is_referee
                );
            });
            wejudge.beans.register('contest_cross_check', function () {
                return wejudge.contest.contest.showContestCrossCheck(
                    "cross_check_container",
                    {
                        crosscheck_list: "{% url 'api.contest.cross_check.list' contest.id %}",
                        delete_record: "{% url 'api.contest.cross_check.delete' contest.id %}",
                        read_code: "{% url 'api.contest.cross_check.code' contest.id %}"
                    },
                    {
                        view_problem: "{% url 'contest.problem' contest.id 0 %}",
                        view_detail: "{% url 'contest.judge.status.detail' contest.id 0 %}"
                    },
                    is_admin
                );
            });
            wejudge.beans.register('contest_printer', function () {
                return wejudge.contest.contest.showPrinterQueue(
                    "printer_queue_container",
                    {
                        printer_queue: "{% url 'api.contest.printer.queue.list' contest.id %}",
                        send_printer: "{% url 'api.contest.printer.queue.send' contest.id %}"
                    },
                    {
                        printer_page: "{% url 'contest.printer.view' contest.id 0 %}"
                    },
                    is_admin
                );
            });
            {% endif %}
            $("#MainNavList>.item").tab({
                history: true,
                onLoad: function () {
                    var tab_name = $(this).attr("data-tab");
                    {% if not wejudge_session.logined %}
                        if (tab_name === "ranklist"){
                            wejudge.beans.getBean('contest_rank_list').load();
                        }
                    {% else %}
                        if(tab_name === "problems"){
                            wejudge.beans.getBean('contest_problems_list').load();
                        }else if (tab_name === "status"){
                            wejudge.beans.getBean('contest_status').load();
                        }
                        else if (tab_name === "ranklist"){
                            wejudge.beans.getBean('contest_rank_list').load();
                        }else if (tab_name === "faq"){
                            wejudge.beans.getBean('contest_faq').getData();
                        }else if (tab_name === "home"){
                            wejudge.beans.getBean('contest_notice').getData();
                        }
                        else if (tab_name === "cross_check"){
                            wejudge.beans.getBean('contest_cross_check').load();
                        }
                        {% if contest.enable_printer_queue %}
                        else if (tab_name === "printer_queue"){
                            wejudge.beans.getBean('contest_printer').load();
                        }
                        {% endif %}
                    {% endif %}
                }
            });
            $('#bg_particles').particleground({
                dotColor: '#FFF',
                lineColor: '#FFF',
                parallax:false
            });
        });
    </script>
{% endblock %}
