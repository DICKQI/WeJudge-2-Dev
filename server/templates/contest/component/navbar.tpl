<!--Navigation-->
<div class="ui inverted stackable menu" style="border-radius: 0;">
    <div class="ui inverted stackable menu" id="MainNavList">
        <div class="ui right dropdown item NavDropdown">
             <img class="ui" src="/static/images/logo_flat_contest.png" height="24" alt="">
            {% include "wejudge/component/nav_logo.tpl" %}
        </div>
        {% if page_name == "INDEX" %}
            <a class="active item" data-tab="home">
                <i class="home icon"></i>
                比赛
            </a>
            {% if wejudge_session.logined %}
                <a class="item" data-tab="problems">
                    <i class="list layout icon"></i>
                    题目
                </a>
                <a class="item" data-tab="status">
                    <i class="history icon"></i>
                    评测
                </a>
            {% endif %}
            <a class="item" data-tab="ranklist">
                <i class="signal icon"></i>
                排行
            </a>
            {% if wejudge_session.logined %}
                <a class="item" data-tab="faq">
                    <i class="help circle icon"></i>
                    问答
                </a>
                {% if wejudge_session.account.role >= 1 or contest.cross_check_public %}
                    <a class="item" data-tab="cross_check">
                        <i class="object group icon"></i>
                        查重
                    </a>
                {% endif %}
                {% if contest.enable_printer_queue %}
                    <a class="item" data-tab="printer_queue">
                        <i class="print icon"></i>
                        打印资料
                    </a>
                {% endif %}
            {% endif %}
        {% else %}
        <a class="item" href="{% url 'contest.contest' contest.id %}">
            <i class="home icon"></i>
            比赛
        </a>
        {% endif %}{# INDEX #}
        {% if wejudge_session.logined and wejudge_session.account.role == 2 %}
            {% if page_name == "MANAGE" %}
                <a class="active item" data-tab="settings">
                    <i class="settings icon"></i>
                    比赛设置
                </a>
                <a class="item" data-tab="accounts">
                    <i class="users icon"></i>
                    账户管理
                </a>
                <a class="item" data-tab="choose_problem">
                    <i class="list icon"></i>
                    题目选择
                </a>
            {% else %}
                <a class="item" href="{% url 'contest.management' contest.id %}">
                    <i class="dashboard icon"></i>
                    控制面板
                </a>
            {% endif %}
        {% endif %}
    </div>
    {% include 'contest/component/navbar_user_block.tpl' %}
</div>