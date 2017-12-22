{% extends "wejudge/component/base.tpl" %}
{% block page_navbar %}{% include "problem/entity/manager/navbar.tpl" %}{% endblock %}
{% block page_title %}评测设置管理 - {{ problem_entity.title }} - {{ problemset.title }} - {% endblock %}
{% block page_head %}
<link rel="stylesheet" href="/static/codemirror/lib/codemirror.css">
<style type="text/css">
.CodeMirror {
    border: 1px solid #eee;
    height: 400px;
}
.ui.list > li{
    line-height: 2.5em !important;
}
</style>
{% endblock %}
{% block page_body %}
<div id="manager_container"></div>
<br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/codemirror/lib/codemirror.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/clike/clike.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/javascript/javascript.js"></script>
    <script type="text/javascript" src="/static/codemirror/mode/python/python.js"></script>
    <script type="text/javascript" src="/static/codemirror/addon/autorefresh.js"></script>
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    <script type="text/javascript">
        $(function () {
            wejudge.problem.problembody.showJudgeManager(
                "manager_container",
                {
                    "judge_config": "{% url 'api.problem.manager.get.judge.config' pset_id problem_id %}",
                    "save_judge_config": "{% url 'api.problem.manager.save.judge.config' pset_id problem_id %}",
                    "toggle_judge": "{% url 'api.problem.manager.judge.toggle' pset_id problem_id %}",
                    "save_answer_case": "{% url 'api.problem.manager.answer.save' pset_id problem_id %}",
                    "save_test_cases_settings": "{% url 'api.problem.manager.test.cases.save'  pset_id problem_id %}",
                    "remove_test_cases": "{% url 'api.problem.manager.test.cases.remove'  pset_id problem_id %}",
                    "get_test_cases_data": "{% url 'api.problem.manager.test.cases.data' pset_id problem_id  %}",
                    "save_test_cases_data": "{% url 'api.problem.manager.test.cases.data.save' pset_id problem_id  %}",
                    "upload_test_cases_data":{
                        "in": '{% url 'api.problem.manager.test.cases.data.upload' pset_id problem_id 'in' %}',
                        "out": '{% url 'api.problem.manager.test.cases.data.upload' pset_id problem_id 'out' %}'
                    },
                    "upload_spj_judger": "{% url 'api.problem.manager.special.judger.save' pset_id problem_id  %}",
                    "save_demo_cases_settings": "{% url 'api.problem.manager.demo.case.save' pset_id problem_id  %}",
                    "save_demo_cases_code": "{% url 'api.problem.manager.demo.case.code.save' pset_id problem_id  %}",
                    "remove_demo_cases": "{% url 'api.problem.manager.demo.case.remove' pset_id problem_id  %}",
                    "modify_problem": "{% url 'api.problem.manager.modify' pset_id problem_id %}",
                    "problem_info": "{% url 'api.problem.view.body' pset_id problem_id %}",
                    "tcmaker_run": "{% url 'api.problem.manager.test.cases.maker.run' pset_id problem_id %}",
                    "tcmaker_hisotory": "{% url 'api.problem.manager.test.cases.maker.history' pset_id problem_id %}"
                },
                {},
                {
                    "is_onwer": {% if wejudge_session.logined and wejudge_session.account == problem_entity.author %}true{% else %}false{% endif %},
                    "problem_type": {{ problem_entity.problem_type }}
                }
            )
        });
    </script>
{% endblock %}