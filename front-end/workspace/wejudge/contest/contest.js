/**
 * Created by lancelrq on 2017/3/10.
 */

module.exports = {
    showContestList: showContestList,
    showContestLogin: showContestLogin,
    showContestProblemsList: showContestProblemsList,
    showContestRankList: showContestRankList,
    showContestSettings: showContestSettings,
    showContestFAQ: showContestFAQ,
    showContestNotice: showContestNotice,
    showContestCrossCheck: showContestCrossCheck,
    showContestAccount: showContestAccount,
    showContestProblemChoose: showContestProblemChoose,
    showStatusManager: showStatusManager,
    showContestRankBoard: showContestRankBoard,
    showPrinterQueue: showPrinterQueue,
    showContestRegister: showContestRegister
};

var React = require('react');
var ReactDom = require('react-dom');

var ContestList = require("./contest/ContestList");
var ContestLogin = require("./contest/ContestLogin");
var ContestProblemsList = require("./contest/ContestProblemsList");
var ContestSettings = require("./contest/ContestSettings");
var ContestFAQ = require("./contest/ContestFAQ");
var ContestNotice = require("./contest/ContestNotice");
var ContestAccount = require("./contest/ContestAccount");
var ContestCrossCheck = require("./contest/ContestCrossCheck");
var ContestProblemChoose = require("./contest/ContestProblemChoose");
var StatusManager = require("./contest/StatusManager");
var ContestRankList = require("./contest/ContestRankList");
var ContestRankBoard = require("./contest/ContestRankBoard");
var ContestPrinterQueue = require("./contest/ContestPrinterQueue");
var ContestRegister = require("./contest/ContestRegister");


function showContestList(container, apis, urls, is_admin) {
    return ReactDom.render(
        <ContestList apis={apis}  urls={urls} is_admin={is_admin} />
        , document.getElementById(container))
}

function showContestLogin(container, apis, options) {
    return ReactDom.render(
        <ContestLogin apis={apis} options={options}/>
        , document.getElementById(container))
}

function showContestRegister(container) {
    return ReactDom.render(
        <ContestRegister />
        , document.getElementById(container))
}

function showContestProblemsList(container, apis, urls, is_admin) {
    return ReactDom.render(
        <ContestProblemsList apis={apis} urls={urls} is_admin={is_admin}/>
        , document.getElementById(container))
}

function showContestRankList(container, apis, urls, is_referee) {
    return ReactDom.render(
        <ContestRankList apis={apis}  urls={urls} stackable is_referee={is_referee}/>
        , document.getElementById(container))
}

function showContestRankBoard(container, apis) {
    return ReactDom.render(
        <ContestRankBoard apis={apis} />
        , document.getElementById(container))
}

function showContestSettings(container, apis, urls) {
    return ReactDom.render(
        <ContestSettings apis={apis}  urls={urls} />
        , document.getElementById(container))
}
function showContestAccount(container, apis, urls) {
    return ReactDom.render(
        <ContestAccount apis={apis}  urls={urls} />
        , document.getElementById(container))
}
function showContestFAQ(container, apis, urls, is_referee) {
    return ReactDom.render(
        <ContestFAQ apis={apis} urls={urls} is_referee={is_referee}/>
        , document.getElementById(container))

}function showContestNotice(container, apis, urls, is_admin) {
    return ReactDom.render(
        <ContestNotice apis={apis} urls={urls} is_admin={is_admin} />
        , document.getElementById(container))
}
function showContestCrossCheck(container, apis, urls, is_admin) {
    return ReactDom.render(
        <ContestCrossCheck apis={apis} urls={urls} is_admin={is_admin} />
        , document.getElementById(container))

}
function showContestProblemChoose(container, apis, urls) {
    return ReactDom.render(
        <ContestProblemChoose apis={apis} urls={urls} />
        , document.getElementById(container))
}
function showStatusManager(container, apis, urls) {
    return ReactDom.render(
        <StatusManager apis={apis} urls={urls} />
        , document.getElementById(container))
}

function showPrinterQueue(container, apis, urls, is_admin) {
    return ReactDom.render(
        <ContestPrinterQueue apis={apis}  urls={urls} is_admin={is_admin} />
        , document.getElementById(container))
}
