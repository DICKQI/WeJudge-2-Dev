/**
 * Created by lancelrq on 2017/1/18.
 */

module.exports = {
    showStatusList: showStatusList,
    showJudgeStatusDetail: showJudgeStatusDetail
};

var React = require('react');
var ReactDom = require('react-dom');

var JudgeStatusList = require("./modules/judge_status/JudgeStatusList").JudgeStatusList;
var JudgeStatusDetail = require("./modules/judge_status/JudgeStatusDetail");

function showStatusList(container, apis, urls, options) {
    return ReactDom.render(
        <JudgeStatusList apis={apis} urls={urls} options={options}/>
        , document.getElementById(container))
}

function showJudgeStatusDetail(container, apis, urls) {
    return ReactDom.render(
        <JudgeStatusDetail apis={apis}  urls={urls} />
        , document.getElementById(container))
}
