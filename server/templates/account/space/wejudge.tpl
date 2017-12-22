{% extends "wejudge/component/base.tpl" %}
{% block page_title %}个人中心 - {{ account.nickname }} - {% endblock %}
{% block page_head %}
<link rel="stylesheet" href="/static/assets/jcrop/css/jquery.Jcrop.min.css">
<style type="text/css">
    #bg_particles{
        {% if account.sex == 0 %}
        background: #FFC0CB;
        {% else %}
        background: #2980b9;
        {% endif %}
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
    .space_head_container{
        width: 80%;
        margin: 0 auto;
        padding: 30px 0;
    }
    .space_username{
        color: #fff;
        text-shadow: 1px 1px 5px #333;
    }
    .space_username > h1{
        line-height: 75px;
    }
    .space_username > span{
        font-size: 1.5rem;
    }
    .pg-canvas{
        position: absolute;
    }
</style>
{% endblock %}
{% block page_body %}
    <div id="bg_particles">
        <div class="space_head_container">
            <div class="ui stackable grid">
                <div class="four wide column">
                    <img class="ui centered aligned small circular image" src="{% url 'account.space.avator' account.id %}">
                </div>
                <div class="twelve wide column space_username">
                    <h1>
                        {{ account.nickname }}
                        {% if account.sex == 0 %}<i class="woman icon" title="妹子"></i>{% elif account.sex == 1 %}<i class="man icon" title="汉子"></i>{% endif %}
                    </h1>
                    <span title="{{ account.motto }}">{% if account.motto != None and account.motto != "" %}{{ account.motto }}{% else %}这人很懒，什么也没写...{% endif %}</span>
                </div>
            </div>
        </div>
    </div>
    <div class="my_page_container">
        {% include "breadcrumb.tpl" %}
        <div class="ui secondary pointing menu" id="MainNavList">
            <a class="active item" data-tab="home">
                <i class="user icon"></i>
                账户信息
            </a>
            {% if wejudge_session.account == account %}
            <a class=" item" data-tab="settings">
                <i class="settings icon"></i>
                个人设置
            </a>
            {% endif %}
        </div>
        <div class="ui active tab" data-tab="home">
            <div class="ui stackable grid">
                <div class="five wide column">
                    <div class="ui two statistics">
                        <div class="statistic">
                            <div class="value">
                            {{ account_info.problem_visited.solved }}
                            </div>
                            <div class="label">
                            完成题目
                            </div>
                        </div>
                        <div class="statistic">
                            <div class="value">
                            {{ account_info.problem_visited.total }}
                            </div>
                            <div class="label">
                            访问题目
                            </div>
                        </div>
                    </div>
                    <table class="ui definition table">
                        {% if wejudge_session.account == account %}
                        <tr>
                            <td>登录名称</td>
                            <td>{{ account.username }}</td>
                        </tr>
                        <tr>
                            <td>安全邮箱</td>
                            <td>
                                {{ account.email | default:"未设置" }}
                                {% if not account.email_validated %}(未验证){% endif %}
                            </td>
                        </tr>
                        {% endif %}
                        <tr>
                            <td>真实姓名</td>
                            <td>{{ account.realname }}</td>
                        </tr>
                        <tr>
                            <td>创建时间</td>
                            <td>{{ account.create_time }}</td>
                        </tr>
                        <tr>
                            <td>上次登录</td>
                            <td>{{ account.last_login_time }}</td>
                        </tr>
                        <tr>
                            <td>管理网站 </td>
                            <td>{% if account.permission_administrator %}<i class="checkmark icon"></i>有{% else %}<i class="remove icon"></i>无{% endif %}</td>
                        </tr>
                        <tr>
                            <td>发布题目</td>
                            <td>{% if account.permission_publish_problem %}<i class="checkmark icon"></i>有{% else %}<i class="remove icon"></i>无{% endif %}</td>
                        </tr>
                        <tr>
                            <td>创建题集</td>
                            <td>{% if account.permission_create_problemset %}<i class="checkmark icon"></i>有{% else %}<i class="remove icon"></i>无{% endif %}</td>
                        </tr>
                        <tr>
                            <td>创建比赛</td>
                            <td>{% if account.permission_create_contest %}<i class="checkmark icon"></i>有{% else %}<i class="remove icon"></i>无{% endif %}</td>
                        </tr>
                    </table>
                </div>
                <div class="eleven wide column">
                    <div id="pv_container"></div>
                </div>
            </div>
        </div>
        {% if wejudge_session.account == account %}
        <div class="ui tab" data-tab="settings">
            <div id="settings_container"></div>
        </div>
        {% endif %}
    </div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/assets/jcrop/js/jquery.Jcrop.min.js"></script>
    <script type="text/javascript" src="/static/assets/jquery.particleground.min.js"></script>
    <script type="text/javascript">
    $(function () {
        $('#bg_particles').particleground({
            {% if account.sex == 0 %}
            dotColor: '#C7B3E5',
            lineColor: '#C7B3E5',
            {% else %}
            dotColor: '#3498db',
            lineColor: '#3498db',
            {% endif %}
            parallax:false
          });
        wejudge.beans.register('problem_visited_view', function () {
            return wejudge.account.space.showWeJudgeProblemVisited(
                'pv_container',
                {
                    vproblems_list: "{% url 'api.account.space.solutions' account.id %}"
                },
                {
                    view_problemset: "{% url 'problem.set.view' 0 %}",
                    view_problem: "{% url 'problem.view' 0 0 %}",
                }
            )
        });
        {% if wejudge_session.account == account %}
        wejudge.beans.register('account_settings', function () {
            return wejudge.account.space.showWeJudgeAccountSettings(
                'settings_container',
                {
                    account_infos: "{% url 'api.account.space.info' account.id %}",
                    save_settings: "{% url 'api.account.space.info.save' account.id %}",
                    upload_headimg: "{% url 'api.account.space.headimg.upload' account.id %}"
                },
                {}
            )
        });
        {% endif %}
        $("#MainNavList>.item").tab({
            history: true,
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if (tab_name == "home") {
                    wejudge.beans.getBean('problem_visited_view').load();
                }
                {% if wejudge_session.account == account %}
                else if(tab_name == "settings") {
                    wejudge.beans.getBean('account_settings').load();
                }
                {% endif %}
            }
        });
    })
    </script>
{% endblock %}