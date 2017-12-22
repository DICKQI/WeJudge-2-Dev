/**
 * Created by lancelrq on 2017/3/2.
 */

module.exports = AnswerCaseManager;

var React = require('react');
var core = require('wejudge-core');
var moment = require("moment");

var FormManagerBase = require("./manager").FormManagerBase;


class AnswerCaseManager extends FormManagerBase {

    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.apis = {
            submit: props.save
        };
    }

    formatTimeLimit(value){
        return (value / 1000).toFixed(1) + " S"
    }

    formatMemoryLimit(value){
        return (value / 1024).toFixed(0) + " MB"
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.getJudgeConfig();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.alertbox.showError(rel, msg);
    }

    render(){
        var formBody = this.renderForm((
            <div className="ui two columns stackable grid">
                <div className="column">
                    <h4>评测限制</h4>
                    <div className="ui divider"></div>
                    <core.forms.RangeField
                        label="最大可用时间" min={1000} max={30000} width="50%"
                        value={this.state.judge_config.time_limit ? this.state.judge_config.time_limit[""+this.state.lang] : 1000}
                        step={100} format={this.formatTimeLimit}
                        name="time_limit" label_value
                    />
                    <core.forms.RangeField
                        label="最大可用内存" min={32768} max={524288} width="50%"
                        value={this.state.judge_config.mem_limit ? this.state.judge_config.mem_limit[""+this.state.lang] : 1000}
                        step={1024} format={this.formatMemoryLimit}
                        name="mem_limit" label_value
                    />
                    <br />
                    <button className="ui primary button">
                        <i className="save icon"></i>
                        保存代码和设置
                    </button>
                </div>
                <div className="column">
                    <h4>示例代码</h4>
                    <core.forms.CodeMirrorField
                        name="code"
                        lang={this.state.lang}
                        value={this.state.judge_config.answer_cases ? (this.state.judge_config.answer_cases[this.state.lang.toString()] || "") : ""} />
                    <input type="hidden" name="lang" value={this.state.lang}/>
                </div>
            </div>
        ));
        return (
            <div className="ui">
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="" />
            </div>
        )
    }
}