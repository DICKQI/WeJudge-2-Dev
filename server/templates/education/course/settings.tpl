{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include "education/component/navbar_course.tpl" %}{% endblock %}
{% block page_title %}课程设置 - {{ course.name }} ({{ course.term }}) - {{ school.name }} - {% endblock %}
{% block page_body %}
<h3>课程设置</h3>
<div class="ui divider"></div>
<div id="container"></div>
<br/>
<h3>删除课程</h3>
<div class="ui divider"></div>
<form action="{% url 'api.education.delete.course' school.id course.id %}" method="post">
    <div class="ui large icon message">
        <i class="warning circle  icon"></i>
        <div class="content">
            <strong>警告：</strong>您应该很清楚您的操作即将带来的后果。
            <ol>
                <li>课程内所有作业信息将会被永久删除，无法恢复。</li>
                <li>所有关于该课程的设置信息都会被永久删除。</li>
                <li>当前操作仅能由教务管理员或该课程的创建者教师执行。</li>
            </ol>
            <label><input type="checkbox" name="agree" value="true">&nbsp;我愿意承担此操作带来的风险</label>
            <div class="ui divider"></div>
            <button type="submit" class="ui red button">删除课程</button>
        </div>
    </div>
</form>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.beans.register('course_settings', function() {
            return wejudge.education.course.showCourseSettings(
                "container",
                {
                    search_student: "{% url 'api.education.search.student'  school.id %}",
                    search_teacher: "{% url 'api.education.search.teacher'  school.id %}",
                    course_info: "{% url 'api.education.course.settings.info' school.id course.id %}",
                    save_settings: "{% url 'api.education.course.settings.save' school.id course.id %}",
                    toggle_assistant:"{% url 'api.education.course.assistants.toggle' school.id course.id %}",
                    toggle_teacher: "{% url 'api.education.course.teachers.toggle' school.id course.id %}"
                },
                {

                }
            );
        });
        wejudge.beans.getBean('course_settings').load();
    });
    </script>
{% endblock %}