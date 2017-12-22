{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_school.tpl' %}{% endblock %}
{% load attr %}
{% block page_title %}{{ school.name }} - {% endblock %}
{% block page_body %}
{#<div class="ui stackable secondary pointing menu" id="NavList">#}
{#    <a class="active item" data-tab="index"><i class="home icon"></i> 学校首页</a>#}
{#    <a class="item" data-tab="problemset"><i class="list layout icon"></i> 教学题库</a>#}
{#    <!--a class="item">讨论板块</a>#}
{#    <!-- Master Teacher -->#}
{#    {% if wejudge_session.logined and wejudge_session.account.role == 3 %}#}
{#    <a class="item"><i class="users icon"></i> 账号管理</a>#}
{#    <a class="item"><i class="announcement icon"></i> 公告管理</a>#}
{#    {% endif %}#}
{#    <div class="right menu">#}
{##}
{#    </div>#}
{#</div>#}

<div class="ui stackable grid" style="clear: both">
    <div class="four wide column">
        <select class="ui fluid dropdown" id="choose_term">
            <option disabled>请选择学期</option>
            {% for term in term_list %}
            <option value="{{ term.id }}" {% if now_term == term %}selected{% endif %}>{{ term.year }} - {{ term.year | add:1 }}学年，第{{ term.term }}学期</option>
            {% endfor %}
        </select>
        {% if wejudge_session.logined %}
        <div class="ui card" style="width: 100%;">
            <div class="ui centered aligned small image">
                <img src="{% if wejudge_session.account.headimg != None and wejudge_session.account.headimg != "" %}{{ wejudge_session.account.headimg }}{% else %}/static/images/user_placeholder.png{% endif %}">
            </div>
            <div class="content">
                <a class="header">{{ wejudge_session.account.nickname }} ({{ wejudge_session.account.realname }})</a>
                <div class="description">上次登录：{% if wejudge_session.account.master != None %}{{ wejudge_session.account.master.last_login_time }}{% else %}{{ wejudge_session.account.last_login_time }}{% endif %}</div>
            </div>
            <div class="extra content">
                <i class="users icon"></i> {{ WJ_EDU_ARC | attr:wejudge_session.account.role }}
            </div>
        </div>
        <div id="my_course_asgn_container"></div>
        {% else %}
        <br />
        <div class="ui blue segment" style="max-width: 400px; margin: 0 auto;">
            <h2>用户登录 <small>{{  school.name  }}</small></h2>
            <div id="edu_login_container"></div>
        </div>
        {% endif %}
    </div>
    <div class="twelve wide column">
        <div class="ui items">
            <div class="item">
                <div class="content">
                    <a class="header">即将推出文章功能</a>
                    <div class="meta">
                        Pending
                    </div>
                    <div class="description">
                        Coming Soon!
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        {% if wejudge_session.logined %}
        {% if wejudge_session.account.role <= 2 %}
        wejudge.beans.register('my_course_asgn', function () {
            return wejudge.education.school.showSchoolIndexMyCourseAsgn(
                "my_course_asgn_container",
                {
                    data: "{% url 'api.education.course_asgn.info' school.id %}"
                },
                {
                    course_view: "{% url 'education.course.index' school.id 0 %}"
                }
            );
        });
        {% endif %}
        {% else  %}
        wejudge.beans.register('login_view', function () {
            return wejudge.education.school.showEducationLoginView('edu_login_container');
        });
        {% endif %}
        $("#choose_term").dropdown({
           onChange:function (value) {
               window.location.href = "{% url 'education.school' school.id  %}?term=" + value;
           }
        });
    });
    </script>
{% endblock %}