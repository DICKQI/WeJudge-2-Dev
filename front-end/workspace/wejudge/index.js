
(function (window, undefined) {

    window.$ = window.jQuery = require('jquery');

    require('../semantic/dist/semantic.min.js');
    require('./library/jquery.address.js');
    require('./library/jstorage.min.js');
    require('./library/sisyphus.min.js');
    require('date-functions');
    require('jquery-mousewheel');
    require('./library/jquery.datetimepicker.css');
    require('jquery-datetimepicker');


    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFtoken', window.csrf_token);
        }
    });
    $.datetimepicker.setLocale('ch');
    $.fn.search.settings.templates = $.extend($.fn.search.settings.templates, {
        message: function (message, type) {
            return '<div class="message empty"><div class="header">未找到结果</div><div class="description">请换个关键字再试</div></div>'
        }
    });

    window.wejudge = {
        account: {
            global: require("./account/global.js"),
            space: require("./account/space.js"),
        },
        problem: {
            problemset: require("./problem/problemset.js"),
            problembody: require("./problem/problembody.js"),
            judgestatus: require("./problem/judge_status.js")
        },
        education:{
            school: require("./education/school"),
            course: require("./education/course"),
            asgn: require("./education/asgn"),
            repository: require("./education/repository"),
            statistic: require("./education/statistic")
        },
        contest:{
            contest: require("./contest/contest")
        },
        global: require("./global"),
        beans: require("./module/bean"),
        plugin: require("./plugin/plugin")
    };

    try {
        console.info("一张网页，要经历怎样的过程，才能抵达用户面前？\n" +
            "一位新人，要经历怎样的成长，才能站在技术之巅？\n" +
            "探寻这里的秘密；\n" +
            "体验这里的挑战；\n" +
            "成为这里的主人；\n" +
            "如果您愿意，WeJudge团队可以为你提供一个学习技术的平台。\n");
        console.log("仅限北京师范大学（珠海校区）同学，请将简历发送至 %c lancelrq@gmail.com", "color:#ff0000");
    }catch(ex){

    }

})(window);