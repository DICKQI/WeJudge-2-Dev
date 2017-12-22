{% extends "education/component/base.tpl" %}
{% load nav_user_call %}
{% block edu_navbar %}{% include "education/component/navbar_asgn.tpl" %}{% endblock %}
{% block page_title %}统计与分析 - {{ asgn.title }} - {{ school.name }} - {% endblock %}
{% block page_head %}
    <script type="text/javascript" src="/static/echars/echarts.common.min.js"></script>
{% endblock %}
{% block page_body %}
    <div class="ui stackable secondary pointing menu" id="NavList">
        <a class="active item" data-tab="package"><i class="download icon"></i> 打包/下载</a>
        <a class="item" data-tab="statistic"><i class="line chart icon"></i> 数据分析</a>
    </div>
    <div class="ui tab active" data-tab="package">

    </div>
    <div class="ui tab" data-tab="statistic">
        <div id="asgn_statistic"></div>
    </div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.beans.register('asgn_statistic', function(){
            return wejudge.education.statistic.showAsgnStatistic(
                "asgn_statistic",
                {
                    data: "{% url 'api.education.asgn.statistic.raw.datas' school.id asgn.id %}"
                }
            )
        });

        $("#NavList>.item").tab({
            history: true,
            cache: false,
            alwaysRefresh: true,
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if(tab_name === "statistic"){
                    wejudge.beans.getBean('asgn_statistic').load();
                }
            }
        });
    });
    </script>
{% endblock %}