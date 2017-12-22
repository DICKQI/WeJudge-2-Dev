{% extends "wejudge/component/base.tpl" %}
{% block page_title %}题库系统 - {% endblock %}
{% block page_body %}
<div class="ui">
    <div class="ui stackable secondary pointing menu" id="MainNavList">
        <a class="active item" href="{% url 'problem.set.list' %}" data-tab="list">
            <i class="list layout icon"></i>
            题目集
        </a>
        {% if wejudge_session.logined and wejudge_session.account.permission_publish_problem %}
        <a class="item" data-tab="my_problem_list">
            <i class="browser icon"></i>
            我发布的题目
        </a>
        {% endif %}
        {% if wejudge_session.logined and wejudge_session.account.permission_create_problemset %}
        <a class="item" id="create_problemset">
            <i class="add icon"></i>
            创建题目集
        </a>
        {% endif %}
        {% if wejudge_session.logined and wejudge_session.account.permission_publish_problem %}
        <a class="item" href="{% url 'problem.set.create.problem.private' %}">
            <i class="send outline icon"></i>
            发布题目
        </a>
        {% endif %}
    </div>
    <div class="ui tab active" data-tab="list">
        <div id="problemset_container"></div>
    </div>
    {% if wejudge_session.logined and wejudge_session.account.permission_publish_problem %}
    <div class="ui tab" data-tab="my_problem_list">
        <div id="my_problem_list"></div>
    </div>
    {% endif %}
</div>
<!--不可见区域-->
<div id="problemset_editor"></div>
<br />
{% endblock %}
{% block page_script %}
<script type="text/javascript">
    $(function () {
        wejudge.beans.register('problemset_list', function () {
            return wejudge.problem.problemset.showProblemsetList(
                "problemset_container",
                {
                    list_problemset: "{% url 'api.problem.set.list' %}",
                    editor: {
                        create: "{% url "api.manager.problem.set.create" %}",
                        modify: "{% url "api.manager.problem.set.modify" 0 %}",
                        data: "{% url "api.problem.set.info" 0 %}",
                        upload_image: "{% url "api.manager.problem.set.image.upload" 0 %}"
                    }
                },
                {
                    view_problemset: "{% url 'problem.set.view' 0 %}"
                },
                {
                    readonly: false
                }
            );
        });
        {% if wejudge_session.logined  and wejudge_session.account.permission_publish_problem%}
        wejudge.beans.register('my_problem_list', function () {
            return wejudge.problem.problemset.showProblemsList(
                "my_problem_list",
                {
                    list_problem: "{% url 'api.problem.mine.problems.list' %}"
                },
                {
                    view_problem: "{% url 'problem.view' 0 0 %}"
                },
                {
                    hide_ratio: true,
                    hide_filter: true,
                    show_manage: false,
                    hide_classify: true
                }
            );
        });
        {% endif %}
        $("#create_problemset").click(function () {
            wejudge.beans.getBean('problemset_list').createProblemSet();
        });
        $("#MainNavList > .item").tab({
            history: true,
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if (tab_name == 'list'){
                    wejudge.beans.getBean('problemset_list').load()
                }
                {% if wejudge_session.logined and wejudge_session.account.permission_publish_problem%}
                else if(tab_name == 'my_problem_list'){
                    wejudge.beans.getBean('my_problem_list').load()
                }
                {% endif %}
            }
        });
    });
</script>
{% endblock %}