{% load nav_user_call %}
<div class="ui right inverted stackable menu">
    {% if not hide_login %}
        {% if not wejudge_session.logined %}
{#            <a class="item" onclick="wejudge.global.register('master')">#}
{#                <i class="child icon"></i>#}
{#                注册#}
{#            </a>#}
        <a class="item" onclick="wejudge.global.login('master')">
            <i class="sign in icon"></i>
            登录
        </a>
        {% else %}
            <div class="ui right dropdown item" id="AccountNavbtn">
                <i class="user icon"></i>
                {{ wejudge_session.account_manager | nav_user_call }} <i class="dropdown icon">
            </i>
                <div class="menu">
                    <a class="item" href="{% url 'account.space' wejudge_session.account.id %}"><i class="file text outline icon"></i> 个人中心</a>
                    <a class="item" href="{% url 'account.space' wejudge_session.account.id %}#settings"><i class="options icon"></i> 个人设置</a>
                    <div class="ui divider"></div>
                    <a class="item" onclick="wejudge.global.login('master')">
                        <i class="exchange icon"></i>
                        切换账户
                    </a>
                    <a class="item" onclick="wejudge.global.logout('master')"><i class="sign out icon"></i> 退出登录</a>
                </div>
            </div>
        {% endif %}
 {% endif %}
</div>