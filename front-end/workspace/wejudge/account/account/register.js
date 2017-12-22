/**
 * Created by lancelrq on 2017/8/24.
 */

module.exports = {
    globalRegisterView: globalRegisterView
};

var React = require('react');
var ReactDom = require('react-dom');

var MasterRegisterView = require('./module/MasterRegisterView');


function globalRegisterView(container, app_name, after_success){
    after_success = (typeof after_success !== 'undefined') ? after_success : "reload";
    if (app_name === 'master') {
        var registerDialog = ReactDom.render(
            <MasterRegisterView dialog afterSuccess={after_success} app_name={app_name}/>
            , document.getElementById(container));
        registerDialog.show();
    }
}
