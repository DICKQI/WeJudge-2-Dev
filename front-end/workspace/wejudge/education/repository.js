/**
 * Created by lancelrq on 2017/8/12.
 */

module.exports = {
    showRepositoryList,
    showRepositoryView
};

var React = require('react');
var ReactDom = require('react-dom');

var RepositoryList = require("./repository/RepositoryList");
var RepositoryView = require("./repository/RepositoryView");


function showRepositoryList(container, apis, urls, options) {
    return ReactDom.render(
        <RepositoryList apis={apis}  urls={urls} options={options} />
        , document.getElementById(container))
}

function showRepositoryView(container, apis, urls, options) {
    return ReactDom.render(
        <RepositoryView apis={apis}  urls={urls} options={options} />
        , document.getElementById(container))
}
