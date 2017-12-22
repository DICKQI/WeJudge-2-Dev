{% extends "wejudge/component/base.tpl" %}
{% block page_title %}{{ problem_entity.title }} - {{ problemset.title }} - {% endblock %}
{% block page_head %}
<link rel="stylesheet" href="/static/codemirror/lib/codemirror.css">
<link rel="stylesheet" href="/static/assets/highlight.css">
<style type="text/css">
.CodeMirror {
    border: 1px solid #eee;
{% if problem_entity.problem_type == 1 %}
    height: auto;
{% else %}
    height: 360px;
{% endif %}
}
img{
    max-width: 100%;
}
</style>
{% endblock %}
{% block page_body %}
    <div class="ui">
        <div style="margin: 20px auto;">
            <h2>{{ problem_entity.id }}. {{ problem_entity.title }}</h2>
        </div>
        <div id="MainContainer"></div>
    </div>
    <br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/codemirror/lib/codemirror.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/clike/clike.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/javascript/javascript.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/python/python.js"></script>
    <script type="text/javascript" src="/static/assets/highlight.pack.js"></script>
    <script type="text/javascript" src="/static/codemirror/addon/autorefresh.js"></script>
    <script type="text/javascript" src="/static/echars/echarts.common.min.js"></script>
    <script type="text/javascript">
        $(function () {
            wejudge.problem.problembody.showProblemView(
                "MainContainer",
                {
                    problem:  "{% url 'api.problem.view.body' pset_id problem_id %}",   // 读取题目内容和评测信息
                    judge: {
                        indent_code: "{% url 'api.manager.code.indent' %}",
                        submit: "{% url 'api.problem.judge.submit' pset_id problem_id %}",
                        rolling: "{% url 'api.problem.judge.status.rolling' 0 %}",
                        get_drafts: "{% url 'api.problem.code.drafts.get' problem_entity.id %}",
                        save_draft: "{% url 'api.problem.code.drafts.save' problem_entity.id %}"
                    },
                    history: {
                        list_status: "{% url 'api.problem.judge.status.list' pset_id problem_id %}"
                    },
                    statistics: {
                        data: "{% url 'api.problem.statistics.info' problem_entity.id %}"
                    }
                },
                {
                    {% if show_manager_link %}
                    manager: "{% url 'problem.manager.judge' pset_id problem_id %}",
                    {% endif %}
                    judge:{
                        view_detail: "{% url 'problem.judge.status' 0 %}"
                    },
                    history: {
                        view_problem: "{% url 'problem.view' pset_id 0 %}",
                        view_detail: "{% url 'problem.judge.status' 0 %}"
                    }
                },
                {
                    statistics: true,
                    history: {
                        realname:false,
                        full: false
                    },
                    user_id: "{{ wejudge_session.account.id }}"
                }
            );
        });
    </script>
{% endblock %}

