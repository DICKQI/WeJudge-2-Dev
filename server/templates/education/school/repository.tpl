{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_school.tpl' %}{% endblock %}
{% load attr %}
{% block page_title %}教学资源仓库 - {{ school.name }} - {% endblock %}
{% block page_body %}
<div id="repository_container"></div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.education.repository.showRepositoryList(
            "repository_container",
            {
                'repotories_list': "{% url 'api.education.repository.list' school.id %}",
                'new_repo': "{% url 'api.education.repository.new' school.id %}"
            },
            {
                'repotory_view': "{% url 'education.repository.index' school.id 0 %}"
            },
            {
                is_teacher: {% if wejudge_session.account.role >= 2 %}true{% else %}false{% endif %}
            }
        ).load();
    });
    </script>
{% endblock %}