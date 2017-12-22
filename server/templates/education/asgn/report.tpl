{% extends "education/component/base.tpl" %}
{% load nav_user_call %}
{% block edu_navbar %}{% include "education/component/navbar_asgn.tpl" %}{% endblock %}
{% block page_title %}{{ asgn_report.author.realname }}的实验报告 - {{ asgn.title }} - {{ school.name }} - {% endblock %}
{% block page_head %}
    <link rel="stylesheet" href="/static/codemirror/lib/codemirror.css">
{% endblock %}
{% block page_body %}
<br />
<br />
<div id="report_container"></div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    <script type="text/javascript">
    $(function () {
        wejudge.education.asgn.showAsgnReport(
            "report_container",
            {
                get_report: "{% url 'api.education.asgn.report' school.id asgn.id asgn_report.id %}",
                save_impression: "{% url 'api.education.asgn.report.impression.save' school.id asgn.id %}",
                save_checkup: "{% url 'api.education.asgn.report.checkup.save' school.id asgn.id asgn_report.id %}",
                list_status: "{% url 'api.education.asgn.judge.status.list' school.id asgn.id %}",
                upload_attachment: "{% url 'api.education.asgn.report.attachment.upload' school.id asgn.id %}"
            },
            {
                view_problem: "{% url 'education.asgn.problem.view' school.id asgn.id 0 %}",
                view_status_detail: "{% url 'education.asgn.judge.status.detail' school.id asgn.id 0 %}",
                download_attachment: "{% url 'api.education.asgn.report.attachment.download' school.id asgn.id 0 %}"
            },
            "{% if wejudge_session.account.role == 0 %}student{% else %}teacher{% endif %}"
        ).load();
    });
    </script>
{% endblock %}