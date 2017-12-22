{% extends "wejudge/component/base.tpl" %}
{% block page_navbar %}{% include "problem/entity/manager/navbar.tpl" %}{% endblock %}
{% block page_title %}编辑题目内容 - {{ problem_entity.title }} - {{ problemset.title }} - {% endblock %}
{% block page_head %}

{% endblock %}
{% block page_body %}
<div id="manager_container"></div>
<br />
{% endblock %}
{% block page_script %}

    <script type="text/javascript">
        $(function () {
            wejudge.problem.problembody.showProblemEditor(
                "manager_container",
                {
                    modify: "{% url 'api.problem.manager.modify' pset_id problem_id %}",
                    problem_info: "{% url 'api.problem.view.body' pset_id problem_id %}"
                },
                {}
            ).modifyProblem();
        });
    </script>
{% endblock %}