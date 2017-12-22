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
    <div class="ui segment" style="width: 400px; margin: 0 auto;">
        <h2>欢迎参加本次比赛！</h2>
        <div class="ui divider"></div>
        <h4>请立即更改您的密码，才能继续使用比赛的功能。</h4>
        <form action="{% url 'api.contest.account.passwd.change' contest.id %}" class="ui form" method="post">
            <div class="required field">
                <label>新密码</label>
                <div class="ui input">
                    <input type="password" name="password" />
                </div>
            </div>
            <div class="required field">
                <label>重复新密码</label>
                <div class="ui input">
                    <input type="password" name="repassword" />
                </div>
            </div>
            <input type="hidden" name="user_id" value="{{ wejudge_session.account.id }}">
            <strong><i>请务必牢记您的新密码，不要将其告知他人！并且忘记密码可能导致比赛资格被取消！</i></strong><br /><br />
            <button class="ui fluid primary button" type="submit">修改密码</button>
        </form>
    </div>
</div>
{% endblock %}
{% block page_script %}

{% endblock %}
