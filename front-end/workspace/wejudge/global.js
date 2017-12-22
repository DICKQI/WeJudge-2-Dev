/**
 * Created by lancelrq on 2017/3/7.
 */


var accountGlobal = require("./account/global.js");

module.exports = {
    login: function (app_name, after_success) {
        app_name = (typeof app_name !== 'undefined') ? app_name : "master";
        after_success = (typeof after_success !== 'undefined') ? after_success : "reload";
        accountGlobal.globalLoginView("wj_global_login_container", app_name, after_success);
    },
    logout: function (app_name, after_success) {
        app_name = (typeof app_name !== 'undefined') ? app_name : "master";
        after_success = (typeof after_success !== 'undefined') ? after_success : "reload";
        accountGlobal.globalLogout(app_name, after_success);
    },
    register: function (app_name, after_success) {
        app_name = (typeof app_name !== 'undefined') ? app_name : "master";
        after_success = (typeof after_success !== 'undefined') ? after_success : "reload";
        accountGlobal.globalRegisterView('wj_global_register_container', app_name, after_success);
    },
    timer: require("./module/tools").wejudge_timer,
    countdown_timer: require("./module/tools").wejudge_countdown_timer,
    clock: require("./module/clock"),
    format_datetime: require("./module/tools").format_datetime
};