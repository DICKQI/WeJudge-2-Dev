/*
* Created by lancelrq on 2017/7/29.
*/

var React = require("react");
var core = require("wejudge-core");
var HeadimgAvatar = require('./HeadimgAvatar');

module.exports = WeJudgeAccountSettings;


class WeJudgeAccountSettings extends core.PageView{

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: this.props.apis.account_infos
        }
    }

    renderBody(){
        return (
            <div className="ui grid">
                <div className="six wide column">
                    <h3>用户设置</h3>
                    <AccountSettings
                        ref="settings_view"
                        account={this.state.data}
                        manager={this}
                        save_settings={this.props.apis.save_settings}
                    />
                </div>
                <div className="ten wide column">
                    <h3>头像设置</h3>
                    <HeadimgAvatar
                        upload_api={this.props.apis.upload_headimg}
                    />
                </div>
            </div>
        )
    }
}

class AccountSettings extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            entity: props.account,
        };
        this.apis = {
            submit: this.props.save_settings
        };
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            entity: nextProps.account
        })
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            window.location.reload();
            //that.manager.load()
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    render(){
        var entity = this.state.entity;
        var formBody = this.renderForm(
            this.state.entity ?
                <div className="ui form">
                    <core.forms.TextField
                        label="当前密码(修改设置时必须填写)" type="password"
                        name="password" required
                    />
                    <core.forms.TextField
                        label="登录名称" name="username" placeholder="请输入登录用户名，可以修改，不能重复"
                        max_length="20" required value={entity.username}
                    />
                    <div className="two fields">
                        <core.forms.TextField
                            label="新密码" name="newpassword"  type="password"
                            max_length="20" placeholder="如果需要修改密码请填写"
                        />
                        <core.forms.TextField
                            label="重复新密码" name="renewpassword" type="password"
                            max_length="20" placeholder="你懂的"
                        />
                    </div>
                    <div className="two fields">
                        <core.forms.TextField
                            label="用户昵称" name="nickname" placeholder="请输入账户昵称" required
                            value={entity.nickname} max_length="20"
                        />
                        <core.forms.TextField
                            label="真实姓名" name="realname" placeholder="请输入真实姓名"
                            value={entity.realname} max_length="20"
                        />
                    </div>
                    <div className="two fields">
                        <core.forms.SelectField
                            label="性别" name="sex" forceDefault required
                            value={entity.sex !== undefined ? entity.sex + "" : null}
                        >
                            <option value="-1">保密</option>
                            <option value="0">女</option>
                            <option value="1">男</option>
                        </core.forms.SelectField>
                        <core.forms.TextField
                            label="Email" name="email" placeholder="请输入e-mail地址" required
                            value={entity.email}  max_length="64"
                        />
                    </div>
                    <core.forms.TextAreaField
                        label="个人简介" name="motto" placeholder="请输入个人简介"
                        value={entity.motto} max_length="100"
                    />

                    <button className="ui green button"><i className="save icon"></i>保存设置</button>
                </div> : null
        );
        return (
            <div className="ui">
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}
