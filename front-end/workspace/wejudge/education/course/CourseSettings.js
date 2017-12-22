
var React = require("react");
var core = require("wejudge-core");


module.exports = CourseSettings;

class CourseSettings extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.course_info
        };
        this.addAssistant = this.addAssistant.bind(this);
        this.addTeacher = this.addTeacher.bind(this);
    }

    addTeacher(){
        var that = this;
        var user_id = that.refs.search_teacher.getValue();
        core.restful({
            url: that.props.apis.toggle_teacher,
            data:{
                user_id: user_id
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.load()
                });
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }

    addAssistant(){
        var that = this;
        var user_id = that.refs.search_assistant.getValue();
        core.restful({
            url: that.props.apis.toggle_assistant,
            data:{
                user_id: user_id
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.load()
                });
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }

    renderBody() {
        var course_info = this.state.data.course;
        var teachers = this.state.data.teachers;
        var assistants = this.state.data.assistants;
        // var repositories = this.state.data.repositories;
        var education = this.state.data.education;
        return (
            <div className="ui grid">
                <div className="row">
                    <div className="sisteen wide column">
                        <div className="ui black segment">
                            <CourseSetting
                                manager={this}
                                entity={course_info}
                                education={education}
                            />
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="eight wide column">
                        <div className="ui top attached stackable menu">
                            <div className="header item">助教管理</div>
                            <div className="item">
                                <core.forms.SearchField
                                    ref="search_assistant"
                                    icon="search" transparent
                                    search_api={this.props.apis.search_student}
                                />
                            </div>
                            <a className="item" onClick={this.addAssistant}>
                                <i className="add icon"></i>添加
                            </a>
                        </div>
                        <div className="ui bottom attached segment">
                            <AccountList
                                manager={this}
                                account_list={assistants}
                                toggle_api={this.props.apis.toggle_assistant}
                            />
                        </div>
                    </div>
                    <div className="eight wide column">
                        <div className="ui top attached stackable menu">
                            <div className="header item">任课教师管理</div>
                            <div className="item">
                                <core.forms.SearchField
                                    ref="search_teacher"
                                    icon="search" transparent
                                    search_api={this.props.apis.search_teacher}
                                />
                            </div>
                            <a className="item" onClick={this.addTeacher}>
                                <i className="add icon"></i>添加
                            </a>
                        </div>
                        <div className="ui bottom attached segment">
                            <AccountList
                                manager={this}
                                account_list={teachers}
                                toggle_api={this.props.apis.toggle_teacher}
                            />
                        </div>
                    </div>
                </div>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm  ref="confirm"  msg_title="操作确认" msg="你确定要执行当前操作吗？" />
            </div>
        );
    }
}


class CourseSetting extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            entity: props.entity,
            education: props.education
        };
        this.apis={
            submit: this.manager.props.apis.save_settings
        }
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.load()
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            entity: nextProps.entity,
            education: nextProps.education
        })
    }

    render(){
        var entity  = this.state.entity;
        var education  = this.state.education;
        var formBody = this.renderForm(
            this.state.entity ?
                <div className="ui">
                   <core.forms.TextField
                       label="课程名称" name="name" placeholder="请输入课程名称"
                       required value={entity.name}/>
                   <core.forms.TextAreaField
                       label="课程简介" name="description" placeholder="请输入课程简介"
                       value={entity.description}/>
                   <div className="two fields">
                       <core.forms.SelectField label="学年学期" name="term" forceDefault value={entity.term.id}>
                           {education.yearterms.map((val, key) => {
                               return (
                                   <option key={key} value={val.id}>{`${val.year}-${val.year+1}年度第${val.term}学期`}</option>
                               );
                           })}
                       </core.forms.SelectField>
                       <core.forms.SelectField label="归属学院" name="academy" forceDefault value={entity.academy.id}>
                           {education.academies.map((val, key) => {
                               return (
                                   <option key={key} value={val.id}>{val.name}</option>
                               );
                           })}
                       </core.forms.SelectField>
                   </div>
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


class AccountList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.manager = props.manager;
        this.state['listdata'] = props.account_list;
        this.state['show_pagination'] = false;
        this.state['inited'] = true;
        this.deleteAccount = this.deleteAccount.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            listdata: nextProps.account_list
        })
    }

    deleteAccount(entity){
        var that = this;
        return function () {
            that.manager.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.toggle_api,
                        data:{
                            user_id: entity.username,
                            remove: true
                        },
                        method: "POST",
                        success: function (rel) {
                            that.manager.refs.alertbox.showSuccess(rel, function () {
                                that.manager.load();
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
                <th>学号/工号</th>
                <th>真实姓名</th>
                <th>昵称</th>
                <th>操作</th>
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return <tr key={key}>
                    <td>{item.username}</td>
                    <td>{item.realname}</td>
                    <td>{item.nickname}</td>
                    <td>
                        <a className="ui  basic tiny compact red button" onClick={this.deleteAccount(item)}>
                            <i className="remove icon"></i>删除
                        </a>
                    </td>
                </tr>
            });
        else
            return null
    }

}