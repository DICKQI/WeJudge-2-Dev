/**
 * Created by lancelrq on 2017/7/30.
 */

module.exports = MasterRegisterView;

var React = require('react');
var core = require('wejudge-core');


class MasterRegisterView extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.apis = {
            submit: window.wejudge.global.account.master.register_backend
        };
    }

    show() {
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            if(typeof that.props.afterSuccess === "function"){
                // 登录成功回调
                that.props.registed();
            }
            else if(that.props.afterSuccess === "reload") {
                window.location.reload();
            }
        });
    }
    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    renderLoginView() {
        var formBody = this.renderForm(
            (
                <section>
                    <core.forms.TextField label="登录名称" name="username" placeholder="请输入，用于登录账号" required={true} />
                    <div className="two fields">
                        <core.forms.TextField label="登录密码" type="password" name="password" placeholder="请输入登录密码" required={true} />
                        <core.forms.TextField label="重复登录密码" type="password" name="repassword" placeholder="你懂的" required={true} />
                    </div>
                    <core.forms.TextField label="用户昵称" name="nickname" placeholder="请输入昵称" required={true} />
                    <core.forms.TextField label="Email" name="email" placeholder="请输入电子邮箱" required={true} />
                    {this.props.dialog ? null: <button type="submit" className="ui button fluid green">注册</button>}
                </section>
            )
        );
        return formBody;
    }

    render() {
        if(this.props.dialog)
            return (
                <section>
                    <core.dialog.Dialog ref="FormDialog" title="注册WeJudge用户" btnTitle="注册" size="mini">
                        {this.renderLoginView()}
                    </core.dialog.Dialog>
                    <core.dialog.Alert ref="alertbox" msg_title="注册成功！" msg="请使用您的账户名和密码注册并使用" />
                </section>
            );
        else
            return <section>
                {this.renderLoginView()}
                <core.dialog.Alert ref="alertbox" msg_title="注册成功!" msg="请使用您的账户名和密码注册并使用" />
            </section>
    }
}
