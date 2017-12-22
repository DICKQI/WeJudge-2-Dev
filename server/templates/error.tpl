{% extends "wejudge/component/base.tpl" %}
{% load errpage_randimg %}
{% block page_title %}您的操作遇到了一些问题 - {% endblock %}
{% block page_body %}
{#    <div class="ui container">#}
{#        <div class="ui steps" style="width: 100%;">#}
{#            <div class="step">#}
{#                <img src="{{ '' | errpage_randimg }}" height="200">#}
{#            </div>#}
{#            <div class="step">#}
{#                #}
{#            </div>#}
{#        </div>#}
{#    </div>#}
    <div class="ui container" align="center">
        <div class="ui segment">
            <div class="title"><h2>您的操作遇到了一些问题</h2></div><br />
            <div class="description">
                <h2 style="color:red">{{ errmsg }}</h2><br/>
                <div style=" width:90%; color: #ccc">
                    <strong>错误代码：</strong>{{ errcode }}<br/><br/>
                    <strong>UserAgent：</strong>{{ USER_AGENT }}
                </div>
            </div>
            <br /><br />
            {% if errcode == 1010 %}
                <a class="ui fluid basic green button" href="/">返回首页</a>
            {% elif errcode == 3010 %}
                <a class="ui fluid basic green button" href="{% url 'education.index' %}">返回教学系统首页</a>
            {% elif  errcode == 5010  %}
                <a class="ui fluid basic green button" href="{% url 'contest.index' %}">返回比赛系统首页</a>
            {% else %}
                <a class="ui fluid basic green button" href="{{ HTTP_REFERER }}">返回上一个页面</a>
            {% endif %}
        </div>
    </div>
{#<div class="ui centered card">#}
{#    <div class="image">#}
{#      <img src="{{ '' | errpage_randimg }}">#}
{#    </div>#}
{#    <div class="content">#}
{#        <div class="header">您的操作遇到了一些问题 </div>#}
{#        <div class="meta"> </div>#}
{#        <div class="description"></div>#}
{#    </div>#}
{#    <div class="extra content">#}

{#    </div>#}
{#</div>#}

{% endblock %}
{#{% block page_script %}#}
{#    <script type="text/javascript">#}
{#    $(function () {#}
{#        $('#errimg')#}
{#          .popup({#}
{#            popup: $('#errcnt')#}
{#          })#}
{#        ;#}
{#    });#}
{#    </script>#}
{#{% endblock %}#}