{% extends "wejudge/component/base.tpl" %}
{% block page_navbar %}{% include "problem/entity/manager/navbar.tpl" %}{% endblock %}
{% block page_title %}题目集关联管理 - {{ problem_entity.title }} - {{ problemset.title }} - {% endblock %}
{% block page_head %}

{% endblock %}
{% block page_body %}
<div id="manager_container"></div>
<br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
        $(function () {
            wejudge.problem.problembody.showRelationManager(
                "manager_container",
                {
                    get_relations: "{% url 'api.problem.manager.relations' pset_id problem_id %}",
                    list_problemset: "{% url 'api.problem.set.list' %}",
                    publish_problem: "{% url 'api.problem.manager.relations.public' 0 problem_entity.id %}",
                    remove_problem: "{% url 'api.problem.manager.relations.remove' 0 problem_entity.id %}"
                },
                {}
            );
        });
    </script>
{% endblock %}