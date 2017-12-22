{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_course.tpl' %}{% endblock %}
{% block page_title %}教学资源 - {{ course.name }} ({{ course.term }})  - {{ school.name }} - {% endblock %}
{% block page_body %}
<div id="repository_container"></div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.education.repository.showRepositoryList(
            "repository_container",
            {
                'repotories_list': "{% url 'api.education.repository.list' school.id course.id %}",
                'toggle_in_course': "{% url 'api.education.course.repository.toggle'  school.id course.id %}"
            },
            {
                'repotory_view': "{% url 'education.repository.index' school.id 0 %}"
            },
            {
                is_teacher: {% if wejudge_session.account.role >= 2 %}true{% else %}false{% endif %},
                toggle_in_course: true
            }
        ).load();
    });
    </script>
{% endblock %}