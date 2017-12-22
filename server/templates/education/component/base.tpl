{% extends 'base.tpl' %}
{% block page_navbar %}{% block edu_navbar %}{% endblock %}{% endblock %}
{% block base_script %}
    <script type="text/javascript">
        /*WeJudge Education Script*/
        window.wejudge.global.account["education"] = {
            "login_backend": "{% url 'api.education.account.login' school.id %}",
            "logout_backend": "{% url 'api.education.account.logout' school.id %}",
            "check_master": "{% url 'api.education.account.check.master' school.id %}",
            "login_use_master": "{% url 'api.education.account.use.master.login' school.id %}",
            "account_info_api": "{% url 'api.education.account.space.info' school.id 0 %}",
            "account_space_view": "{% url 'account.education.space' school.id 0 %}",
            "account_space_avator": "{% url 'education.account.space.avator' school.id 0 %}"
        };
    </script>
{% endblock %}