/**
 * Created by lancelrq on 2017/4/1.
 */

var React = require("react");
var moment = require("moment");
var core = require("wejudge-core");


module.exports = AsgnSettings;

class AsgnSettings extends core.forms.FormComponent {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            entity: null
        };
        this.apis = {
            data: props.apis.asgn_settings,
            submit: props.apis.save_settings
        };
        this.LangList = core.LangList;
    }

    load(){
        var that = this;
        this.getData(function (rel) {
            that.setState({
                entity: rel.data
            });
        }, function (rel, msg) {
            that.refs.alertbox.showError(rel, msg);
        });
    }

    doSubmitSuccess(rel){
        this.refs.alertbox.showSuccess(rel, function () {

        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    render(){
        var that = this;
        var languageSelected = function () {
            var lang = that.state.entity.lang;

            return that.LangList.map((value, key) => {
                var checked = (!lang || lang === 0 || ((value[0] & lang) > 0));
                return (<core.forms.CheckBoxField
                    name="lang" key={key} label={value[1]} value={value[0]} checked={checked}/>);
            })
        };
        var asgn = this.state.entity ? this.state.entity.asgn : null;
        var sections = this.state.entity ? this.state.entity.sections : {};
        var formBody =  this.renderForm( this.state.entity ?
            <div className="ui bottom attached stackable grid segment">
                <div className="ten wide column">
                    <h3>作业设置</h3>
                    <div className="two fields">
                        <core.forms.TextField
                            label="作业名称" name="title" placeholder="请输入作业名称"
                            required value={asgn.title}/>
                        <core.forms.TextField
                            label="最高得分" name="full_score" placeholder="最低1.0，最高1000.0"
                            required value={asgn.full_score}/>
                    </div>
                    <core.forms.CKEditorField label="作业描述" name="description" value={asgn.description} />
                    <strong>可用语言</strong>（仅用于选题时初始化题目设置，具体的限制请对单个题目进行设置）
                    <div className="ui segment inline secondary fields">
                        {languageSelected()}
                    </div>
                    <core.forms.DateTimeField
                        label="公开答案时间(不写表示不公开)" name="public_answer_at"
                        value={asgn.public_answer_at ? core.tools.format_datetime(asgn.public_answer_at) : ""}/>

                    <div className="ui four inline fields secondary segment">
                        <core.forms.CheckBoxField
                            name="hide_problem_title" type="toggle" label="隐藏题目标题"
                            value="true" checked={asgn.hide_problem_title}/>
                        <core.forms.CheckBoxField
                            name="hide_student_code" type="toggle" label="隐藏学生代码"
                            value="true" checked={asgn.hide_student_code}/>
                    </div>
                </div>
                <div className="six wide column">
                    <h3>访问权限</h3>
                    {this.state.entity.arrangements.map((val, key) => {
                        var formatTime = function (time) {
                            return moment()
                                .startOf('day')
                                .add(time * 1000)
                                .format("YYYY-MM-DD HH:mm:ss")
                        };
                        var defaultStartTime = "";
                        var defaultEndTime = "";
                        try {
                            defaultStartTime = formatTime(sections[val.start_section].start_time);
                            defaultEndTime = formatTime(sections[val.end_section].end_time);
                        }catch (ex){

                        }
                        return (
                            <div key={key} className={`ui ${val.access_info.enabled ? 'green' : 'grey'} segment`}>
                                <core.forms.CheckBoxField
                                    name="arrangements" type="toggle" label={val.full_name}
                                    value={val.access_info.id} checked={val.access_info.enabled}/>
                                <div className="two fields">
                                    <core.forms.DateTimeField
                                        label="开始时间" name={"start_time_" + val.access_info.id} required
                                        value={val.access_info.start_time || defaultStartTime}/>
                                    <core.forms.DateTimeField
                                        label="结束时间" name={"end_time_" + val.access_info.id}
                                        required value={val.access_info.end_time || defaultEndTime}/>
                                </div>
                            </div>
                        )
                    })}
                </div>
            </div> : null
        );
        return (
            <div className="ui">
                <div className="ui top attached menu">
                    <div className="right menu">
                        <a className={`item ${!this.state.entity && "disabled"}`} onClick={this.submit}>
                            <i className="save icon"></i>保存设置
                        </a>
                    </div>
                </div>
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面"/>
            </div>
        );
    }
}
