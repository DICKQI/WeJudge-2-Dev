{% extends "contest/component/base.tpl" %}
{% block contest_navbar %}{% include 'contest/component/navbar.tpl' %}{% endblock %}
{% load problem_index %}
{% block page_title %}{% if contest.hide_problem_title %}题目{{ problem.index | problem_index }}{% else  %}{{ problem.index | problem_index }}. {{ problem_entity.title }}{% endif %} - {{ contest.title }} - {% endblock %}
{% block page_head %}
<link rel="stylesheet" href="/static/codemirror/lib/codemirror.css">
<link rel="stylesheet" href="/static/assets/highlight.css">
<style type="text/css">
.CodeMirror {
    border: 1px solid #eee;
{% if problem_entity.problem_type == 1 %}
    height: auto;
{% else %}
    height: 400px;
{% endif %}
}
img{
    max-width: 100%;
}
</style>
{% endblock %}
{% block page_body %}
{#<div class="ui stackable grid">#}
{#    <div class="three wide column">#}
{#        <div class="ui secondary vertical pointing menu">#}
{#            <p class="item"><strong style="font-size: 1.2em;">题目列表</strong></p>#}
{#            {% for lproblem in problems_list %}#}
{#            <a class="{% if problem.id == lproblem.id %}active {% endif %}item"#}
{#                href="{% url 'contest.problem' contest.id lproblem.id %}"#}
{#            >{% if contest.hide_problem_title %}题目{{ lproblem.index | problem_index }}{% else  %}{{ lproblem.index | problem_index }}. {{ lproblem.entity.title }}{% endif %}</a>#}
{#            {% endfor %}#}
{#        </div>#}
{#    </div>#}
{#    <div class="thirteen wide column">#}
{#        <div style="margin: 20px auto;">#}
{#            <h2>{% if contest.hide_problem_title %}题目{{ problem.index | problem_index }}{% else  %}题目{{ problem.index | problem_index }}. {{ problem_entity.title }}{% endif %}</h2>#}
{#        </div>#}
{#        <div id="MainContainer"></div>#}
{#    </div>#}
{#</div>#}
<div class="ui pointing menu">
    <a class="item"><strong>题目导航</strong></a>
    {% for lproblem in problems_list %}
    <a class="{% if problem.id == lproblem.id %}active {% endif %}item"
        href="{% url 'contest.problem' contest.id lproblem.id %}"
    >题目{{ lproblem.index | problem_index }}</a>
    {% endfor %}
</div>
<div style="margin: 20px auto;">
    <h2>{% if contest.hide_problem_title %}题目{{ problem.index | problem_index }}{% else  %}{{ problem.index | problem_index }}. {{ problem_entity.title }}{% endif %}</h2>
</div>
<div id="MainContainer"></div>
<br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/codemirror/lib/codemirror.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/clike/clike.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/javascript/javascript.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/python/python.js"></script>
    <script type="text/javascript" src="/static/assets/highlight.pack.js"></script>
    <script type="text/javascript" src="/static/codemirror/addon/autorefresh.js"></script>
    <script type="text/javascript">
        $(function () {
            wejudge.problem.problembody.showProblemView(
                "MainContainer",
                {
                    problem:  "{% url 'api.contest.problem.body' contest.id problem_id %}",   // 读取题目内容和评测信息
                    judge: {
                        submit: "{% url 'api.contest.problem.judge.submit' contest.id problem_id %}",
                        rolling: "{% url 'api.contest.judge.status.rolling' contest.id 0 %}",
                        get_drafts: "{% url 'api.problem.code.drafts.get' problem_entity.id %}",
                        save_draft: "{% url 'api.problem.code.drafts.save' problem_entity.id %}"
                    },
                    history: {
                        list_status: "{% url 'api.contest.problem.judge.status.list' contest.id problem_id %}"
                    }
                },
                {
                    {% if wejudge_session.account.role >= 2 %}
                    manager: "{% url 'problem.manager.judge' 0 problem_entity.id %}",
                    {% endif %}
                    judge:{
                        view_detail: "{% url 'contest.judge.status.detail' contest.id 0 %}"
                    },
                    history: {
                        view_problem: "{% url 'contest.problem' contest.id 0 %}",
                        view_detail: "{% url 'contest.judge.status.detail' contest.id 0 %}"
                    }
                },
                {
                    statistics: false,
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
