/**
 * Created by lancelrq on 2017/3/13.
 */

module.exports ={
    showAsgnProblemsList: showAsgnProblemsList,
    showAsgnReport: showAsgnReport,
    showAsgnSettings: showAsgnSettings,
    showAsgnRankList: showAsgnRankList,
    showAsgnReportsList: showAsgnReportsList,
    showAsgnAnswer: showAsgnAnswer,
    showAsgnVisitRequirement: showAsgnVisitRequirement,
    showAsgnRankBoard: showAsgnRankBoard
};


var React = require('react');
var ReactDom = require('react-dom');
var AsgnProblemsList = require("./asgn/AsgnProblemsList");
var AsgnReport = require("./asgn/AsgnReport");
var AsgnSettings = require("./asgn/AsgnSettings");
var AsgnRankList = require("./asgn/AsgnRankList");
var AsgnReportsList = require("./asgn/AsgnReportsList");
var AsgnAnswer = require("./asgn/AsgnAnswer");
var AsgnVisitRequirement = require("./asgn/AsgnVisitRequirement");
var AsgnRankBoard = require("./asgn/AsgnRankBoard");


function showAsgnProblemsList(container, apis, urls, is_teacher) {
    return ReactDom.render(
        <AsgnProblemsList apis={apis}  urls={urls} is_teacher={is_teacher} />
        , document.getElementById(container))
}

function showAsgnReport(container, apis, urls, mode) {
    return ReactDom.render(
        <AsgnReport apis={apis} urls={urls} mode={mode} />
        , document.getElementById(container))
}

function showAsgnRankList(container, apis, urls, options) {
    return ReactDom.render(
        <AsgnRankList apis={apis}  urls={urls} options={options} />
        , document.getElementById(container))
}

function showAsgnSettings(container, apis, urls, is_teacher) {
    return ReactDom.render(
        <AsgnSettings apis={apis}  urls={urls} is_teacher={is_teacher} />
        , document.getElementById(container))
}

function showAsgnReportsList(container, apis, urls) {
    return ReactDom.render(
        <AsgnReportsList apis={apis}  urls={urls} />
        , document.getElementById(container))
}

function showAsgnAnswer(container, apis, urls) {
    return ReactDom.render(
        <AsgnAnswer apis={apis}  urls={urls} />
        , document.getElementById(container))
}

function showAsgnVisitRequirement(container, apis, urls, options) {
    return ReactDom.render(
        <AsgnVisitRequirement apis={apis}  urls={urls} options={options}/>
        , document.getElementById(container))
}

function showAsgnRankBoard(container, apis, urls) {
    return ReactDom.render(
        <AsgnRankBoard apis={apis} urls={urls} />
        , document.getElementById(container))
}
