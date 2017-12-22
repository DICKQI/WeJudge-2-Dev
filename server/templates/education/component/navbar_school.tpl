<!--Navigation-->
<div class="ui inverted stackable menu" style="border-radius: 0;">
    <div class="ui inverted stackable menu">
        <div class="ui right dropdown item NavDropdown">
            <img class="ui" src="/static/images/logo_flat_edu.png" height="24" alt="">
            {% include "wejudge/component/nav_logo.tpl" %}
        </div>
        <a class="{% if page_name == "INDEX" %}active {% endif %}item" href="{% url 'education.school' school.id %}">
            <i class="student icon"></i>
            学校首页
        </a>
        <a class="{% if page_name == "REPOSITORY" %}active {% endif %}item" href="{% url 'education.school.repository' school.id %}">
            <i class="share alternate icon"></i>
            教学资源
        </a>
        <a href="{% url 'problem.set.list' %}" class="item">
            <i class="list items icon"></i>
            题目中心
        </a>
        <a class="item" href="{% url 'helper.faq' %}" target="_blank">
            <i class="help circle outline icon"></i>{{ wejudge_const.apps.HELP.0 }}
        </a>
        {% if wejudge_session.account.role >= 3 %}
        <a class="{% if page_name == "MANAGER" %}active {% endif %}item" href="{% url 'education.school.management' school.id %}">
            <i class="setting yellow icon"></i>
            学校管理
        </a>
        {% endif %}


    </div>
    {% include 'education/component/navbar_user_block.tpl' %}
</div>