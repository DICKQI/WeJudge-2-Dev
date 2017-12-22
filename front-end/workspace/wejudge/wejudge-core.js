/**
 * Created by lancelrq on 2017/3/3.
 */

module.exports = {
    dialog: require("./module/dialog"),
    forms: require("./module/forms"),
    ListView: require("./module/listview"),
    Pagination: require("./module/pagination"),
    restful: require("./module/restful"),
    dimmer: require("./module/dimmer"),
    PageView: require("./module/pageview"),
    utils: require("./module/utils"),
    JSTree: require("./module/jstree"),
    LangList: [
        [1, "C语言 (GNU C)"],
        [2, "C++ (GNU CPP)"],
        [4, "Java 1.8"],
        [8, "Python 2.7"],
        [16, "Python 3.5"]
    ],
    tools: require("./module/tools"),
    show_account: function (app_name, account_id) {
        var accountSpace = require("./account/space.js");
        return function (e) {
            accountSpace.showAccountCard(app_name, account_id);
        }
    },
};