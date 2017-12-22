/**
 * Created by lancelrq on 2017/4/13.
 */


var React = require("react");
var core = require("wejudge-core");

module.exports = ContestAccount;



class ContestAccount extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.showCreate = this.showCreate.bind(this);
        this.showImport = this.showImport.bind(this);
    }

    showCreate(){
        this.refs.editor.create();
    }
    showImport(){
        this.refs.xls_importer.show();
    }
    load(){
        this.refs.listView.getListData();
    }

    render() {
        var that = this;
        return (
            <div className="ui">
                <div>
                    <div className="ui compact menu">
                        <a className="item" onClick={this.showCreate}><i className="add icon"></i> 新建账户</a>
                        <a className="item" onClick={this.showImport}><i className="file excel outline icon"></i> 从Excel导入账户</a>
                    </div>
                </div>
                <ContestAccountList
                    ref="listView"
                    account_list={this.props.apis.account_list}
                    delete_account={this.props.apis.delete_account}
                    manager={this}
                />
                <ContestAccountEditor
                    ref="editor"
                    edit_account={this.props.apis.edit_account}
                    manager={this}
                />
                <ContestAccountXLSImporter
                    ref="xls_importer"
                    upload={this.props.apis.upload_xls}
                    manager={this}
                />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="你确定要删除这个账号吗？" msg_title="操作确认" ref="confirm" />
            </div>
        )
    }
}

class ContestAccountList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.manager = props.manager;
        this.apis = {
            data: props.account_list
        };
        this.showModify = this.showModify.bind(this);
        this.deleteAccount = this.deleteAccount.bind(this);
    }

    showModify(entity){
        var that = this;
        return function(){
            that.manager.refs.editor.modify(entity);
        }
    }
    deleteAccount(uid){
        var that = this;
        return function () {
            that.manager.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.delete_account + "?id=" + uid,
                        method: "POST",
                        success: function (rel) {
                            that.manager.refs.alertbox.showSuccess(rel, function () {
                                that.manager.refs.listView.getListData();
                            });
                        },
                        error: function (rel, msg) {
                            that.manager.refs.alertbox.showError(rel, msg);
                        }
                    }).call()
                }
            });
        }
    }

    renderListHeader(){
        return (
            <tr>
                <th>ID</th>
                <th>登录名称</th>
                <th>用户身份</th>
                <th>明文密码</th>
                <th>队伍名称</th>
                <th>参赛队员</th>
                <th>红名</th>
                <th>最终排名</th>
                <th>管理</th>
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key}>
                        <td>#{item.id}</td>
                        <td>{item.username}</td>
                        <td>{item.role == 2 ? "管理员" : item.role == 1 ? "裁判" : "参赛者"}</td>
                        <td>{item.clear_password}</td>
                        <td>{item.nickname}</td>
                        <td>{item.realname}</td>
                        <td>{item.role == 0 ? item.sex==0 ? "是" : "否" : "---"}</td>
                        <td>{item.role == 0 ? item.ignore_rank ? "不参与" : (item.finally_rank == 0) ? "暂无" : item.finally_rank : "---"}</td>
                        <td>
                            <a className="ui tiny primary button" onClick={this.showModify(item)}>编辑</a>
                            <a className="ui tiny red button" onClick={this.deleteAccount(item.id)}>删除</a>
                        </td>
                    </tr>
                )
            });
        else
            return null
    }
}



class ContestAccountEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            dialog_title: "",
            entity: {},
            is_new: false
        };
        this.apis = {
            submit: props.edit_account
        }
    }

    create(){
        var that = this;
        this.setState({
            dialog_title: "新建账户",
            is_new: true,
            entity: {}
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    modify(entity){
        var that = this;
        this.setState({
            dialog_title: "编辑账户",
            entity: entity,
            is_new: false
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.load();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var is_new = this.state.is_new;
        var formBody = this.renderForm(
            <section>
                <input type="hidden" name="id" value={this.state.entity.id || "0"} />
                <core.forms.TextField label="登录名称" name="username" value={this.state.entity.username} required />
                <div className="inline fields">
                    <core.forms.RadioField
                        label="参赛者" name="role"
                        value="0" checked={is_new || this.state.entity.role==0} />
                    <core.forms.RadioField
                        label="裁判" name="role"
                        value="1" checked={this.state.entity.role==1}
                    />
                    <core.forms.RadioField
                        label="管理员" name="role"
                        value="2" checked={this.state.entity.role==2}
                    />
                </div>
                <core.forms.TextField label="登录密码" name="password" value={this.state.entity.password || ""} placeholder={is_new ? "不填则自动生成（8位）" : "不填则不修改，填入“随机”或者“random”会随机生成8位密码"} />
                <core.forms.CheckBoxField label="保存一份明文" type="toggle" name="save_clear_pwd" value="true" checked={is_new}/>
                出于安全性考虑，如果账户绑定过主账户，则更改密码功能无效。
                <core.forms.TextField label="队伍名称" name="nickname" value={this.state.entity.nickname} required />
                <core.forms.TextField label="参赛成员" name="realname" value={this.state.entity.realname} required />
                <core.forms.CheckBoxField label="红名" type="toggle" name="sex" value="true" checked={this.state.entity.sex == 0} />
                <core.forms.CheckBoxField label="不参与最终排名" type="toggle" name="ignore_rank" value="true" checked={this.state.entity.ignore_rank} />

            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title={this.state.dialog_title} size="small" btnTitle="保存">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="保存成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}



class ContestAccountXLSImporter extends React.Component {

    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            unmount_uploader: false
        };
    }

    show(){
        var that = this;
        that.setState({
            unmount_uploader: false
        });
        this.refs.FormDialog.show(function () {
            that.setState({
                unmount_uploader: true
            });
            that.manager.load();
        });
    }

    render(){
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="从Excel文件导入账户" size="small" btnTitle="确定">
                    <section>
                        <a href="/static/xls/contest_account.xls">下载模板</a>
                        {!this.state.unmount_uploader ? <core.forms.FileField ref="upload" upload_api={this.props.upload} auto/> : null }
                    </section>
                </core.dialog.Dialog>
            </div>

        );
    }

}