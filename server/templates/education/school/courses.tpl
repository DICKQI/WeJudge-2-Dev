{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_school.tpl' %}{% endblock %}
{% load attr %}
{% block page_title %}课程中心 - {{ school.name }} - {% endblock %}
{% block page_body %}
<div class="ui stackable grid" style="clear: both">
    <div class="four wide column">
        <select class="ui fluid dropdown" id="choose_term">
            <option disabled>请选择学期</option>
            {% for term in term_list %}
            <option value="{{ term.id }}" {% if now_term == term %}selected{% endif %}>{{ term.year }} - {{ term.year | add:1 }}学年，第{{ term.term }}学期</option>
            {% endfor %}
        </select>
        <div class="ui card" style="width: 100%;">
            <div class="ui centered aligned small image">
                <img src="{% url 'education.account.space.avator' school.id wejudge_session.account.id %}">
            </div>
            <div class="content">
                <a class="header">{{ wejudge_session.account.nickname }} ({{ wejudge_session.account.realname }})</a>
                <div class="description">上次登录：{% if wejudge_session.account.master != None %}{{ wejudge_session.account.master.last_login_time }}{% else %}{{ wejudge_session.account.last_login_time }}{% endif %}</div>
            </div>
            <div class="extra content">
                <i class="users icon"></i> {{ WJ_EDU_ARC | attr:wejudge_session.account.role }}
            </div>
        </div>
    </div>
    <div class="twelve wide column">
        <div id="course_list_container"></div>
    </div>
</div>
<br>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.beans.register('course_list', function () {
            return wejudge.education.school.showCourseManager(
                "course_list_container",
                {
                    course_data: "{% url 'api.education.course_asgn.info' school.id %}",
                    create_course: "{% url 'api.education.course.create' school.id %}",
                    search_teacher: "{% url 'api.education.search.teacher' school.id %}"
                },
                {
                    course_view: "{% url 'education.course.index' school.id 0 %}"
                },
                {
                    teacher_id:"{% if wejudge_session.account.role <= 2 %}{{ wejudge_session.account.username }}{% endif %}",
                    academies: eval('({{ academies | safe }})')
                }
            );
        });
        $("#choose_term").dropdown({
           onChange:function (value) {
               window.location.href = "{% url 'education.school.courses' school.id  %}?term=" + value;
           }
        });
    });
    </script>
{% endblock %}