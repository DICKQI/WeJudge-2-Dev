/**
 * Created by lancelrq on 2017/3/4.
 */

var React = require('react');
var core = require('wejudge-core');

var ProblemEditor = require("./ProblemEditor");
var JudgeConfigManager = require("./manager/JudgeConfigManager");
var TestCaseManager = require("./manager/TestCaseManager");
var AnswerCaseManager = require("./manager/AnswerCaseManager");
var DemoCaseManager = require("./manager/DemoCaseManager");

module.exports = JudgeManager;

class JudgeManager extends React.Component {

    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            judge_config: {},
            problem_type: props.options.problem_type || 0,
            is_onwer: props.options.is_onwer || false,
            lang_selected: 1,
            view_problem_editor: false
        };
        this.init_problem_editor = false;
        this.LangList = [
            [1, "C语言 (GNU C)"],
            [2, "C++ (GNU CPP)"],
            [4, "Java 1.8"],
            [8, "Python 2.7"],
            [16, "Python 3.5"]
        ];
        this.LangCall = {
            1: "C语言 (GNU C)",
            2: "C++ (GNU CPP)",
            4: "Java 1.8",
            8: "Python 2.7",
            16: "Python 3.5"
        };
        this.changeLang = this.changeLang.bind(this);
        this.toggleJudge = this.toggleJudge.bind(this);
    }


    showProcessingDimmer(){
        $(this.refs.ProcessingDimmer).dimmer("show");
    }
    hideProcessingDimmer(){
        $(this.refs.ProcessingDimmer).dimmer("hide");
    }

    getJudgeConfig(){
        var that = this;
        this.showProcessingDimmer();
        core.restful({
            method: 'POST',
            responseType: "json",
            url: that.props.apis.judge_config,
            success: function (rel) {
                that.hideProcessingDimmer();
                that.setState({
                    judge_config: rel.data
                });
            },
            error: function (rel, msg) {
                that.hideProcessingDimmer();
                $(that.refs.ErrorDimmer).dimmer("show");
            }
        }).call();
    }

    componentDidMount() {
        var that = this;
        this.getJudgeConfig();
        $(this.refs.NavList).find(".item").tab({
            history: true,
            onLoad: function () {
                var tab_name = $(this).attr("data-tab") ;
                if(tab_name === 'modify_problem'){
                    if(that.init_problem_editor) {
                        return false;
                    }
                    that.refs.problem_editor.modifyProblem();
                    that.init_problem_editor = true;

                } else if(tab_name === 'judge_config'){

                }else if (tab_name === 'code_config') {
                }else if (tab_name === 'test_cases') {
                }
            }
        });
    }
    changeLang(event){
        this.setState({lang_selected: event.target.value});
    }
    toggleJudge(){
        var that = this;
        this.showProcessingDimmer();
        core.restful({
            method: 'POST',
            responseType: "json",
            url: that.props.apis.toggle_judge,
            success: function (rel) {
                that.hideProcessingDimmer();
            },
            error: function (rel, msg) {
                that.hideProcessingDimmer();
                that.refs.alertbox.showError(rel, msg);
            }
        }).call();
    }

    render(){
        var lang_options = this.LangList.map((val, key) => {
            return (
                <option key={key} value={val[0]}>{val[1]}</option>
            )
        });
        return (
            <div className="ui">
                <div className="ui menu stackable" ref="NavList">
                    <a className="active item" data-tab="modify_problem">
                        <i className="edit icon"></i>
                        题目
                    </a>
                    <a className="item" data-tab="judge_config">
                        <i className="settings icon"></i>
                        评测
                    </a>
                    <a className="item" data-tab="code_config">
                        <i className="code icon"></i>
                        代码
                    </a>
                    <a className="item" data-tab="test_cases">
                        <i className="sitemap icon"></i>
                        数据
                    </a>

                    <div className="item">
                        <core.forms.SelectField inline forceDefault onchange={this.changeLang} value={this.state.lang_selected}>
                            <option value="0" disabled>执行切换语言操作，未保存的更改将要丢失</option>
                            {lang_options}
                        </core.forms.SelectField>
                    </div>
                    <div className="right menu">
                        <div className="item" title="题目内容查看">
                            {(this.state.judge_config.permission & 1) === 0 ? <i className="lock icon"></i>: <i className="checkmark icon"></i>}
                            访问
                        </div>
                        <div className="item" title="提交评测">
                            {(this.state.judge_config.permission & 2) === 0 ? <i className="lock icon"></i>: <i className="checkmark icon"></i>}
                            评测
                        </div>
                        <div className="item" title="对外数据访问权限">
                            {(this.state.judge_config.permission & 4) === 0 ? <i className="lock icon"></i>: <i className="checkmark icon"></i>}
                            数据
                        </div>
                        <div className="item" title="对外管理权限">
                            {(this.state.judge_config.permission & 8) === 0 ? <i className="lock icon"></i>: <i className="checkmark icon"></i>}
                            管理
                        </div>
                        <div className="item">
                            <core.forms.CheckBoxField
                                inline
                                type="toggle"
                                label="评测"
                                checked={this.state.judge_config.pause_judge===false}
                                value="true"
                                name="start_judge"
                                onchange={this.toggleJudge}
                            />
                        </div>
                    </div>
                </div>
                <div className="ui segment">
                    <div className="ui inverted dimmer" ref="ProcessingDimmer">
                        <div className="ui text loader">
                            <div className="ui text">处理中...</div><br /><br />
                        </div>
                    </div>
                    <div className="ui inverted dimmer" ref="ErrorDimmer">
                        <h2 className="ui icon header">
                            <i className="remove icon"></i>
                        </h2>
                        <div className="ui text">加载评测设置失败，请刷新页面重试</div><br /><br />
                    </div>
                    <div className="ui ">
                        <div className="ui tab active" data-tab="modify_problem">
                            <ProblemEditor
                                apis={{
                                    modify: this.props.apis.modify_problem,
                                    problem_info: this.props.apis.problem_info
                                }}
                                ref="problem_editor"
                            />
                        </div>
                        <div className="ui tab" data-tab="judge_config">
                            <JudgeConfigManager
                                judge_config={this.state.judge_config}
                                judge_config_update={this.state.judge_config_update}
                                save={this.props.apis.save_judge_config}
                                spj_judger={this.props.apis.upload_spj_judger}
                                manager={this}
                            />
                        </div>
                        <div className="ui tab" data-tab="test_cases">
                            <TestCaseManager
                                judge_config={this.state.judge_config}
                                judge_config_update={this.state.judge_config_update}
                                lang={this.state.lang_selected}
                                save_settings={this.props.apis.save_test_cases_settings}
                                get_data={this.props.apis.get_test_cases_data}
                                save_data={this.props.apis.save_test_cases_data}
                                upload_data={this.props.apis.upload_test_cases_data}
                                tcmaker_run={this.props.apis.tcmaker_run}
                                tcmaker_hisotory={this.props.apis.tcmaker_hisotory}
                                manager={this}
                                remove={this.props.apis.remove_test_cases}
                            />
                        </div>
                        <div className="ui tab" data-tab="code_config">
                            {(this.state.problem_type === 1) ?
                                <DemoCaseManager
                                    judge_config={this.state.judge_config}
                                    judge_config_update={this.state.judge_config_update}
                                    lang={this.state.lang_selected}
                                    manager={this}
                                    save_data={this.props.apis.save_demo_cases_settings}
                                    save_code={this.props.apis.save_demo_cases_code}
                                    remove={this.props.apis.remove_demo_cases}
                                />
                            :
                                <AnswerCaseManager
                                    judge_config={this.state.judge_config}
                                    judge_config_update={this.state.judge_config_update}
                                    lang={this.state.lang_selected}
                                    save={this.props.apis.save_answer_case}
                                    manager={this}
                                />
                            }
                        </div>
                    </div>
                </div>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="" />
            </div>
        );
    }
}
