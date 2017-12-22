/**
 * Created by lancelrq on 2017/3/13.
 */

module.exports ={
    showCourseAsgnsList: showCourseAsgnsList,
    showArrangementsManager: showArrangementsManager,
    showCourseSettings: showCourseSettings
};


var React = require('react');
var ReactDom = require('react-dom');
var CourseAsgnsList = require("./course/CourseAsgnsList");
var ArrangementsManager = require("./course/ArrangementsManager");
var CourseSettings = require("./course/CourseSettings");


function showCourseAsgnsList(container, apis, urls, options) {
    return ReactDom.render(
        <CourseAsgnsList apis={apis}  urls={urls} options={options} />
        , document.getElementById(container))
}

function showArrangementsManager(container, apis, urls, options) {
    return ReactDom.render(
        <ArrangementsManager apis={apis}  urls={urls} options={options}/>
        , document.getElementById(container))
}

function showCourseSettings(container, apis, urls) {
    return ReactDom.render(
        <CourseSettings apis={apis}  urls={urls}/>
        , document.getElementById(container))
}