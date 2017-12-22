/**
 * Created by lancelrq on 2017/9/9.
 */


var React = require("react");
var core = require("wejudge-core");

module.exports = MasterAccountLeader;

class MasterAccountLeader extends core.forms.FormComponent{

    constructor(props){
        super(props);
        this.apis = {
            submit: props.apis.register_leader
        };
        this.state = {
            mode: "register"
        };
        this.show = this.show.bind(this);
    }

    show(){
        var that = this;
        this.refs.MainDialog.show(function () {
            that.submit();
            return false;
        });
    }

    exchange(mode){
        var that = this;
        return function () {
            that.setState({
                "mode": mode
            })
        }
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            window.location.reload();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            (
                <section>
                    <input type="hidden" name="mode" value={this.state.mode} />
                    { this.state.mode === "register" ?
                        <div>
                            <core.forms.TextField label="用户昵称" name="nickname" placeholder="给自己取个好听的名字吧"/>
                            <core.forms.TextField label="新的登录密码" type="password" name="password" placeholder="请输入新的登录密码" required={true} />
                            <core.forms.TextField label="重复密码" type="password" name="repassword" placeholder="你懂的" required={true} />
                            <a href="javascript:void(0)" onClick={this.exchange.bind(this)('login')}>我曾经注册过WeJudge账号</a>
                        </div>
                        :
                        <div>
                            <core.forms.TextField label="登录名称" name="username" placeholder="WeJudge主账户用户名" required={true}/>
                            <core.forms.TextField label="登录密码" type="password" name="password" placeholder="WeJudge主账户密码" required={true} />
                            <a href="javascript:void(0)" onClick={this.exchange.bind(this)('register')}>我要新建WeJudge账号</a>
                        </div>
                    }
                    </section>
            )
        );
        return <div>
            <core.dialog.Dialog
                ref="MainDialog"
                title="欢迎使用WeJudge教学系统"
                btnTitle={this.state.mode === "register" ? "激活主账户": "绑定"}
                size="tiny"
            >
                {this.state.mode === "register" ?
                    <h4>在开始使用系统之前，<br />请先激活WeJudge主账号，以开启更多的功能。<br/>设置一个好记的密码，一个好听的名字，一同开启我们的代码之旅吧！</h4>
                    : <h4>绑定WeJudge主账号，以获得更好的体验！</h4>
                }
                <div className="ui divider"></div>
                {formBody}
            </core.dialog.Dialog>
            <core.dialog.Alert ref="alertbox" msg_title="保存成功" msg="点击确定刷新页面" />
        </div>
    }
}