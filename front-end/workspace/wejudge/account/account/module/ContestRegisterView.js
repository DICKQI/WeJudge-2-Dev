/**
 * Created by lancelrq on 2017/7/30.
 */

module.exports = ContestRegisterView;

var React = require('react');
var core = require('wejudge-core');


class ContestRegisterView extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.state = {
            entity: {}
        };
        this.apis = {
            submit: window.wejudge.global.account.contest.register_backend,
            data: window.wejudge.global.account.master.my_account_info
        };
    }

    show() {
        if(!this.apis.data){
            this.refs.alertbox.showError({}, "请先登录WeJudge主账户");
            return;
        }
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
        that.getData(function (rel) {
            that.setState({
                entity: rel.data
            })
        });
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

    render() {
        return (
            <section>
                <core.dialog.Dialog ref="FormDialog" title="报名参赛" btnTitle="报名" size="mini">
                    {this.renderForm(
                        (
                            <section>
                                <input type="hidden" name="action" value="register"/>
                                <core.forms.TextField label="身份名称" name="username" placeholder="请输入身份标识" value={this.state.entity.username && this.state.entity.username.replace("bnuz", "")} readonly required={true} />
                                <core.forms.TextField label="队伍名称" name="nickname" placeholder="请输入队伍名称" value={this.state.entity.realname} required={true} readonly />
                            </section>
                        )
                    )}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="报名成功！" msg="点击确定刷新" />
            </section>
        );
    }
}
