/**
 * Created by lancelrq on 2017/10/6.
 */

module.exports ={
    showAsgnStatistic: showAsgnStatistic,
};


var React = require('react');
var ReactDom = require('react-dom');
var AsgnStatistic = require("./statistic/AsgnStatistic");

function showAsgnStatistic(container, apis) {
    return ReactDom.render(
        <AsgnStatistic apis={apis} />
        , document.getElementById(container))
}
