{% extends "wejudge/component/base.tpl" %}
{% block page_head %}
<style type="text/css">
    .wj_page_container{
        width: 100% !important;
        height: 100% !important;
    }
    .ui.menu{
        margin: 0 !important;
    }
    #main_background{
        background-image: url(/static/images/bg/1.jpg);
        background-repeat: no-repeat;
        background-size: 100% 100%;
        height: 100%;
    }
    .logo_panel{
        width: 350px;
        height: 300px;
        position: relative;
        top:15%;
        margin: 0 auto;
        text-align: center;
    }
</style>
{% endblock %}
{% block page_body %}
    <div id="main_background">
        <div class="logo_panel">
            <br>
            <img src="/static/images/logo_flat.png" style="max-height: 80px; height:80px;"><br />
            <span style="font-size: 1.2em; font-weight: 500; letter-spacing: 0.5em; line-height: 3.2em; color: #fff;">在线代码评测教学辅助系统</span><br />
        </div>
    </div>
{% endblock %}
{% block page_after_body %}
    <div class="ui container">
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
        <br /><br />
    </div>
{% endblock %}