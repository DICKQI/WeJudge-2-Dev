{% extends 'base.tpl' %}
{% block page_navbar %}{% block contest_navbar %}{% endblock %}{% endblock %}
{% block base_script %}
    <script type="text/javascript">
        /*WeJudge Contest Script*/
        window.wejudge.global.account["contest"] = {
            "login_backend": "{% url 'api.contest.account.login' contest.id %}",
            "logout_backend": "{% url 'api.contest.account.logout' contest.id %}",
            "check_master": "{% url 'api.contest.account.check.master' contest.id %}",
            "login_use_master": "{% url 'api.contest.account.use.master.login' contest.id %}",
            "register_backend": "{% url 'api.contest.account.register' contest.id %}"
        };
    </script>
{% endblock %}