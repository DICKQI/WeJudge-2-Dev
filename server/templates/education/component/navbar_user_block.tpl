{% load nav_user_call %}
<div class="ui right inverted stackable menu">
    {% if not wejudge_session.logined %}
        {% if not hide_login %}
        <a class="item" onclick="wejudge.global.login('education')">
            <i class="sign in icon"></i>
            登录
        </a>
        {% endif %}
    {% else %}
        <div class="ui right dropdown item" id="AccountNavbtn">
            <i class="user icon"></i>
            {{ wejudge_session.account_manager | nav_user_call }} <i class="dropdown icon">
            </i>
            <div class="menu">
                <a class="item" href="{% url 'account.education.space' school.id wejudge_session.account.id %}"><i class="file text outline icon"></i> 个人中心</a>
                <a class="item" href="{% url 'account.education.space' school.id wejudge_session.account.id %}#settings"><i class="options icon"></i> 个人设置</a>
                <div class="ui divider"></div>
                <a class="item" onclick="wejudge.global.login('education')">
                    <i class="exchange icon"></i>
                    切换账户
                </a>
                <a class="item" onclick="wejudge.global.logout('education', function() { window.location.href='{% url 'education.school' school.id %}' });">
                    <i class="sign out icon"></i> 退出登录
                </a>
            </div>
        </div>
    {% endif %}
</div>