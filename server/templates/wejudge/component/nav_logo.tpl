<div class="menu">
    <a href="{% url 'wejudge.index.index' %}" class="item">
        <i class="home icon"></i>WeJudge
    </a>
    <a href="{% url 'problem.set.list' %}" class="item">
        <i class="list items icon"></i>
        {{ wejudge_const.apps.PROBLEM.0 }}
    </a>
    <div class="ui divider"></div>
    <a href="{% url 'education.index' %}" class="item">
        <i class="student icon"></i>
        {{ wejudge_const.apps.EDUCATION.0 }}
    </a>
    <a href="{% url 'education.index' %}?choose=1" class="item">
        <i class="placeholder icon"></i>
        学校列表
    </a>
    <div class="ui divider"></div>
    <a href="{% url 'contest.index' %}" class="item">
        <i class="trophy icon"></i>
        {{ wejudge_const.apps.CONTEST.0 }}
    </a>
    <div class="ui divider"></div>
    <a href="{% url 'helper.faq' %}" class="item">
        <i class="help circle icon"></i>
        {{ wejudge_const.apps.HELP.0 }}
    </a>
</div>