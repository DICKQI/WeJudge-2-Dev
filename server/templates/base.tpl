<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width,
          user-scalable=no,
          initial-scale=1.0,
          maximum-scale=1.0,
          minimum-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge,Chrome=1" />
    <meta name="description" content="{{ wejudge_config.web_desc }}" />
    <meta name="keywords" content="{{ wejudge_config.web_keyword }}" />
    <link rel="shortcut icon" href="/favicon.ico" />
    <link rel="bookmark" href="/favicon.ico" type="image/x-icon" />
    <!--[if lt IE 10]>
    <script type="text/javascript" src="/static/fuckie/fuckie.js"></script>
    <![endif]-->
    <link rel="stylesheet" href="/static/assets/semantic/semantic.min.css">
    <link rel="stylesheet" href="/static/assets/wejudge/app.css?build={{ wejudge_assets_hash }}">
    <title>{% block page_title %}{% endblock %}{{ wejudge_config.web_title }}</title>
    {% block page_head %}{% endblock %}
</head>
<body>
    {% block page_navbar %}{% endblock %}
    <div class="wj_page_container">
        {% if not hide_breadcrumb %}{% include "breadcrumb.tpl" %}{% endif %}
        {% block page_body %}{% endblock %}
    </div>
    {% block page_after_body %}{% endblock %}
    <div id="WeJudgeGlobalContainer">
        <div id="wj_global_login_container"></div>
        <div id="wj_global_register_container"></div>
        <div id="wj_global_account_card_container"></div>
    </div>
    <script type="text/javascript" src="/static/assets/wejudge/app.js?build={{ wejudge_assets_hash }}"></script>
    <script type="text/javascript">
        /*WeJudge Standard Script*/
        window.wejudge.global.account = {
            master: {
                "login_backend": "{% url 'api.account.login' %}",
                "logout_backend": "{% url 'api.account.logout' %}",
                "register_backend": "{% url 'api.account.register' %}",
                "my_account_info": "{% if wejudge_session.master_logined %}{% url 'api.account.space.info' wejudge_session.master.id %}{% endif %}",
                "account_info_api": "{% url 'api.account.space.info' 0 %}",
                "account_space_view": "{% url 'account.space' 0 %}",
                "account_space_avator": "{% url 'account.space.avator' 0 %}"
            }
        };

        $(function () {
            $("#AccountNavbtn,.NavDropdown").dropdown();
            window.wejudge.global.timer({{ wejudge_servertime }}, 'wejudge_server_timer');
        });

        try {
            var _czc = _czc || [];
            window._czc = _czc;
            _czc.push(["_setAccount", "1261763113"]);
        }catch(ex){}
    </script>
    {% block base_script %}{% endblock %}
    {% block page_script %}{% endblock %}
    <div id="footer">
        <div class="ui container">
            <div class="ui stackable two columns grid">
                <div class="column">
                    <div class="ui two columns grid">
                        <div class="column">
                            <h3>项目介绍</h3>
                            WeJudge是一个在线带代码判题系统，并用于辅助程序设计课程教学。
                        </div>
                        <div class="column">
                            <h3>联系我们</h3>
                            如有问题请发邮件到
                            webmaster#wejudge.net（你懂得)
                        </div>
                    </div>
                </div>
                <div class="right aligned column">
                    &copy; 2015-2017 wejudge.net Powered By WeJudgeStudio &nbsp;&nbsp;
                    <a href="https://github.com/LanceLRQ/wejudge" target="_blank">&lt;WeJudge1.0开源&gt;</a><br />
                    网站版本：<a href="#">Ver.{{ wejudge_config.web_version }}</a>&nbsp;&nbsp;
                    服务器时间：<span id="wejudge_server_timer"></span>
                    {% if not django_settings.DEBUG %}
                        <br />
                        <span id='cnzz_stat_icon_1261763113'></span>
                        <script src='//s95.cnzz.com/stat.php?id=1261763113&online=1&show=line' type='text/javascript'></script>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>