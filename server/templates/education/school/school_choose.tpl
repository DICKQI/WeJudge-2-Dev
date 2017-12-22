{% extends "wejudge/component/base.tpl" %}
{% block page_title %}选择学校 - 在线教学 - {% endblock %}
{% block page_body %}
<div class="ui stackable four column grid">
    {% for school in school_list %}
    <div class="column">
        <div class="ui card">
            {% if school.logo %}<div class="image"><img src="{{ school.logo }}" alt=""></div>{% endif %}
            <div class="content">
                <div class="header">{{ school.name }}</div>
                <div class="description">{{ school.description }}</div>
            </div>
            <div class="extra content">
                <a class="ui fluid green button" href="{% url 'education.school' school.id %}">选择</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}