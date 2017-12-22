/**
 * Created by lancelrq on 2017/3/10.
 */

module.exports = {
    showSchoolIndexPage: showSchoolIndexPage,
    showCourseManager: showCourseManager,
    showEducationAccountManager: showEducationAccountManager,
    showSchoolSettingsManager: showSchoolSettingsManager,
    showMasterAccountLeader: showMasterAccountLeader
};

var React = require('react');
var ReactDom = require('react-dom');

var SchoolIndexPage = require("./school/SchoolIndexPage");
var CourseManager = require("./school/CourseManager");
var EducationAccount = require("./school/EducationAccount");
var SchoolSettings = require("./school/SchoolSettings");
var MasterAccountLeader = require("./school/MasterAccountLeader");


function showSchoolIndexPage(container, apis, urls, options) {
    return ReactDom.render(
        <SchoolIndexPage apis={apis}  urls={urls}  options={options}/>
        , document.getElementById(container))
}
function showCourseManager(container, apis, urls, options){
    return ReactDom.render(
        <CourseManager  apis={apis}  urls={urls} options={options}/>
        , document.getElementById(container));

}
function showEducationAccountManager(container, apis, urls, options){
    return ReactDom.render(
        <EducationAccount  apis={apis}  urls={urls} options={options}/>
        , document.getElementById(container));

}
function showSchoolSettingsManager(container, apis, urls){
    return ReactDom.render(
        <SchoolSettings  apis={apis}  urls={urls}/>
        , document.getElementById(container));

}
function showMasterAccountLeader(container, apis){
    return ReactDom.render(
        <MasterAccountLeader apis={apis}/>
        , document.getElementById(container));
}