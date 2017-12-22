{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include "education/component/navbar_course.tpl" %}{% endblock %}
{% block page_title %}{{ course.name }} ({{ course.term }}) - {{ school.name }} - {% endblock %}
{% block page_body %}
    <div class="ui stackable grid">
        <div class="four wide column">
                <div class="ui black segment">
                    <h3 class="header">{{ course.name }}</h3>
                    <div class="content">
                        <div class="description">
                            <p>{{course.description}}</p>
                            <div class="ui divider"></div>
                            <p><strong>创建者：</strong><a href="javascript:void(0)" onclick="wejudge.account.space.showAccountCard('education', {{ course.author.id}})">{{ course.author.realname }}</a></p>
                            <p><strong>任课教师：</strong>{% for teachers in course_teachers %}<a href="javascript:void(0)" onclick="wejudge.account.space.showAccountCard('education', {{ teachers.id}})">{{teachers.realname}}</a>&nbsp;&nbsp;{% endfor %}</p>
                            <p><strong>开课单位：</strong>{{course.academy.name}}</p>
                            <p><strong>课程时间：</strong>{{course.term}}</p>
                            <div class="ui divider"></div>
                            <h4>上课时间</h4>
                            <div class="ui ordered list">
                                {% for arr in course_arrangements %}
                                <div class="item">{{ arr.toString }}</div>
                                {% empty %}
                                <div><i class="remove icon"></i>暂未设置</div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
        </div>
        <div class="twelve wide column">
            <div id="course_asgns_container"></div>
        </div>
    </div>
    <div id="maccount_leader_container"></div>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        var is_teacher = false;
        {% if wejudge_session.account.role >= 1 %}
            is_teacher = true;
        {% endif %}
         wejudge.beans.register('course_asgns', function() {
            return wejudge.education.course.showCourseAsgnsList(
                "course_asgns_container",
                {
                    course_asgns: "{% url 'api.education.course.asgns' school.id course.id %}",
                    create_asgn: "{% url 'api.education.asgn.create' school.id course.id %}"
                },
                {
                    asgn_view: "{% url 'education.asgn.index' school.id 0 %}",
                    asgn_manager: "{% url 'education.asgn.manager' school.id 0 %}"
                },
                {
                    is_teacher: is_teacher
                }
            );
        });
         {% if wejudge_session.logined and wejudge_session.account.master is None %}
        wejudge.education.school.showMasterAccountLeader(
            'maccount_leader_container',
            {
                register_leader: "{% url 'api.education.bind.master' school.id %}"
            }
        ).show();
        {% endif %}
        wejudge.beans.getBean('course_asgns').load();
    });
    </script>
{% endblock %}