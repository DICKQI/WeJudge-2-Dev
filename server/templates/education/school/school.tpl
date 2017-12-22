{% extends "education/component/base.tpl" %}
{% load attr %}
{% block edu_navbar %}{% include 'education/component/navbar_school.tpl' %}{% endblock %}
{% block page_title %}{{ school.name }} - {% endblock %}
{% block page_head %}
<style type="text/css">
    #bg_particles{
        background: {{ school.banner_style | safe }};
        background-size: 100% auto;
        filter: brightness(.5);
        height: auto;
        min-height: 260px;
        margin-bottom: 10px;
        position: absolute;
        width: 100%;
    }
    @media screen and (max-width: 767px) {
        .school_head_container {
            display: none;
        }
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
        padding-top: 40px;
        height: 280px;
    }
    .school_infos{
        color: #fff;
        text-shadow: 1px 1px 5px #333;
    }
    .pg-canvas{
        position: absolute;
    }
    #wejudge_breadcrumb_navbar{
        margin-bottom: 0 !important;
    }
</style>
{% endblock %}
{% block page_body %}
    <div id="bg_particles"></div>
    <div class="school_head_container">
        <div class="ui stackable grid">
            <div class="eight wide column school_infos">
                <h2>
                    {{ school.name }}
                </h2>
                <h4>{{ school.description }}</h4>
            </div>
            <div class="four wide column"></div>
            <div class="four wide column">
                {% if wejudge_session.logined %}
                <div class="ui segment">
                    <div class="ui grid">
                        <div class="ten wide column" style="padding: 8%;">
                            <h3>{{ wejudge_session.account.nickname | truncatechars:10 }}<br /><small>{{ wejudge_session.account.realname }}</small></h3>
                            <span><i class="users icon"></i> {{ WJ_EDU_ARC | attr:wejudge_session.account.role }}</span>
                        </div>
                        <div class="six wide column">
                             <img class="ui centered aligned small circular image" src="{% url 'education.account.space.avator' school.id wejudge_session.account.id %}">
                        </div>
                    </div>
                </div>
                {% else %}
                    <div class="ui segment">
                        <div class="ui grid">
                            <div class="ten wide column" style="padding: 8%;">
                                <h3>请登录<br /><small>以使用更多功能</small></h3>
                            </div>
                            <div class="six wide column">
                                 <img class="ui centered aligned small circular image" src="{% url 'account.space.avator' 0 %}">
                            </div>
                        </div>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
    <div class="my_page_container">
        <div class="ui stackable grid">
            <div class="twelve wide column" style="align-self: center;">
                {% include "breadcrumb.tpl" %}
            </div>
            <div class="four wide column">
                <select class="ui fluid dropdown" id="choose_term">
                    <option disabled>请选择学期</option>
                    {% for term in term_list %}
                    <option value="{{ term.id }}" {% if now_term == term %}selected{% endif %}>{{ term.year }} - {{ term.year | add:1 }}学年，第{{ term.term }}学期{% if school.now_term == term %}(当前学期){% endif %}</option>
                    {% endfor %}
                </select>
            </div>
        </div>
        <br />
        {{ index_view | safe }}
        <div id="school_container"></div>

    </div>
    <div id="maccount_leader_container"></div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.beans.register('school_index', function () {
            return wejudge.education.school.showSchoolIndexPage(
                "school_container",
                {
                    course_asgn_list: "{% url 'api.education.course_asgn.info' school.id %}",
                    course_data: "{% url 'api.education.courses.list' school.id %}",
                    create_course: "{% url 'api.education.course.create' school.id %}",
                    search_teacher: "{% url 'api.education.search.teacher' school.id %}"
                },
                {
                    course_view: "{% url 'education.course.index' school.id 0 %}",
                    asgn_view: "{% url 'education.asgn.index' school.id 0 %}"
                },
                {
                    is_logined: {% if wejudge_session.logined %}true{% else %}false{% endif %},
                    is_teacher: {% if wejudge_session.account.role >= 2 %}true{% else %}false{% endif %},
                    teacher_id:"{% if wejudge_session.account.role <= 2 %}{{ wejudge_session.account.username }}{% endif %}",
                    academies: eval('({{ academies | safe }})')
                }
            );
        });
        {% if wejudge_session.logined and wejudge_session.account.master is None %}
        wejudge.education.school.showMasterAccountLeader(
            'maccount_leader_container',
            {
                register_leader: "{% url 'api.education.bind.master' school.id %}"
            }
        ).show();
        {% endif %}
        $("#choose_term").dropdown({
           onChange:function (value) {
               window.location.href = "{% url 'education.school' school.id  %}?term=" + value;
           }
        });
    });
    </script>
{% endblock %}