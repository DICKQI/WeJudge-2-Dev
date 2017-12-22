{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include "education/component/navbar_asgn.tpl" %}{% endblock %}
{% block page_title %}作业管理：{{ asgn.title }} - {{ school.name }} - {% endblock %}
{% block page_head %}
    <style type="text/css">
    img {
        max-width: 100%;
    }
    a.step:hover{
            text-decoration: none !important;
    }
    </style>
{% endblock %}
{% block page_body %}
    <div class="ui stackable secondary pointing menu" id="NavList">
        <a class="active item" data-tab="checkup"><i class="checkmark box icon"></i> 作业批改</a>
        {% if wejudge_session.account.role >= 2 %}
        <a class="item" data-tab="problems"><i class="list items icon"></i> 作业题目</a>
        <a class="item" data-tab="settings"><i class="settings icon"></i> 作业设置</a>
        <a class="item" data-tab="visit_require"><i class="area chart icon"></i> 调课管理</a>
        <a class="item" data-tab="delete"><i class="remove circle icon"></i> 删除作业</a>
        {% endif %}
    </div>
    <div class="ui active tab" data-tab="checkup">
        <div id="checkup_container"></div>
    </div>
    <div class="ui tab" data-tab="problems">
        <div id="problems_list_container"></div>
        <div class="ui horizontal divider"><i class="add icon"></i>选择作业题目</div>
        <div id="problem_choosing_container"></div>
    </div>
    <div class="ui tab" data-tab="settings">
        <div id="settings_container"></div>
    </div>
    <div class="ui tab" data-tab="visit_require">
        <div id="visit_require_container"></div>
    </div>
    <div class="ui tab" data-tab="delete">
        <div id="delete_container">
            <form action="{% url 'api.education.delete.asgn' school.id asgn.id %}" method="post">
                <div class="ui large icon message">
                    <i class="warning circle  icon"></i>
                    <div class="content">
                        <strong>警告：</strong>您应该很清楚您的操作即将带来的后果。
                        <ol>
                            <li>作业信息将会被永久删除，无法恢复。</li>
                            <li>所有与该作业关联的做题信息、实验报告、批改信息等都将要被删除。</li>
                            <li>题目、评测记录、运行数据等存放于服务器文件系统的内容将不会被删除。</li>
                            <li>当前操作仅能由管理员或作业发布者执行。</li>
                        </ol>
                        <label><input type="checkbox" name="agree" value="true">&nbsp;我愿意承担此操作带来的风险</label>
                        <div class="ui divider"></div>
                        <button type="submit" class="ui red button">删除作业</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
    <br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    <script type="text/javascript">
    $(function () {
        var is_teacher = false;
        {% if wejudge_session.account.role >= 2 %}
            is_teacher = true;
        {% endif %}
        wejudge.beans.register('problems_list', function(){
            return wejudge.education.asgn.showAsgnProblemsList(
                "problems_list_container",
                {
                    problems_list: "{% url 'api.education.asgn.problems' school.id asgn.id %}",
                    save_problem_setting: "{% url 'api.education.asgn.problem.settings.save' school.id asgn.id 0 %}",
                    remove_problem: "{% url 'api.education.asgn.problem.remove' school.id asgn.id 0 %}",
                    rejudge_problem: "{% url 'api.education.asgn.problem.rejudge' school.id asgn.id 0 %}",
{#                    {% if wejudge_session.account.role >= 2 %}#}
{#                    problem_choosing:{#}
{#                        problemset:{#}
{#                            list_problemset: "{% url 'api.problem.set.list' %}",#}
{#                            list_problem: "{% url 'api.problem.set.problems.list' 0 %}"#}
{#                        },#}
{#                        jstree: {#}
{#                            get_data: "{% url 'api.problemset.classification.data' 0 %}"#}
{#                        },#}
{#                        save_choosing: "{% url 'api.education.asgn.problems.choosing.save' school.id asgn.id %}",#}
{#                        highlight_items: "{% url 'api.education.asgn.problems.choosing.history' school.id asgn.id %}"#}
{#                    }#}
{#                    {% endif %}#}
                },
                {
                    problem_view: "{% url 'education.asgn.problem.view' school.id asgn.id 0 %}",
                    problem_manager: "{% url 'problem.manager.judge' 0 0 %}",
{#                    {% if wejudge_session.account.role >= 2 %}#}
{#                    problem_choosing:{#}
{#                        view_problem: "{% url 'problem.view' 0 0 %}"#}
{#                    }#}
{#                    {% endif %}#}
                },
                {% if wejudge_session.account.role >= 2 %}true{% else %}false{% endif %}
            );
        });
        wejudge.beans.register('problem_choosing', function(){
            return wejudge.problem.problemset.showProblemChoosing(
                "problem_choosing_container",
                {
                    problemset:{
                        list_problemset: "{% url 'api.problem.set.list' %}",
                        list_problem: "{% url 'api.problem.set.problems.list' 0 %}"
                    },
                    classify: {
                        get_data: "{% url 'api.problemset.classification.data.wejudge' 0 %}"
                    },
                    jstree: {
                        get_data: "{% url 'api.problemset.classification.data' 0 %}"
                    },
                    save_choosing: "{% url 'api.education.asgn.problems.choosing.save' school.id asgn.id %}",
                    highlight_items: "{% url 'api.education.asgn.problems.choosing.history' school.id asgn.id %}"
                },
                {
                    view_problem: "{% url 'problem.view' 0 0 %}"
                }
            );
        });
        wejudge.beans.register('asgn_checkup', function(){
            return wejudge.education.asgn.showAsgnReportsList(
                "checkup_container",
                {
                    reports_list: "{% url 'api.education.asgn.report.list' school.id asgn.id %}",
                    get_report: "{% url 'api.education.asgn.report' school.id asgn.id 0 %}",
                    save_checkup: "{% url 'api.education.asgn.report.checkup.save' school.id asgn.id 0 %}",
                    save_batch_checkup: "{% url 'api.education.asgn.report.batch.checkup.save' school.id asgn.id %}",
                    refresh_datas: "{% url 'api.education.asgn.refresh.datas' school.id asgn.id %}"
                },
                {
                    view_report: "{% url "education.asgn.report" school.id asgn.id 0 %}"
                }
            );
        });
        {% if wejudge_session.account.role >= 2 %}
        wejudge.beans.register('asgn_settings', function(){
            return wejudge.education.asgn.showAsgnSettings(
                "settings_container",
                {
                    asgn_settings: "{% url 'api.education.asgn.settings' school.id asgn.id %}",
                    save_settings: "{% url 'api.education.asgn.settings.save' school.id asgn.id %}"
                },
                {}
            );
        });
        wejudge.beans.register('visit_require', function(){
            return wejudge.education.asgn.showAsgnVisitRequirement(
                "visit_require_container",
                {
                    data: "{% url 'api.education.asgn.visit.requirement' school.id asgn.id %}",
                    add_new: "{% url 'api.education.asgn.visit.requirement.add' school.id asgn.id %}",
                    remove: "{% url 'api.education.asgn.visit.requirement.delete' school.id asgn.id %}",
                    search_student: "{% url 'api.education.search.student' school.id %}"
                },
                {},
                {
                    arrangements: eval('({{ arrangements | safe }})')
                }
            );
        });
        {% endif %}
        $("#NavList>.item").tab({
            history: true,
            cache: false,
            alwaysRefresh: true,
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if(tab_name == "checkup") {
                    wejudge.beans.getBean('asgn_checkup').load();
                }else if(tab_name == "problems"){
                    wejudge.beans.getBean('problems_list').load();
                    wejudge.beans.getBean('problem_choosing').init();
                }
                {% if wejudge_session.account.role >= 2 %}
                else if(tab_name == "settings"){
                    wejudge.beans.getBean('asgn_settings').load();
                } else if(tab_name == "visit_require"){
                    wejudge.beans.getBean('visit_require').load();
                }
                {% endif %}
            }
        });
    });
    </script>
{% endblock %}