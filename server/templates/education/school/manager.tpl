{% extends "education/component/base.tpl" %}
{% block edu_navbar %}{% include 'education/component/navbar_school.tpl' %}{% endblock %}
{% load attr %}
{% block page_title %}学校管理 - {{ school.name }} - {% endblock %}
{% block page_body %}
<div class="ui secondary pointing menu" id="MainNavList">
    <a class="active item" data-tab="settings">
        <i class="setting icon"></i>
        学校信息
    </a>
    <a class=" item" data-tab="account">
        <i class="users icon"></i>
        账号管理
    </a>
    <!--a class=" item" data-tab="group">
        <i class="sitemap icon"></i>
        学校组织管理(暂未开发)
    </a-->
</div>
<div class="ui active tab" data-tab="settings">
    <div id="settings_container"></div>
</div>
    <div class="ui tab" data-tab="account">
    <div id="account_container"></div>
</div>
<!--div class="ui tab" data-tab="group">
    <div id="group_container"></div>
</div-->
<br>
{% endblock %}
{% block page_script %}
    <script type="text/javascript">
    $(function () {
        wejudge.beans.register('school_settings', function () {
            return wejudge.education.school.showSchoolSettingsManager(
                "settings_container",
                {
                    school_info: "{% url 'api.education.settings.info' school.id %}",
                    save_settings: '{% url 'api.education.settings.save' school.id %}',
                    save_sections: '{% url 'api.education.settings.sections.save' school.id %}',
                    change_yearterm: '{% url 'api.education.settings.yearterm.change' school.id %}'
                },
                {}
            );
        });
        wejudge.beans.register('education_account', function () {
            return wejudge.education.school.showEducationAccountManager(
                "account_container",
                {
                    account_list: "{% url 'api.education.account.list' school.id %}",
                    edit_account: "{% url 'api.education.account.edit' school.id %}",
                    delete_account: "{% url 'api.education.account.delete' school.id %}",
                    upload_xls: "{% url 'api.education.account.import' school.id %}"
                },
                {},
                {
                    academies: eval('({{ academies | safe }})')
                }
            );
        });
        $("#MainNavList>.item").tab({
            history: true,
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if (tab_name == "settings") {
                    wejudge.beans.getBean('school_settings').load();
                }else if(tab_name == "account") {
                    wejudge.beans.getBean('education_account').load();
                }
            }
        });
    });
    </script>
{% endblock %}