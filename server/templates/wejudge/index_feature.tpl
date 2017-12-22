{% extends "wejudge/component/base.tpl" %}
{% block base_script %}<script src="/static/assets/app_index/prefixfree.min.js"></script>{% endblock %}
{% block page_head %}
<style type="text/css">
    .wj_page_container{
        width: 100% !important;
        margin-bottom: 0;
    }
    .ui.menu{
        margin: 0 !important;
    }

</style>
<link rel="stylesheet" href="/static/assets/app_index/index.css">
{% endblock %}
{% block page_body %}
    <div id="bg_container"></div>
    <div class="x-mark" id="close-mark">
        <div class="container">
            <div class="left"></div>
            <div class="right"></div>
        </div>
    </div>

    <div class="main_container">
        <div class="intro-container">
            <img src="/static/images/logo_flat.png" height="80">
            <h1 class="main_title">在线代码评测教学辅助系统</h1>

            <div class="start_button shift-camera-button">
                <div class="border">
                    <div class="left-plane"></div>
                    <div class="right-plane"></div>
                </div>
                <div class="text">开始使用</div>
            </div>
        </div>
        <div class="sky-container" >
            <div class="ui stackable grid">
                <div class="ten wide column">
                    <img src="/static/images/logo_flat.png" height="80">
                    <h1>在线代码评测教学辅助系统</h1>
                    <div class="ui statistics" style="margin-top: 7.3%;">
                        <div class="statistic">
                            <div class="value">
                                400
                            </div>
                            <div class="label">
                                题目
                            </div>
                        </div>
                        <div class="statistic">
                            <div class="value">
                                31,200
                            </div>
                            <div class="label">
                                评测
                            </div>
                        </div>
                        <div class="statistic">
                            <div class="value">
                                2200
                            </div>
                            <div class="label">
                                用户
                            </div>
                        </div>
                    </div>
                </div>
                <div class="six wide column">
                    {% if not wejudge_session.is_logined %}
                    <div class="ui black segment">
                        <h3>用户登录</h3>
                        <div id="login_container"></div>
                    </div>
                    {% else %}

                    {% endif %}
                </div>
            </div>
        </div>
    </div>
{% endblock %}
{% block page_after_body %}
    <div class="main_container">
        <div align="center" style="margin-bottom: 5rem;">
            <h1>WeJudge 2.0<br/><small>遇见更好的你</small></h1>
        </div>
        <div class="ui four columns stackable grid">
            <div class="column" align="center">
                <i class="list layout huge icon"></i><h4>题库</h4>
                <h5>更加适合教学使用的题目，更加合理的题目管理方案</h5>
            </div>
            <div class="column" align="center">
                <i class="puzzle huge icon"></i><h4>教学</h4>
                <h5>强大的在线教学管理，在线作业练习提高快</h5>
            </div>
            <div class="column" align="center">
                <i class="share alternate huge icon"></i><h4>比赛</h4>
                <h5>即使是正规ACM比赛，也能轻松应对，准确评判</h5>
            </div>
            <div class="column" align="center">
                <i class="dashboard huge icon"></i>
                <h4>技术</h4>
                <h5>多样化判题技术，灵活选择判题模式，准确的同时也能近人情</h5>
            </div>
        </div>
    </div>
{% endblock %}
{% block page_script %}
    <script src='/static/assets/app_index/TweenMax.min.js'></script>
    <script src='/static/assets/app_index/three.min.js'></script>
    <script src="/static/assets/app_index/index.js"></script>
    <script type="text/javascript">
        $(function () {
            $.WejudgeIndexAnimate().init();
            {% if not wejudge_session.is_logined %}
            wejudge.account.global.showLoginView('login_container' , 'master');
            {% endif %}
        });
    </script>
{% endblock %}