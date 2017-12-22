{% extends "wejudge/component/base.tpl" %}
{% load attr %}
{% block edu_navbar %}{% include 'wejudge/component/navbar.tpl' %}{% endblock %}
{% block page_title %}帮助中心 - {% endblock %}
{% block page_head %}
<style type="text/css">
    .content{
        line-height: 2rem;
    }
</style>
{% endblock %}
{% block page_body %}
<div class="ui secondary pointing menu">
    <a class="active item" data-tab="faq">常见问题F.A.Q</a>
    <a class="item" data-tab="utils">编程环境/工具</a>
</div>
<div class="ui active tab" data-tab="faq">
    {% include 'helper/module/faq.tpl' %}
</div>
<div class="ui tab" data-tab="utils">
    {% include 'helper/module/utils.tpl' %}
</div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        $('.menu .item').tab({
            history: true
        });
{#        $('.ui.sticky')#}
{#          .sticky({#}
{#            context: '#example1'#}
{#          })#}
{#        ;#}
    });
    </script>
{% endblock %}