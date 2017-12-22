{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_school.tpl' %}{% endblock %}
{% load attr %}
{% block page_head %}
    <link rel="stylesheet" href="/static/assets/jstree/themes/default/style.min.css">
{% endblock %}
{% block page_title %}{{ repository.title }} - 教学资源仓库 - {{ school.name }} - {% endblock %}
{% block page_body %}
<div id="repository_container"></div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/assets/jstree/jstree.min.js"></script>
    <script type="text/javascript">
    $(function () {
        wejudge.education.repository.showRepositoryView(
            "repository_container",
            {
                'get_folders': "{% url 'api.education.repository.folders' school.id repository.id %}",
                'get_files': "{% url 'api.education.repository.files' school.id repository.id %}",
                'new_folder': "{% url 'api.education.repository.folders.new' school.id repository.id %}",
                'upload_file': "{% url 'api.education.repository.files.upload' school.id repository.id %}",
                'delete_path': "{% url 'api.education.repository.filesystem.delete' school.id repository.id %}",
                'edit_repo': "{% url 'api.education.repository.edit' school.id repository.id %}",
                'repo_info': "{% url 'api.education.repository.info' school.id repository.id %}",
                'delete_repo': "{% url 'api.education.repository.delete' school.id repository.id %}"
            },
            {
                'root': "/resource/repositories/{{ repository.id }}/",
                'repos_list': "{% url 'education.school.repository' school.id %}"
            },
            {
                is_teacher: {% if wejudge_session.account.role >= 2 %}true{% else %}false{% endif %}
            }
        ).load();
    });
    </script>
{% endblock %}