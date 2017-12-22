{% load nav_user_call %}
<div class="ui right inverted stackable menu">
    {% if not wejudge_session.logined %}
        {% if contest.register_mode != 'register' %}
        {% if not hide_login%}
        <a class="item" onclick="wejudge.global.login('contest')">
            <i class="sign in icon"></i>
            登录
        </a>
        {% endif %}
        {% endif %}
    {% else %}
        <div class="ui right dropdown item" id="AccountNavbtn">
            <i class="user icon"></i>
            {{ wejudge_session.account_manager | nav_user_call }} <i class="dropdown icon">
        </i>
            <div class="menu">
                <a class="item"><i class="file text outline icon"></i> 个人资料</a>
                <a class="item"><i class="options icon"></i> 个人设置</a>
                <div class="ui divider"></div>
                <a class="item" onclick="wejudge.global.login('contest')">
                    <i class="exchange icon"></i>
                    切换账户
                </a>
                <a class="item" onclick="wejudge.global.logout('contest', function() { window.location.href='{% url 'contest.contest' contest.id %}' });">
                    <i class="sign out icon"></i> 退出登录
                </a>
            </div>
        </div>
    {% endif %}
</div>