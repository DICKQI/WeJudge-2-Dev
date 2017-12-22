{% extends "wejudge/component/base.tpl" %}
{% block page_title %}发布题目 - {% endblock %}
{% block page_head %}
    <link rel="stylesheet" href="/static/assets/jstree/themes/default/style.min.css">
{% endblock %}
{% block page_body %}
    <div class="ui icon message" style="">
        <i class="info circle icon"></i>
        <div class="content">
            {% if problemset is not None %}
            <p>当前新建的题目将被自动推送到题目集【{{ problemset.title }}】中，您可以自由解除其关联或者将其添加到别的题目集中。</p>
            {% else %}
            <p>当前新建的题目将储存在“我发布的题目”，后续您可以将其添加到题目集中。</p>
            {% endif %}
        </div>
    </div>
    <div id="problem_editor"></div>
    <br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    <script type="text/javascript">
        $(function () {
           wejudge.problem.problembody.showProblemEditor(
                "problem_editor",
                {
                    create: "{% url 'api.problem.manager.create' pset_id %}"
                },
                {
                    view_problem_manager: "{% url 'problem.manager.judge' 0 0 %}"
                }
            ).createProblem();
        });
    </script>
{% endblock %}