/**
 * Created by lancelrq on 2017/1/23.
 */

module.exports = {
    showCodeSubmit: showCodeSubmit,
    showProblemEditor: showProblemEditor,
    showJudgeManager: showJudgeManager,
    showProblemView: showProblemView,
    showRelationManager: showRelationManager
};


var React = require('react');
var ReactDom = require('react-dom');

var SubmitCode = require("./modules/problembody/SubmitCode");
var ProblemEditor = require("./modules/problembody/ProblemEditor");
var JudgeManager = require("./modules/problembody/JudgeManager");
var ProblemView = require("./modules/problembody/ProblemView");
var ProblemRelations = require("./modules/problembody/ProblemRelations");


function showProblemView(container, apis, urls, optionals) {
    return ReactDom.render(
        <ProblemView apis={apis} urls={urls} optionals={optionals}  />
        , document.getElementById(container))
}


function showCodeSubmit(container, apis, urls, user_id) {
    return ReactDom.render(
        <SubmitCode apis={apis} urls={urls} user_id={user_id}/>
        , document.getElementById(container))
}

function showProblemEditor(container, apis, urls) {
    return ReactDom.render(
        <ProblemEditor apis={apis}  urls={urls} autosave />
        , document.getElementById(container))
}

function showJudgeManager(container, apis, urls, options) {
    return ReactDom.render(
        <JudgeManager apis={apis}  urls={urls} options={options}  />
        , document.getElementById(container))
}

function showRelationManager(container, apis, urls) {
    return ReactDom.render(
        <ProblemRelations apis={apis}  urls={urls}  />
        , document.getElementById(container))
}