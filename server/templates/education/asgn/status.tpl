{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_asgn.tpl' %}{% endblock %}
{% load desc_status_flag %}
{% block page_title %}评测详情 - ID:{{ status.id }} - {{ asgn.title }} - {% endblock %}
{% block page_head %}
<link rel="stylesheet" href="/static/codemirror/lib/codemirror.css">
<link rel="stylesheet" href="/static/jsdifflib/diffview.css">
<style type="text/css">
.CodeMirror {
    border: 1px solid #eee;
    height: 400px;
}
.diff-cp-contianer{
    height: 400px;
    overflow: auto;
    width: 100%;
}
.ui.segment{
    margin: 0;
}
</style>
{% endblock %}
{% block page_body %}
    {% if wejudge_session.logined and wejudge_session.account.role >= 1 %}
    <div id="status_manager"></div>
    {% endif %}
    {% if status.flag == 1 and not problem.strict_mode %}
        <h1 class="ui yellow header">数据通过(DA)</h1>
    {% else %}
    {{ status.flag | desc_status_flag | safe }}
    {% endif %}
    <div class="ui divider"></div>
    <div id="page_container"></div>
    <br /><br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/codemirror/lib/codemirror.js"></script>
    <script type="text/javascript" src="/static/codemirror/addon/autorefresh.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/clike/clike.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/javascript/javascript.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/python/python.js"></script>
    <script src="/static/jsdifflib/difflib.js"></script>
    <script src="/static/jsdifflib/diffview.js"></script>
    <script type="text/javascript">
        $(function () {
            wejudge.problem.judgestatus.showJudgeStatusDetail(
                "page_container",
                {
                    result: "{% url 'api.education.asgn.judge.status.detail' school.id asgn.id status.id %}"
                },
                {

                }
            );
            {% if wejudge_session.logined and wejudge_session.account.role >= 1 %}
            wejudge.contest.contest.showStatusManager(
                'status_manager',
                {
                    do_delete: "{% url 'api.education.asgn.judge.status.delete' school.id asgn.id status.id %}",
                    edit_status: "{% url 'api.education.asgn.judge.status.edit' school.id asgn.id status.id %}",
                    load_status: "{% url 'api.education.asgn.judge.status.body' school.id asgn.id status.id %}",
                    rejudge: "{% url 'api.education.asgn.judge.status.rejudge' school.id asgn.id status.id %}"
                },
                {

                }
            );
            {% endif %}
        });
    </script>
{% endblock %}