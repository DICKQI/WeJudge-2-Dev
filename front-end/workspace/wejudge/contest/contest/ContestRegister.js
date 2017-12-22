/**
 * Created by lancelrq on 2017/11/30.
 */

module.exports = ContestRegister;

var React = require('react');
var core = require('wejudge-core');
var ContestRegisterView = require("../../account/account/module/ContestRegisterView");


class ContestRegister extends React.Component{

    constructor(props) {
        super(props);
    }

    showRegister(){
        this.refs.register_view.show();
    }

    render() {
        return  (
            <section>
                <a className="ui primary fluid huge button" onClick={this.showRegister.bind(this)}>
                    <i className="sign out icon"></i>我要报名参加本次比赛
                </a>
                <ContestRegisterView ref="register_view" />
            </section>
        );
    }
}

