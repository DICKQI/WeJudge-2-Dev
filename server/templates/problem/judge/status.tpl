{% extends "wejudge/component/base.tpl" %}
{% load desc_status_flag %}
{% block page_title %}评测详情 - ID:{{ status.id }} - {% endblock %}
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
        wejudge.problem.judgestatus.showJudgeStatusDetail(
            "page_container",
            {
                result: "{% url 'api.problem.judge.status.detail.result' status.id %}",
            },
            {

            }
        );

    </script>
{% endblock %}