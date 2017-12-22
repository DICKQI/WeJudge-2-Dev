/**
 * Created by lancelrq on 2017/4/16.
 */

module.exports = BNUZ_ESValidater;

var React = require('react');
var core = require('wejudge-core');


class BNUZ_ESValidater extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.unmount = false;
        this.apis = {
            submit: props.apis.submit
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
        this.refs.alertbox.showSuccess(rel, function () {
            window.location.reload();
        });
    }
    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    render() {
        return (
            <section>
                <core.dialog.Dialog ref="FormDialog" title="北师珠教务系统认证" btnTitle="验证" size="tiny">
                    {this.renderForm(
                        (
                            <section>
                                <core.forms.TextField label="学号" name="username" placeholder="请输入您的学号" required={true} />
                                <core.forms.TextField label="密码" type="password" name="password" placeholder="请输入您的教务（选课）密码" required={true} />
                                <br />
                                {!this.props.dialog ? null: <button type="submit" className="ui button green">验证</button>}
                                <span>
                                    <i className="info circle icon"></i> 验证信息由【北师珠教务系统】提供
                                </span>
                            </section>
                        )
                    )}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="验证成功！" msg="请使用您刚输入的学号和密码登录系统。" />
            </section>
        )
    }
}

//
// function bnuzLoginCheck(container, api){
//     var loginDialog = ReactDom.render(
//
//         , document.getElementById(container));
//     loginDialog.show();
// }
