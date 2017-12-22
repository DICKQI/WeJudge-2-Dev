/**
 * Created by lancelrq on 2017/3/2.
 */

module.exports = DemoCaseManager;

var React = require('react');
var core = require('wejudge-core');
var FormManagerBase = require("./manager").FormManagerBase;
var DemoCaseEditor = require('./module/DemoCaseEditor');


class DemoCaseManager extends FormManagerBase {

    constructor(props) {
        super(props);
        // 初始状态
        this.manager = props.manager;
        this.apis = {
            submit: props.save_code
        };
        this.state['addable'] = true;
        this.insertHandle = this.insertHandle.bind(this);
        this.doModify = this.doModify.bind(this);
        this.doCreate = this.doCreate.bind(this);
    }

    insertHandle(handle){
        var that = this;
        return function () {
            that.refs.DemoCode.appendToCursor("/***## " + handle + " ##***/");
        }
    }

    doModify(entity){
        var that = this;
        var dclist = (this.state.lang && this.state.judge_config.demo_answer_cases) && (this.state.judge_config.demo_answer_cases[this.state.lang] || []);
        var code = dclist[entity.handle];
        return function () {
            that.refs.editor.show(entity, code);
        }
    }

    doCreate(){
        var that = this;
        if(this.adding) return;
        this.adding = true;
        var core = require('wejudge-core');
        core.restful({
            method: 'POST',
            responseType: "json",
            url: that.props.save_data,
            data: {
                is_new: true,
                lang: this.state.lang
            },
            success: function (rel) {
                that.adding = false;
                that.manager.getJudgeConfig();
            },
            error: function (rel, msg) {
                that.adding = false;
                that.refs.alertbox.showError(rel, msg);
            }
        }).call();
    }
    removeDemoCase(entity){
        var that = this;
        return function () {
            that.refs.RMDCCfm.show(function (rel) {
                if(rel){
                    that.doRemove(entity.handle);
                }
            })
        }
    }
    doRemove(handle){
        var that = this;
        if(this.removing) return;
        this.removing = true;
        var core = require('wejudge-core');
        core.restful({
            method: 'POST',
            responseType: "json",
            url: that.props.remove,
            data: {
                lang: this.state.lang,
                handle: handle
            },
            success: function (rel) {
                that.removing = false;
                that.manager.getJudgeConfig();
            },
            error: function (rel, msg) {
                that.removing = false;
                that.refs.alertbox.showError(rel, msg);
            }
        }).call();
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.getJudgeConfig();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    render(){
        var dclist = (this.state.lang && this.state.judge_config.demo_cases) && (this.state.judge_config.demo_cases[this.state.lang] || []);
        var demoCaseList = dclist ? dclist.map((val, key)=> {
            return (
                <tr key={key}>
                    <td>
                        <a onClick={this.doModify(val)}>{val.name}</a>
                    </td>
                    <td>{val.handle}</td>
                    <td>
                        <a className="ui basic red tiny button" onClick={this.removeDemoCase(val)}><i className="remove icon"></i> 删除</a>
                        <a className="ui basic blue tiny button" onClick={this.insertHandle(val.handle)}><i className="arrow right icon"></i> 插入到代码</a>
                    </td>
                </tr>
            )
        }): "";
        console.log((this.state.judge_config.demo_code_cases && this.state.judge_config.demo_code_cases[this.state.lang]));
        var form_area = this.renderForm(
            <div className="ui two columns stackable grid">
                <div className="column">
                    <div className="ui">
                        <a className="ui green button" onClick={this.doCreate}>
                            <i className="add icon"></i>
                            添加填空区
                        </a>
                        <table className="ui stackable table">
                            <thead>
                            <tr>
                                <th>名称</th>
                                <th>标识符</th>
                                <th>操作</th>
                            </tr>
                            </thead>
                            <tbody>
                            {demoCaseList}
                            </tbody>
                        </table>
                        <i className="info circle icon"></i> 请不要插入多个相同的区域以保证该代码能够正常编译运行
                        <br />
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
                        <button className="ui primary button">
                            <i className="save icon"></i>
                            保存代码和设置
                        </button>
                    </div>
                </div>
                <div className="column">
                    <h4>填空模板代码</h4>
                    <div className="ui divider"></div>
                    <core.forms.CodeMirrorField name="code" ref="DemoCode"
                        lang={this.state.lang} value={(this.state.judge_config.demo_code_cases && this.state.judge_config.demo_code_cases[this.state.lang]) || ""}
                    />
                    <input type="hidden" name="lang" value={this.state.lang}/>
                </div>
            </div>
        );
        return (
            <div className="ui">
                {form_area}
                <DemoCaseEditor ref="editor" lang={this.state.lang}
                    apis={{submit: this.props.save_data}}
                    manager={this.manager}
                />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="你确定要删除这条填空用例吗，用例答案内容将被永久删除不可找回！" msg_title="操作确认" ref="RMDCCfm" />
            </div>
        );
    }

}

// <div className="column" key={key}>
//     <div className="ui card">
//         <div className="content">
//             <a className="right floated" onClick={this.removeDemoCase(val)}><i className="remove icon"></i></a>
//             <div className="header">
//                 {val.name} <a onClick={this.doModify(val)}><i className="edit icon"></i></a>
//             </div>
//             <div className="description">标识符：{val.handle}</div>
//         </div>
//         <div className="extra content">
//             <a className="left floated" onClick={this.insertHandle(val.handle)}><i className="arrow right icon"></i>插入到代码</a>
//         </div>
//     </div>
// </div>