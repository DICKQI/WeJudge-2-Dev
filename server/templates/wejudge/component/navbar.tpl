{% load nav_user_call %}
<!--Navigation-->
<div class="ui inverted stackable menu" style="border-radius: 0;">
    <div class="ui inverted stackable menu">
        <a class="item" href="/"><img class="ui" src="/static/images/logo_flat.png" width="104" height="24" alt=""></a>
        <a class="item{% if wejudge_const.apps.PROBLEM.0 == wejudge_navlist.0.0 %} active{% endif %}"
           href="{% url 'problem.index' %}">
        <i class="list items icon"></i>
        {{ wejudge_const.apps.PROBLEM.0 }}
        </a>
        <a class="item{% if wejudge_const.apps.EDUCATION.0 == wejudge_navlist.0.0 %} active{% endif %}"
            href="{% url 'education.index' %}" >
        <i class="student icon"></i>
        {{ wejudge_const.apps.EDUCATION.0 }}
        </a>
        <a class="item{% if wejudge_const.apps.CONTEST.0 == wejudge_navlist.0.0 %} active{% endif %}"
            href="{% url 'contest.index' %}"
        >
        <i class="trophy icon"></i>
        {{ wejudge_const.apps.CONTEST.0 }}
        </a>
        <a class="item{% if wejudge_const.apps.HELP.0 == wejudge_navlist.0.0 %} active{% endif %}"
            href="{% url 'helper.faq' %}"
        >
        <i class="help circle icon"></i>
        {{ wejudge_const.apps.HELP.0 }}
        </a>
        <a class="item" href="http://acm.bnuz.edu.cn" target="_blank">北师ACM协会</a>
    </div>
    {% include 'wejudge/component/navbar_user_block.tpl' %}
</div>