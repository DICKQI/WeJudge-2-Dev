/**
 * Created by lancelrq on 2017/7/19.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = CourseManager;

class CourseManager extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis={
            data: props.apis.course_data
        };
        this.createCourse = this.createCourse.bind(this);
    }

    componentDidMount() {
        this.getData();
    }

    createCourse(){
        this.refs.editor.create(this.props.options.teacher_id);
    }
    
    renderBody(){
        return (
            <section>
                <div className="ui blue segment">
                    <div className="ui header">本学期所有课程</div>
                    {this.state.data.courses_list && this.state.data.courses_list.length > 0 ?
                        <div className="ui relaxed divided list">
                        {this.state.data.courses_list.map((val, key)=> {
                            return (
                                <div className="item" key={key}>
                                    <i className="book big middle aligned icon"></i>
                                    <div className="content" style={{lineHeight: "1.5rem"}}>
                                        <a className="header"
                                           href={this.props.urls.course_view.replace("course/0", "course/" + val.id)}
                                        >{val.name} ({val.academy.name})</a>
                                        <div className="description" title={val.description}>
                                            任课教师：<a href="javascript:void(0)" onClick={core.show_account('education', val.author.id)}>{val.author.realname}</a>
                                        </div>
                                    </div>

                                </div>
                            )
                        })}
                        </div>
                        :
                        <div className="content">
                            还没有课程信息，请先创建
                        </div>
                    }
                </div>
                {this.props.options.is_teacher ? <div className="ui compact menu">
                    <a className="item" onClick={this.createCourse}>
                        <i className="add icon"></i>
                        创建课程
                    </a>
                </div> : null}
                <CourseEditor
                    manager={this}
                    ref="editor"
                    create={this.props.apis.create_course}
                    search_teacher={this.props.apis.search_teacher}
                    academies={this.props.options.academies}
                />
            </section>
        );
    }
}

class CourseEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.apis = {
            submit: this.props.create
        };
        this.state = {
            teacher_id: ""
        };
        this.create = this.create.bind(this);
    }

    create(teacher_id){
        var that = this;
        this.setState({
            teacher_id: teacher_id || ""
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.getData();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            <div className="ui">
                {this.state.teacher_id ?
                    <div>
                        <div className="ui required disabled field">
                            <label>归属老师</label>
                            <input type="text" value={this.state.teacher_id}/>
                        </div>
                        <input type="hidden" name="teacher" value={this.state.teacher_id}/>
                    </div>
                    :
                    <div className="ui required field">
                        <label>归属老师</label>
                        <core.forms.SearchField
                            name="teacher"
                            ref="search_teacher"
                            icon="search"
                            search_api={this.props.search_teacher}
                        />
                    </div>
                }
                <core.forms.SelectField label="归属学院" name="academy" forceDefault>
                    {this.props.academies.map((val, key) => {
                        return (
                            <option key={key} value={val.id}>{val.name}</option>
                        );
                    })}
                </core.forms.SelectField>
                <core.forms.TextField
                    label="课程名称" name="name" placeholder="请输入课程名称" required/>
                <core.forms.TextAreaField
                    label="课程简介" name="description" placeholder="请输入课程简介" />
            </div>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="创建新课程" size="small" btnTitle="创建">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="创建成功" msg="请进入课程进行相关的设置" />
            </div>

        );
    }

}