{% extends "wejudge/component/base.tpl" %}
{% block page_title %}题目列表 - {{ problemset.title }} - {% endblock %}
{% block page_head %}
    <link rel="stylesheet" href="/static/assets/jstree/themes/default/style.min.css">
{% endblock %}
{% block page_body %}
<div class="ui">
    <div class="ui secondary pointing menu" id="MainNavList">
        <a class="active item" data-tab="problems">
            <i class="list layout icon"></i>
            题目列表
        </a>
        <a class="item" data-tab="status">
            <i class="wait icon"></i>
            评测历史
        </a>
        {% if problemset_management %}
        <a class="item" data-tab="classify">
            <i class="sitemap icon"></i>
            分类管理
        </a>
        <a class="item" href="{% url 'problem.set.create.problem' pset_id %}">
            <i class="send outline icon"></i>
            发布题目到此题库
        </a>
        {% endif %}
    </div>
    <div class="ui tab active" data-tab="problems">
        <div id="problems_list_container"></div>
    </div>
    <div class="ui tab" data-tab="status">
        <div id="status_list_container"></div>
    </div>
    <div class="ui tab" data-tab="classify">
        <div id="classify_mgr_container"></div>
    </div>
</div>
<br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/assets/jstree/jstree.min.js"></script>
    <script type="text/javascript">
        $(function () {
            var CreatingProblemLoaded = false;
            wejudge.beans.register('problems_list', function () {
                return wejudge.problem.problemset.showProblemsList(
                    "problems_list_container",
                    {
                        list_problemset: "{% url 'api.problem.set.list' %}",
                        list_problem: "{% url 'api.problem.set.problems.list' pset_id %}",
                        remove_problem: "{% url 'api.manager.problem.set.remove.problem' pset_id 0 %}",
                        classify: {
                            get_data: "{% url 'api.problemset.classification.data.wejudge' pset_id %}"
                        },
                        jstree: {
                            get_data: "{% url 'api.problemset.classification.data' pset_id %}"
                        },
                        problem_moveto_classify: "{% url 'api.problemset.classification.problems.moveto' pset_id 0 %}",
                        problem_moveto_problemset: "{% url 'api.problemset.problems.moveto' pset_id %}",
                        problem_removefrom_problemset: "{% url 'api.problemset.problems.remove' pset_id %}"
                    },
                    {
                        view_problem: "{% url 'problem.view' pset_id 0 %}"
                    },
                    {
                        hide_ratio: false,
                        hide_filter: false,
                        show_manage: {% if problemset_management %}true{% else %}false{% endif %}
                    }
                );
            });
            wejudge.beans.register('status_list', function () {
                return wejudge.problem.judgestatus.showStatusList(
                    "status_list_container",
                    {
                        list_status: "{% url 'api.problemset.judge.status.list' pset_id %}"
                    },
                    {
                        view_problem: "{% url 'problem.view' pset_id 0 %}",
                        view_detail: "{% url 'problem.judge.status' 0 %}"
                    },
                    {
                        realname:false,
                        full: true
                    }
                );
            });
            wejudge.beans.register('classify_mgr', function () {
                return wejudge.problem.problemset.showClassifyManager(
                    "classify_mgr_container",
                    {
                        change_classify: "{% url 'api.problemset.classification.change' pset_id 0 %}",
                        jstree: {
                            get_data: "{% url 'api.problemset.classification.data' pset_id %}"
                        }
                    },
                    {}
                );
            });
            $("#MainNavList>.item").tab({
                history: true,
                onLoad: function () {
                    var tab_name = $(this).attr("data-tab");

                    if(tab_name == 'problems'){
                        wejudge.beans.getBean('problems_list').load()
                    }else if(tab_name == "status"){
                        wejudge.beans.getBean('status_list').load()
                    }else if(tab_name == 'classify'){
                        wejudge.beans.getBean('classify_mgr').init()
                    }
                }
            });

        });
    </script>
{% endblock %}