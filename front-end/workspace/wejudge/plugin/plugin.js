/**
 * Created by lancelrq on 2017/9/14.
 */

var React = require('react');
var ReactDom = require('react-dom');


module.exports = {
    showBNUZ_ESValidater: showBNUZ_ESValidater
};

var BNUZ_ESValidater = require("./module/BNUZ_ESValidater");


function showBNUZ_ESValidater(container, apis){
    return ReactDom.render(
        <BNUZ_ESValidater apis={apis} />
        , document.getElementById(container))
}
