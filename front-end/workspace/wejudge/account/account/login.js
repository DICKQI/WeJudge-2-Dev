/**
 * Created by lancelrq on 2017/1/14.
 */

module.exports = {
    showLoginView: showLoginView,
    globalLoginView: globalLoginView
};


var React = require('react');
var ReactDom = require('react-dom');
var LoginView = require('./module/LoginView');


function showLoginView(container, app_name){
    return ReactDom.render(
        <LoginView app_name={app_name} afterSuccess="reload" />
        , document.getElementById(container))
}


function globalLoginView(container, app_name, after_success){
    app_name = (typeof app_name !== 'undefined') ? app_name : "master";
    after_success = (typeof after_success !== 'undefined') ? after_success : "reload";
    var loginDialog = ReactDom.render(
        <LoginView dialog afterSuccess={after_success} app_name={app_name} />
        , document.getElementById(container));
    loginDialog.show();
}