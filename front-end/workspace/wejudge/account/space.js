/**
 * Created by lancelrq on 2017/7/28.
 */


var React = require('react');
var ReactDom = require('react-dom');

module.exports = {
    showWeJudgeProblemVisited: showWeJudgeProblemVisited,
    showWeJudgeAccountSettings: showWeJudgeAccountSettings,
    showEducationSolutionVisited: showEducationSolutionVisited,
    showEducationAccountSettings: showEducationAccountSettings,
    showAccountCard: showAccountCard,
};

var WeJudgeProblemVisited = require('./space/WeJudgeProblemVisited');
var WeJudgeAccountSettings = require('./space/WeJudgeAccountSettings');
var EducationSolutionVisited = require('./space/EducationSolutionVisited');
var EducationAccountSettings = require('./space/EducationAccountSettings');
var AccountCard = require('./space/AccountCard');


function showEducationSolutionVisited(container, apis, urls){
    return ReactDom.render(
        <EducationSolutionVisited apis={apis} urls={urls} />
        , document.getElementById(container))
}

function showEducationAccountSettings(container, apis, urls){
    return ReactDom.render(
        <EducationAccountSettings apis={apis} urls={urls} />
        , document.getElementById(container))
}


function showWeJudgeProblemVisited(container, apis, urls){
    return ReactDom.render(
        <WeJudgeProblemVisited apis={apis} urls={urls} />
        , document.getElementById(container))
}


function showWeJudgeAccountSettings(container, apis, urls){
    return ReactDom.render(
        <WeJudgeAccountSettings apis={apis} urls={urls} />
        , document.getElementById(container))
}

function showAccountCard(app_name, account_id){
    var cardDialog = ReactDom.render(<AccountCard />, document.getElementById("wj_global_account_card_container"));
    cardDialog.show(app_name, account_id);
}