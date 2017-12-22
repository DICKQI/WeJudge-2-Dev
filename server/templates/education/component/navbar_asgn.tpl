<!--Navigation-->
<div class="ui inverted stackable menu" style="border-radius: 0;">
    <div class="ui inverted stackable menu" id="NavList">
        <div class="ui right dropdown item NavDropdown">
            <img class="ui" src="/static/images/logo_flat_edu.png" height="24" alt="">
            {% include "wejudge/component/nav_logo.tpl" %}
        </div>
        {% if page_name == "INDEX" %}
        <a class="active item" data-tab="problems"><i class="puzzle icon"></i> 作业内容</a>
        <a class="item" data-tab="status"><i class="history icon"></i> 评测历史</a>
        <a class="item" data-tab="answer"><i class="code icon"></i> 参考答案</a>
        <a class="item" data-tab="ranklist"><i class="signal icon"></i> 排行榜</a>
        {% else %}
        <a class="{% if page_name == 'PROBLEM' %}active {% endif %}item" href="{% url 'education.asgn.index' school.id asgn.id %}">
            <i class="puzzle icon"></i>
            作业内容
        </a>
        <a class="item" href="{% url 'education.asgn.index' school.id asgn.id %}#/status">
            <i class="history icon"></i> 评测历史
        </a>
        <a class="item" href="{% url 'education.asgn.index' school.id asgn.id %}#/answer">
            <i class="code icon"></i> 参考答案
        </a>
        <a class="item" href="{% url 'education.asgn.index' school.id asgn.id %}#/ranklist">
            <i class="signal icon"></i> 排行榜
        </a>
        {% endif %}
        {% if wejudge_session.account.role == 0 %}
        <a class="{% if page_name == "REPORT" %}active {% endif %}item" href="{% url "education.asgn.report" school.id asgn.id asgn_report.id %}"><i class="sticky note icon"></i> 实验报告</a>
        {% endif %}
        {% if wejudge_session.account.role > 0 %}
        <a class="{% if page_name == "MANAGER" or page_name == "REPORT" and wejudge_session.account.role >= 1 %}active {% endif %}item" href="{% url 'education.asgn.manager' school.id asgn.id %}">
            <i class="yellow checked calendar icon"></i>
            批改与管理
        </a>
        <a class="{% if page_name == "STATISTIC" or page_name == "STATISTIC" and wejudge_session.account.role >= 1 %}active {% endif %}item" href="{% url 'education.asgn.statistic' school.id asgn.id %}">
            <i class="blue line chart icon"></i>
            统计与报告
        </a>
        {% endif %}
    </div>
    {% include 'education/component/navbar_user_block.tpl' %}
</div>