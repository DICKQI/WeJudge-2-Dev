{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_school.tpl' %}{% endblock %}
{% load attr %}
{% block page_title %}授权登录 - {{ school.name }} - {% endblock %}
{% block page_body %}

    <div class="ui black segment" style="width: 480px; margin:0 auto; text-align: center;">
        <h2>使用WeJudge教学账号授权此应用</h2>
        <div class="ui divider"></div>
        <div class="ui three columns grid">
            <div class="column" align="center">
                <img class="ui centered aligned tiny circular image" src="{% if wejudge_session.is_logined %}{% url 'education.account.space.avator' school.id wejudge_session.account.id %}{% else %}{% url 'education.account.space.avator' school.id 0 %}{% endif %}">
            </div>
            <div class="column" align="center">
                 <img src="/static/images/connect.png"  class="ui centered aligned tiny image">
            </div>
            <div class="column" align="center">
                <img src="{{ client.avatar }}" class="ui centered aligned tiny image">
            </div>
        </div>
        <div class="ui three columns grid">
            <div class="column" align="center">
                {% if wejudge_session.is_logined %}
                    {{ wejudge_session.account.nickname }}
                {% else %}
                    <a href="javascript:void(0)" onclick="wejudge.global.login('education')">请登录</a>
                {% endif %}
            </div>
            <div class="column" align="center">
                <i class="arrow right icon"></i>
            </div>
            <div class="column" align="center">
                {{ client.appname }}
            </div>
        </div>
        <div class="ui divider"></div>
        <div align="left">
            <h4>您的操作将会授权此应用获取以下信息</h4>
            <ul class="ui bulleted list">
                <li>账号基本信息</li>
                <li>账号详细资料</li>
                <li>以此账号身份使用所有系统功能（暂未开放）</li>
            </ul>
        </div>
        <div class="ui divider"></div>
        <form action="?{{ urlcall }}" method="post" id="FormAuth">
            <div class="ui fluid buttons">
                {% if wejudge_session.is_logined %}
                    <input type="hidden" id="ConfirmCheckBox" name="confirm" value="1">
                    <button class="ui green button">确认授权</button>
                    <button type="button" class="ui button" onclick="cancle_auth()">拒绝授权</button>
                {% else %}
                    <a class="ui disabled green button">确认授权</a>
                    <a class="ui disabled button">拒绝授权</a>
                {% endif %}
            </div>
        </form>
    </div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        {% if not wejudge_session.is_logined %}
            wejudge.global.login('education');
        {% endif %}
    });
    function cancle_auth(){
        document.getElementById('ConfirmCheckBox').value=0;
        document.getElementById('FormAuth').submit()
    }
    </script>
{% endblock %}