/**
 * Created by lancelrq on 2017/7/21.
 */


var React = require("react");
var core = require("wejudge-core");

module.exports = EducationAccount;



class EducationAccount extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.showCreate = this.showCreate.bind(this);
        this.showImport = this.showImport.bind(this);
        this.showFilter = this.showFilter.bind(this);
        this.onFilter = this.onFilter.bind(this);
        this.education = {
            academies: this.props.options.academies
        }
    }

    onFilter(formdata){
        this.refs.listView.setParams(formdata);
        this.refs.listView.getListData();
    }
    showFilter () {
        this.refs.filter.show();
    };
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
                        <a className="item" onClick={this.showFilter}><i className="filter icon"></i> 筛选</a>
                        <a className="item" onClick={this.showImport}><i className="file excel outline icon"></i> 从Excel导入账户</a>
                    </div>
                </div>
                <EducationAccountList
                    ref="listView"
                    account_list={this.props.apis.account_list}
                    delete_account={this.props.apis.delete_account}
                    manager={this}
                    education={this.education}
                />
                <EducationAccountEditor
                    ref="editor"
                    edit_account={this.props.apis.edit_account}
                    manager={this}
                    education={this.education}
                />
                <EducationAccountXLSImporter
                    ref="xls_importer"
                    upload={this.props.apis.upload_xls}
                    manager={this}
                />
                <EducationAccountFilter
                    onFilter={this.onFilter}
                    ref="filter"
                    manager={this}
                    education={this.education}
                />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="你确定要删除这个账号吗？账号关联的所有信息都将被删除！" msg_title="操作确认" ref="confirm" />
            </div>
        )
    }
}

class EducationAccountList extends core.ListView {

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
        this.AcademiesInfo = {};
        for(var i = 0; i < props.education.academies.length; i++){
            var a = props.education.academies[i];
            this.AcademiesInfo[a.id] = a.name
        }
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
                <th>用户身份</th>
                <th>学号/工号/登录名称</th>
                <th>真实姓名</th>
                <th>账号昵称</th>
                <th>性别</th>
                {/*<th>归属学院</th>*/}
                <th>WeJudge主账户登录名</th>
                <th>管理</th>
            </tr>
        );
    }
    renderListItems(){
        var USER_ROLE_CALL = { 0: "学生", 2: "教师", 3: "教务/管理员"};
        var USRE_SEX_CALL = {"-1": "未知", 0: "女", 1: "男"};

        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key} className={`${item.role === 2 ?"positive": item.role === 3 ? 'warning' : null} `}>
                        <td>{item.locked ? <i className="lock icon" />:<i className="user icon" />}{item.id}</td>
                        <td>{USER_ROLE_CALL[item.role]}</td>
                        <td>{item.username}</td>
                        <td>{item.realname}</td>
                        <td>{item.nickname}</td>
                        <td>{USRE_SEX_CALL[item.sex]}</td>
                        {/*<td>{this.AcademiesInfo[item.academy_id]}</td>*/}
                        <td>{item.master ? item.master.username : "未绑定"}</td>
                        <td>
                            <a className="ui tiny primary compact button" onClick={this.showModify(item)}>编辑</a>
                            <a className="ui tiny red compact button" onClick={this.deleteAccount(item.id)}>删除</a>
                        </td>
                    </tr>
                )
            });
        else
            return null
    }
}

class EducationAccountEditor extends core.forms.FormComponent {


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
                <div className="two fields">
                    <core.forms.TextField
                        label="学号/工号/登录名称" name="username"
                        value={this.state.entity.username} required />
                    <core.forms.TextField
                        label="登录密码" name="password"
                        value={this.state.entity.password || ""}
                        placeholder={is_new ? "不填则为用户名+12345678" : "不填则不修改"}
                        disabled={this.state.entity.master}
                    />
                </div>
                由于安全策略影响，如账户绑定过WeJudge账户，则更改密码功能停用，请联系WeJudge系统管理员！
                <br /><br />
                <div className="ui inline fields segment">
                    <core.forms.RadioField
                        label="学生" name="role"
                        value="0" checked={is_new || this.state.entity.role===0} />
                    <core.forms.RadioField
                        label="教师" name="role"
                        value="2" checked={this.state.entity.role===2}
                    />
                    <core.forms.RadioField
                        label="教务/管理员" name="role"
                        value="3" checked={this.state.entity.role===3}
                    />
                </div>
                *创建或编辑教师、教务角色的账号时，如果该账号没有绑定WeJudge主账户，则会自动创建并绑定。<br />**该WeJudge主账户拥有创建题目、题目集和比赛的高级权限。
                <br /><br />
                <div className="three fields">
                    <core.forms.TextField label="真实姓名" name="realname" value={this.state.entity.realname} required />
                    <core.forms.TextField label="账号昵称" name="nickname" value={this.state.entity.nickname} required />
                    <core.forms.SelectField
                        label="性别" name="sex"
                        value={this.state.entity.sex !== undefined ? this.state.entity.sex + "" : null}
                    >
                        <option value="0">女</option>
                        <option value="1">男</option>
                    </core.forms.SelectField>
                </div>
                <core.forms.SelectField label="归属学院" name="academy" value={this.state.entity.academy_id}>
                    {this.props.education.academies.map((val, key) => {
                        return (
                            <option key={key} value={val.id}>{val.name}</option>
                        );
                    })}
                </core.forms.SelectField>
                <div className="ui fields segment">
                    <core.forms.CheckBoxField
                        label="锁定账号" type="toggle" name="lock"
                        value="true" checked={this.state.entity.lock}
                    />
                    <core.forms.CheckBoxField
                        label="解除WeJudge主账户绑定(仅对学生角色有效)" type="toggle" name="unbind" value="true"
                    />
                </div>
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

class EducationAccountFilter extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
    }

    show(){
        var that = this;
        this.refs.FilterDialog.show(function () {
            // OK
            if(typeof that.props.onFilter === "function")
                var arraydata = $(that.refs.FilterFormPanel).serializeArray();
            var formdata = {};
            arraydata.map((val, key) => {
                formdata[val.name] = val.value;
            });
            that.props.onFilter(formdata);
        }, function () {
            // Close
        })
    }

    render(){
        return (
            <core.dialog.Dialog ref="FilterDialog" size="mini" btnTitle="筛选" title="筛选评测结果">
                <form className="ui form" ref="FilterFormPanel">
                    <core.forms.TextField name="keyword" label="关键词" placeholder="学号/工号/登录名/昵称/真实姓名" />
                    <core.forms.SelectField name="role" label="用户角色" forceDefault >
                        <option value="-1">全部</option>
                        <option value="0">学生</option>
                        <option value="2">教师</option>
                        <option value="3">教务/管理员</option>
                    </core.forms.SelectField>
                    <core.forms.SelectField label="归属学院" name="academy" forceDefault>
                        <option value="-1">全部</option>
                        {this.props.education.academies.map((val, key) => {
                            return (
                                <option key={key} value={val.id}>{val.name}</option>
                            );
                        })}
                    </core.forms.SelectField>
                    <div className="ui segment">
                        <core.forms.CheckBoxField name="desc" type="toggle" label="按ID倒序排列" value="true"/>
                    </div>
                </form>
            </core.dialog.Dialog>
        )
    }
}

class EducationAccountXLSImporter extends React.Component {

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
                <core.dialog.Dialog ref="FormDialog" title="从Excel文件导入账户" size="tiny" btnShow={false}>
                    <section>
                        <a href="/static/xls/education_account.xls">下载模板</a>
                        {!this.state.unmount_uploader ? <core.forms.FileField ref="upload" upload_api={this.props.upload} auto/> : null }
                        <span>账户初始密码为"学号+12345678"</span>
                    </section>
                </core.dialog.Dialog>
            </div>

        );
    }

}

