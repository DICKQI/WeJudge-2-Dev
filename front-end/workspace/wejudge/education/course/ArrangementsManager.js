
var React = require("react");
var core = require("wejudge-core");


module.exports = ArrangementsManager;

class ArrangementsManager extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.get_arrangements_list
        };
        this.state['api_student_list'] = "";
        this.createArrangement = this.createArrangement.bind(this);
        this.modifyArrangement = this.modifyArrangement.bind(this);
        this.deleteArrangement = this.deleteArrangement.bind(this);
        this.addStudent = this.addStudent.bind(this);
        this.deleteStudent = this.deleteStudent.bind(this);
        this.openXLSImporter = this.openXLSImporter.bind(this);
    }

    componentDidMount() {
        this.tabBind();
    }
    componentDidUpdate() {
        this.tabBind();
    }

    tabBind(){
        var that = this;
        $(this.refs.ArrListMenu).find('.item').tab({
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if(tab_name !== "arr_index")
                    that.refs[tab_name.replace("arr_", "arrs_list_")].load();
            }
        });
    }

    createArrangement(){
        this.refs.arrangement_editor.create();
    }

    modifyArrangement(entity){
        var that = this;
        return function(){
            that.refs.arrangement_editor.modify(entity);
        }
    }
    deleteArrangement(entity){
        var that = this;
        return function () {
            that.refs.arr_confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.change_arrangement,
                        data:{
                            id: entity.id,
                            delete: true
                        },
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.load();
                            });
                        },
                        error: function (rel, msg) {
                            that.refs.alertbox.showError(rel, msg);
                        }
                    }).call()
                }
            });
        }
    }
    addStudent(entity){
        var that = this;
        return function () {
            var student_id = that.refs["search_" + entity.id].getValue();
            core.restful({
                url: that.props.apis.toggle_student,
                data:{
                    id: entity.id,
                    user_id: student_id
                },
                method: "POST",
                success: function (rel) {
                    that.refs.alertbox.showSuccess(rel, function () {
                        that.refs["arrs_list_" + entity.id].load();
                        that.refs["search_" + entity.id].clearValue();
                    });
                },
                error: function (rel, msg) {
                    that.refs.alertbox.showError(rel, msg);
                }
            }).call()
        }
    }
    deleteStudent(entity, user_id){
        var that = this;
        return function () {
            var student_id = user_id || that.refs["search_" + entity.id].getValue();
            that.refs.stu_confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.toggle_student,
                        data:{
                            id: entity.id,
                            user_id: student_id,
                            remove: true
                        },
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.refs["arrs_list_" + entity.id].load();
                                that.refs["search_" + entity.id].clearValue();
                            });
                        },
                        error: function (rel, msg) {
                            that.refs.alertbox.showError(rel, msg);
                        }
                    }).call()
                }
            });
        }
    }

    openXLSImporter(arrid){
        var that = this;
        return function () {
            that.refs['xls_importer_' +arrid].show(function () {
                that.load(function () {
                    that.refs["arrs_list_" + arrid].load();
                });
            });
        }
    }


    renderBody() {
        var arrangements = this.state.data;
        var that = this;
        return (
            <div className="ui stackable grid">
                <div className="four wide column">
                    <div ref="ArrListMenu" className="ui fluid vertical pointing menu">
                        <a data-tab="arr_index" className="primary active item"><i className="large middle aligned tasks icon"></i> 排课管理</a>
                        {arrangements && arrangements.length > 0 ? arrangements.map(function (val, key) {
                            return <a key={key} data-tab={`arr_${val.id}`} className="primary item">
                                {val.name ? val.name : core.tools.get_arrangement_desc(val)}
                                <div className="ui label">{val.students_count}</div>
                            </a>
                        }) : <span className="item">请先增加排课</span> }
                    </div>
                </div>
                <div className="twelve wide column">
                    <div className="ui tab active" data-tab="arr_index">
                        <div className="ui top attached stackable menu">
                            <a className="item" onClick={this.createArrangement}><i className="add icon"></i>新增</a>
                        </div>
                        <div className="ui bottom attached segment">
                            <div className="ui relaxed divided list">
                                {arrangements && arrangements.length > 0 ? arrangements.map(function (val, key) {
                                    return <div className="item" key={key}>
                                        <a className="ui right floated basic tiny red button" onClick={that.deleteArrangement(val)}><i className="remove icon"></i>删除</a>
                                        <a className="ui right floated basic tiny primary button" onClick={that.modifyArrangement(val)}><i className="edit icon"></i>编辑</a>
                                        <i className="large bookmark middle aligned icon"></i>
                                        <div className="content">
                                            <span className="header">{val.name || `排课${key+1}`}</span>
                                            <div className="description">{core.tools.get_arrangement_desc(val)}</div>
                                        </div>

                                    </div>
                                }) : <div className="content">请增加排课信息</div>}
                            </div>
                            <core.dialog.Confirm  ref="arr_confirm"  msg_title="操作确认" msg="你确定要删除这个排课吗？这将会删除关于设个排课的所有设置信息！" />
                        </div>
                    </div>
                    {arrangements && arrangements.map(function (val, key) {
                        return <div key={key} className="ui tab" data-tab={`arr_${val.id}`}>
                            <div className="ui stackable menu">
                                <div className="item">
                                    <core.forms.SearchField
                                        ref={`search_${val.id}`}
                                        icon="arrow right" transparent
                                        search_api={that.props.apis.search_student}
                                    />
                                </div>
                                <a className="item" onClick={that.addStudent(val)}>
                                    <i className="add icon"></i>添加到排课
                                </a>
                                <a className="item" onClick={that.deleteStudent(val)}>
                                    <i className="remove icon"></i>从排课中移除
                                </a>
                                <a className="item" onClick={that.openXLSImporter(val.id)}>
                                    <i className="file excel outline icon"></i>从Excel导入
                                </a>
                            </div>
                            <ArrangementStudentList
                                ref={`arrs_list_${val.id}`}
                                student_list={that.props.apis.student_list.replace('arrangement/0', 'arrangement/' + val.id)}
                                arrangement={val}
                                manager={that}
                            />
                            <EducationAccountXLSImporter
                                ref={`xls_importer_${val.id}`}
                                upload={that.props.apis.toggle_student_by_xls.replace('arrangement/0', 'arrangement/' + val.id)}
                                manager={that}
                            />
                        </div>
                    })}
                    <ArrangementEditor
                        ref="arrangement_editor"
                        api_submit={this.props.apis.change_arrangement}
                        manager={this}
                    />
                    <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                    <core.dialog.Confirm  ref="stu_confirm"  msg_title="操作确认" msg="你确定要从当前排课里删除这个学生吗？" />
                </div>
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

    show(onclose){
        var that = this;
        that.setState({
            unmount_uploader: false
        });
        this.refs.FormDialog.show(function () {
            that.setState({
                unmount_uploader: true
            });
        }, function () {
            onclose && onclose();
        });
    }

    render(){
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="从Excel文件导入" size="tiny" btnShow={false}>
                    <section>
                        <a href="/static/xls/education_import_student.xls">下载模板</a>
                        {!this.state.unmount_uploader ? <core.forms.FileField ref="upload" upload_api={this.props.upload} auto/> : null }
                    </section>
                </core.dialog.Dialog>
            </div>

        );
    }

}

class ArrangementStudentList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.manager = props.manager;
        this.apis = {
            data: props.student_list
        };
    }

    componentWillReceiveProps(nextProps) {
        this.apis['data'] = nextProps.student_list
    }

    renderListHeader(){
        return (
            <tr>
                <th>用户名（学号）</th>
                <th>真实姓名</th>
                <th>昵称</th>
                <th>操作</th>
            </tr>
        );
    }
    renderListItems(){
        var that = this;
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key}>
                        <td>{item.username}</td>
                        <td>{item.realname}</td>
                        <td>{item.nickname}</td>
                        <td>
                            <a className="ui basic tiny compact red button" onClick={that.manager.deleteStudent(that.props.arrangement, item.username)}>
                                <i className="remove icon"></i>删除
                            </a>
                        </td>
                    </tr>
                )
            });
        else
            return null
    }
}


class ArrangementEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            dialog_title: "",
            entity: {},
            options: this.manager.props.options,
            is_new: false
        };
        this.apis = {
            submit: props.api_submit
        }
    }

    create(){
        var that = this;
        this.setState({
            dialog_title: "新建排课",
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
            dialog_title: "编辑排课信息",
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
        var entity = this.state.entity || {};
        var options = this.state.options || {};
        var weeks = [], weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        for(var i = 1; i <= options.max_week; i++)
            weeks.push(i);
        var formBody = this.renderForm(
            <section>
                <input type="hidden" name="id" value={entity.id || "0"} />
                <core.forms.TextField label="排课名称" name="name" value={entity.name || ""} placeholder="非必填，不填时显示具体时间" />
                <div className="ui divider"></div>
                <div className="ui inline fields segment">
                    <core.forms.RadioField
                        label="正常" name="odd_even" inline
                        value="0" checked={entity.odd_even != 1 && entity.odd_even != 2} />
                    <core.forms.RadioField
                        label="仅单周" name="odd_even" inline
                        value="1" checked={entity.odd_even==1}
                    />
                    <core.forms.RadioField
                        label="仅双周" name="odd_even" inline
                        value="2" checked={entity.odd_even==2}
                    />
                </div>
                <div className="ui inline fields">
                    <core.forms.SelectField name="start_week" label="开始周" required value={entity.start_week || 1}>
                        {weeks.map(function (val, key) {
                            return <option value={val} key={key}>{val}</option>
                        })}
                    </core.forms.SelectField>
                    <core.forms.SelectField name="end_week" label="结束周" required value={entity.end_week || 17}>
                        {weeks.map(function (val, key) {
                            return <option value={val} key={key}>{val}</option>
                        })}
                    </core.forms.SelectField>
                </div>
                <div className="ui inline fields">
                    <core.forms.SelectField name="day_of_week" label="周几？" required value={entity.day_of_week || 1}>
                        {weekdays.map(function (val, key) {
                            return <option value={key} key={key}>{val}</option>
                        })}
                    </core.forms.SelectField>
                    <core.forms.SelectField name="start_section" label="开始节" required value={entity.start_section || 1}>
                        {weeks.map(function (val, key) {
                            return <option value={val} key={key}>{val}</option>
                        })}
                    </core.forms.SelectField>
                    <core.forms.SelectField name="end_section" label="结束节" required value={entity.end_section || 2}>
                        {weeks.map(function (val, key) {
                            return <option value={val} key={key}>{val}</option>
                        })}
                    </core.forms.SelectField>
                </div>
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title={this.state.dialog_title} size="middle" btnTitle="保存">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="保存成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}
