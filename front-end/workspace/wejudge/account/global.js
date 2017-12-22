/**
 * Created by lancelrq on 2017/3/7.
 */



var login_module = require("./account/login");
var logout_module = require("./account/logout");
var register_module = require("./account/register");

module.exports = {
    showLoginView: login_module.showLoginView,
    globalLoginView: login_module.globalLoginView,
    globalLogout: logout_module.globalLogout,
    globalRegisterView: register_module.globalRegisterView
};
