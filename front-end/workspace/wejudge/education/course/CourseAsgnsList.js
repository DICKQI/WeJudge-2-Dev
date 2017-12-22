/**
 * Created by lancelrq on 2017/3/13.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = CourseAsgnsList;

class CourseAsgnsList extends core.ListView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.course_asgns
        };
        this.createAsgn = this.createAsgn.bind(this);
    }

    createAsgn(){
        this.refs.editor.create();
    }

    renderListHeader(){
        return (
            <tr>
                <th>作业名称</th>
                <th>作业题量</th>
                <th>作业状态</th>
                <th>截止时间</th>
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((val, key) => {
                var card_color = "", card_state = "", card_icon = "";
                switch (val.status) {
                    case -2:
                    {
                        card_icon = "lock";
                        card_color = "gray";
                        card_state = "无权限";
                        break;
                    }
                    case -1:
                    {
                        card_icon = "puzzle";
                        card_color = "red";
                        card_state = "未访问";
                        break;
                    }
                    case 0:
                    {
                        card_icon = "arrow right";
                        card_color = "yellow";
                        card_state = "未提交实验报告";
                        break;
                    }
                    case 1:
                    {
                        card_icon = "hourglass half";
                        card_color = "green";
                        card_state = "已提交实验报告";
                        break;
                    }
                    case 2:
                    {
                        card_icon = "checkmark";
                        card_color = "blue";
                        card_state = "已批改";
                        break;
                    }
                    case 3:
                    {
                        if (val.pending_check_count === 0) {
                            card_icon = "checkmark";
                            card_color = "green";
                            card_state = "无需批改";
                        } else {
                            card_color = "orange";
                            card_icon = "wait";
                            card_state = `${val.pending_check_count}项待批改`;
                        }
                        break;
                    }
                }
                return <tr key={key}>
                    <td>
                        {val.status > -2 ?
                        <a  className="header"
                            href={this.props.urls.asgn_view.replace("asgn/0", "asgn/" + val.id)}
                            target="_blank">{val.title}</a> : val.title}
                    </td>
                    <td>{val.problems_count}题</td>
                    <td><i className={`${card_color} big ${card_icon} middle aligned icon`}></i>{card_state}</td>
                    <td>{this.props.options.is_teacher ? <div>
                            <a href={this.props.urls.asgn_manager.replace("asgn/0", "asgn/" + val.id)} className="ui mini green button">批改</a>
                            <a href={this.props.urls.asgn_manager.replace("asgn/0", "asgn/" + val.id) + "#/settings"} className="ui mini primary button">管理</a>
                            <a href={this.props.urls.asgn_manager.replace("asgn/0", "asgn/" + val.id) + "#/delete"} className="ui mini red button">删除</a>
                        </div>
                        : val.deadline ? (val.nowtime - val.deadline) > 0 ? "已截止" : core.tools.format_datetime(val.deadline) : "---"}
                    </td>
                </tr>
            });
        else
            return null
    }

    renderFooterBody(){
        return <div>
            <br />
            {this.props.options.is_teacher ? <div className="ui compact menu">
                <a className="item" onClick={this.createAsgn}>
                    <i className="add icon"></i>
                    发布作业
                </a>
            </div> : null}
            <AsgnEditor
                manager={this}
                ref="editor"
                create={this.props.apis.create_asgn}
                view_asgn_manager={this.props.urls.asgn_manager + "#/problems"}
            />
        </div>
    }

}

class AsgnEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.apis = {
            submit: this.props.create
        };
        this.create = this.create.bind(this);
    }

    create(){
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            window.location.href=that.props.view_asgn_manager.replace("asgn/0", "asgn/" + rel.data)
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            <div className="ui">
                <core.forms.TextField
                    label="作业名称" name="title" placeholder="请输入作业名称" required/>
                <core.forms.TextField
                    label="最高得分" name="full_score" placeholder="最低1.0，最高1000.0" required value="100"/>
                <div className="ui message">
                    <i className="warning circle icon"></i> 详细的内容请在发布作业后，<br />在【批改与管理】页面设置。
                </div>
            </div>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="发布作业" size="mini" btnTitle="发布">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="发布成功" msg="请进入作业进行相关设置" />
            </div>

        );
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
                <core.dialog.Dialog ref="FormDialog" title="从Excel文件导入账户" size="tiny" btnTitle="确定">
                    <section>
                        <a href="/static/xls/education_account.xls">下载模板</a>
                        {!this.state.unmount_uploader ? <core.forms.FileField ref="upload" upload_api={this.props.upload} auto/> : null }
                    </section>
                </core.dialog.Dialog>
            </div>

        );
    }

}