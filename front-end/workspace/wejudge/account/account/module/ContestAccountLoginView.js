/**
 * Created by lancelrq on 2017/6/4.
 */

module.exports = ContestAccountLoginView;

var React = require('react');
var core = require('wejudge-core');


class ContestAccountLoginView extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.apis = {
            submit: window.wejudge.global.account.contest.login_backend
        };

        this.loginMasterChanged = this.loginMasterChanged.bind(this);
        this.useGeneralLogin = this.useGeneralLogin.bind(this);
        this.useFastLogin = this.useFastLogin.bind(this);
        this.useMasterLogin = this.useMasterLogin.bind(this);
        // this.usernameCheckupWorker = null;
        // this._onChange = this._onChange.bind(this);
        this.state = {
            username: "",
            password: "",
            rembme_disabled: false,
            view_login_link: false,
            login_info: null
        }
    }

    checkMasterLogin(){
        var that = this;
        core.restful({
            method: 'GET',
            responseType: "json",
            url: window.wejudge.global.account.contest.check_master,
            success: function (rel) {
                if(rel.data) {
                    that.setState({
                        login_info: rel.data,
                        view_login_link: true
                    });
                }
            },
            error: function (rel, msg) {
                console.log("ERROR: 无法加载用户登录信息")
            }
        }).call();
    }

    useMasterLogin(){
        var that = this;
        core.restful({
            method: 'POST',
            responseType: "json",
            url: window.wejudge.global.account.contest.login_use_master,
            success: function (rel) {
                if(typeof that.props.afterSuccess == "function"){
                    // 登录成功回调
                    that.props.logined();
                }
                else if(that.props.afterSuccess === "reload") {
                    window.location.reload();
                }
            },
            error: function (rel, msg) {
                window.alert("登录失败！\n\n" + msg);
            }
        }).call();
    }

    useGeneralLogin(){
        this.setState({
            view_login_link: false
        })
    }
    useFastLogin(){
        this.setState({
            view_login_link: true
        })
    }

    componentDidMount() {
        var that = this;
        $(this.refs.LoginLink).find('.image').dimmer({
            on: 'hover'
        });
        setTimeout(function () {
            that.checkMasterLogin();
        }, 100); //延时100ms后触发登录用户检查
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
    submit(){
        // 重写
        if(this.state.view_login_link) this.useMasterLogin();
        else super.submit();
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

    loginMasterChanged(ev) {
        if(ev.target.checked){
            this.setState({
                'rembme_disabled': false
            })
        }else{
            this.setState({
                'rembme_disabled': true
            })
        }

    }

    render() {
        var formBody = this.renderForm(
            (
                <section>
                    <core.forms.TextField
                        label="登录名称" name="username" placeholder="请输入用户名"
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
                        <core.forms.CheckBoxField type="toggle" label="同时登录主账号" name="login_master" value={true} onchange={this.loginMasterChanged} />
                        <core.forms.CheckBoxField type="toggle" label="主账号记住登录" name="remember_me" value={true} disabled={this.state.rembme_disabled} />
                    </div>
                    {this.props.dialog ? null: <br />}
                    {this.props.dialog ? null: <button  type="submit" className="ui button fluid green">登录</button>}
                    <br />
                    {this.state.login_info ? <a href="javascript:void(0)" onClick={this.useFastLogin}><i className="icon reply"></i>使用快速登录</a> : null}
                </section>
            )
        );
        return (
            <section>
                <div ref="LoginForm" style={{display: this.state.view_login_link ? "none" : "block"}}>
                    {formBody}
                </div>
                <div ref="LoginLink" style={{display: this.state.view_login_link ? "block" : "none"}}>
                    <div className="ui card" style={{width:"200px", margin:"0 auto"}}>
                        <div className="blurring dimmable image">
                            <div className="ui dimmer">
                                <div className="content">
                                    <div className="center">
                                        <button className="ui inverted green button" onClick={this.useMasterLogin}>快速登录</button>
                                    </div>
                                </div>
                            </div>
                            <img src={this.state.login_info ? (this.state.login_info.user.headimg || "/static/images/user_placeholder.png") : "/static/images/user_placeholder.png"} />
                        </div>
                        <div className="content">
                            <span className="header">{this.state.login_info ? this.state.login_info.user.nickname : null}</span>
                            <div className="meta">
                                {this.state.login_info ? this.state.login_info.user.username : null}
                            </div>
                        </div>
                        <div className="extra content">
                            <a onClick={this.useGeneralLogin}><i className="icon reply"></i>使用账号密码登录</a>
                        </div>
                    </div>
                </div>
            </section>
        );
    }
}
