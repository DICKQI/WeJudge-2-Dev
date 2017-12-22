/**
 * Created by lancelrq on 2017/1/18.
 */

module.exports = {
    showProblemsList: showProblemsList,
    showProblemChoosing: showProblemChoosing,
    showProblemsetList: showProblemsetList,
    showClassifyManager: showClassifyManager

};

var React = require('react');
var ReactDom = require('react-dom');

var ProblemsList = require("./modules/problemset/ProblemsList").ProblemsList;
var ProblemsetList = require("./modules/problemset/ProblemsetList").ProblemsetList;
var ProblemChoosing = require("./modules/problemset/ProblemChoosing");
var ClassifyManager = require("./modules/problemset/ClassifyManager");


function showProblemsetList(container, apis, urls, options) {
    return ReactDom.render(
        <ProblemsetList apis={apis} urls={urls} options={options}/>
        , document.getElementById(container))
}


function showProblemsList(container, apis, urls, options) {
    return ReactDom.render(
        <ProblemsList apis={apis} urls={urls}  options={options}/>
        , document.getElementById(container))
}

function showProblemChoosing(container, apis, urls) {
    return ReactDom.render(
        <ProblemChoosing apis={apis} urls={urls} />
        , document.getElementById(container))
}


function showClassifyManager(container, apis, urls) {
    return ReactDom.render(
        <ClassifyManager apis={apis} urls={urls} />
        , document.getElementById(container))
}

