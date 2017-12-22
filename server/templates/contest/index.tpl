{% extends "wejudge/component/base.tpl" %}
{% load attr %}
{% block page_title %}在线比赛 - {% endblock %}
{% block page_body %}
    <div class="wj_page_container" id="contest_list_container"></div>
    <br />
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    var is_admin = {% if wejudge_session.account.permission_create_contest %}true{% else %}false{% endif %};
    $(function () {
        wejudge.contest.contest.showContestList(
            "contest_list_container",
            {
                contest_list: "{% url 'api.contest.list' %}",
                create_contest: "{% url 'api.contest.create' %}"
            },
            {
                contest_view: "{% url 'contest.contest' 0 %}"
            },
            is_admin
        )
    });
    </script>
{% endblock %}