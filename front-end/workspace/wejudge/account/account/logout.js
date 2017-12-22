/**
 * Created by lancelrq on 2017/8/24.
 */

var core = require("wejudge-core");

module.exports = {
    globalLogout: globalLogout
};

function globalLogout(app_name, after_success) {
    app_name = (typeof app_name !== 'undefined') ? app_name : "master";
    after_success = (typeof after_success !== 'undefined') ? after_success : "reload";
    core.restful({
        method: 'GET',
        responseType: "json",
        url: window.wejudge.global.account[app_name].logout_backend,
        success: function (rel) {
            if(after_success === 'reload') {
                window.location.href = window.location.href.replace(window.location.hash, '');
            }else if (typeof after_success === 'function'){
                after_success();
            }
        },
        error: function (rel, msg) {
            window.alert("登出失败：\n\n" + msg);
        }
    }).call();
}
