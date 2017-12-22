<div class="ui breadcrumb" id="wejudge_breadcrumb_navbar" style="margin-bottom: 10px;">
    <a href="/"><i class="home icon"></i> WeJudge首页</a>
    <i class="right chevron icon divider"></i>
    {% for navitem in wejudge_navlist %}
    {% if not forloop.last %}
    {% if navitem.1 is None %}{{ navitem.0 }}{% else %}<a class="section" href="{{ navitem.1 }}">{{ navitem.0 }}</a>{% endif %}
    <i class="right chevron icon divider"></i>
    {% else %}
    <p class="section">{{ navitem.0 }}</p>
    {% endif %}
    {% endfor %}
</div>

