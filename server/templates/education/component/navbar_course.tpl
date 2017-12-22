<!--Navigation-->
<div class="ui inverted stackable menu" style="border-radius: 0;">
    <div class="ui inverted stackable menu">
        <div class="ui right dropdown item NavDropdown">
            <img class="ui" src="/static/images/logo_flat_edu.png" height="24" alt="">
            {% include "wejudge/component/nav_logo.tpl" %}
        </div>
        <a class="{% if page_name == "INDEX" %}active {% endif %}item" href="{% url 'education.course.index' school.id course.id %}">
            <i class="book icon"></i>
            课程首页
        </a>
        <a class="{% if page_name == "REPOSITORY" %}active {% endif %}item" href="{% url 'education.course.repository' school.id course.id %}">
            <i class="share alternate icon"></i>
            教学资源
        </a>
        {% if wejudge_session.account.role >= 2 %}
        <a class="{% if page_name == "ARRANGEMENTS" %}active {% endif %}item" href="{% url 'education.course.arrangements' school.id course.id %}">
            <i class="tasks yellow icon"></i>
            排课管理
        </a>
        <a class="{% if page_name == "SETTINGS" %}active {% endif %}item" href="{% url 'education.course.settings' school.id course.id %}">
            <i class="settings yellow icon"></i>
            课程设置
        </a>
        <a class="item" href="" >
            <i class="bar chart blue icon"></i>
            统计与归档(开发中)
        </a>
        {% endif %}

    </div>
    {% include 'education/component/navbar_user_block.tpl' %}
</div>