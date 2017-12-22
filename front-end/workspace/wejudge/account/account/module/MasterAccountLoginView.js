/**
 * Created by lancelrq on 2017/5/20.
 */

module.exports = MasterAccountLoginView;

var React = require('react');
var core = require('wejudge-core');


class MasterAccountLoginView extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        };
        this.apis = {
            submit: window.wejudge.global.account.master.login_backend
        };
    }

    doSubmitSuccess(rel){
        if(typeof this.props.afterSuccess === "function"){
            // 登录成功回调
            this.props.logined();
        }
        else if(this.props.afterSuccess === "reload") {
            window.location.reload();
        }

    }
    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }
    _onChange(field_name){
        var that = this;
        return function (e) {
            var newValue = e.target.value;
            that.setState({
                [field_name]: newValue
            })
        }
    }

    render() {
        var formBody = this.renderForm(
            (
                <section>
                    <core.forms.TextField
                        label="登录名称" name="username" placeholder="请输入WeJudge账户名或邮箱名称"
                        value={this.state.username} required={true}
                        onchange={this._onChange('username')} ref="UNBox"
                    />
                    <core.forms.TextField
                        label="登录密码" type="password" name="password"
                        onchange={this._onChange('password')}
                        placeholder="请输入用户密码" required={true}
                        value={this.state.password}
                    />
                    <br />
                    <div className="ui">
                        <core.forms.CheckBoxField type="toggle" label="记住登录" name="remember_me" value={true} />
                    </div>
                    {this.props.dialog ? null: <button type="submit" className="ui button fluid green">登录</button>}
                </section>
            )
        );
        return (
            <section>
                {formBody}
            </section>
        );
    }
}
