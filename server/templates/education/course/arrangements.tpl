{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include "education/component/navbar_course.tpl" %}{% endblock %}
{% block page_title %}排课设置 - {{ course.name }} ({{ course.term }}) - {{ school.name }} - {% endblock %}
{% block page_body %}
<div id="container"></div>
<br/>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.beans.register('arrangements_list', function() {
            return wejudge.education.course.showArrangementsManager(
                "container",
                {
                    search_student: "{% url 'api.education.search.student'  school.id %}",
                    get_arrangements_list: "{% url 'api.education.course.arrangements' school.id course.id %}",
                    student_list: "{% url 'api.education.course.arrangement.students' school.id course.id 0 %}",
                    change_arrangement: "{% url 'api.education.course.arrangement.change' school.id course.id %}",
                    toggle_student: "{% url 'api.education.course.arrangement.toggle.student' school.id course.id %}",
                    toggle_student_by_xls: "{% url 'api.education.course.student.import' school.id course.id 0 %}"
                },
                {

                },
                {
                    max_week: {{ school.max_week }}
                }
            );
        });
        wejudge.beans.getBean('arrangements_list').load();
    });
    </script>
{% endblock %}