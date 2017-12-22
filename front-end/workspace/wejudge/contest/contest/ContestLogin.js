/**
 * Created by lancelrq on 2017/4/6.
 */

module.exports = ContestLogin;

var React = require('react');
var core = require('wejudge-core');
var LoginView = require("../../account/account/module/LoginView");
var ContestRegisterView = require("../../account/account/module/ContestRegisterView");
var BNUZ_ESValidater = require("../../plugin/module/BNUZ_ESValidater");


class ContestLogin extends React.Component{

    constructor(props) {
        super(props);
    }

    showRegister(){
        this.refs.register_view.show();
    }

    render() {
        return  (
            <section>
                {this.props.options.register_mode && this.props.options.register_mode !=="none"  ?
                    <a className="ui primary fluid huge button" onClick={this.showRegister.bind(this)}>
                        <i className="sign out icon"></i>点击这里报名参加
                    </a>
                : null}
                <div className="ui stacked segment"  style={{maxWidth: 350}}>
                    <h2>登录比赛系统</h2>
                    <div className="ui divider"></div>
                    <LoginView afterSuccess="reload" app_name='contest' hide_master />
                </div>
                {this.props.options.register_mode === 'register' ?
                    <ContestRegisterView ref="register_view" /> : null
                }
                {this.props.options.register_mode === 'bnuz_validater' ?        // it don't work!
                    <BNUZ_ESValidater ref="register_view" submit="" /> : null
                }
            </section>
        );
    }
}

