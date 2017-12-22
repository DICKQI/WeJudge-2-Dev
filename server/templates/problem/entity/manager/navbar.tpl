{% load nav_user_call %}
<!--Navigation-->
<div class="ui inverted stackable menu" style="border-radius: 0;">
    <div class="ui inverted stackable menu">
        <a class="item" href="/"><img class="ui" src="/static/images/logo_flat.png" width="104" height="24" alt=""></a>
{#        <a class="item"#}
{#           href="{% url 'problem.view' pset_id problem_id %}">#}
{#            <i class="reply icon"></i>#}
{#            查看题目#}
{#        </a>#}
        <a class="{% if page_name == "JUDGE" %}active {% endif %}item"
            href="{% url 'problem.manager.judge' pset_id problem_id  %}" >
            <i class="settings icon"></i>
            评测设置
        </a>
        <a class="{% if page_name == "PROBLEMSET" %}active {% endif %}item"
            href="{% url 'problem.manager.problemset.relation' 0 problem_entity.id %}">
            <i class="list layout icon"></i>
            题集关联
        </a>
        <a class="{% if page_name == "DELETE" %}active {% endif %}item">
            <i class="remove icon"></i>
            删除题目
        </a>
    </div>
    {% include 'wejudge/component/navbar_user_block.tpl' %}
</div>