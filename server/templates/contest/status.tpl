{% extends "contest/component/base.tpl" %}
{% block contest_navbar %}{% include 'contest/component/navbar.tpl' %}{% endblock %}
{% load desc_status_flag %}
{% block page_title %}评测详情 - ID:{{ status.id }} - {{ contest.title }} - {% endblock %}
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
    {{ status.flag | desc_status_flag | safe }}
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
                    result: "{% url 'api.contest.judge.status.detail' contest.id status.id %}"
                },
                {

                }
            );
            {% if wejudge_session.logined and wejudge_session.account.role >= 1 %}
            wejudge.contest.contest.showStatusManager(
                'status_manager',
                {
                    do_delete: "{% url 'api.contest.judge.status.delete' contest.id status.id %}",
                    edit_status: "{% url 'api.contest.judge.status.edit' contest.id status.id %}",
                    load_status: "{% url 'api.contest.judge.status.body' contest.id status.id %}",
                    rejudge: "{% url 'api.contest.judge.status.rejudge' contest.id status.id %}"
                },
                {

                }
            );
            {% endif %}
        });
    </script>
{% endblock %}