/**
* Created by lancelrq on 2017/2/15.
*/

module.exports = SubmitCode;

var React = require('react');
var ReactDom = require('react-dom');
var core = require('wejudge-core');
var DraftsBox = require("./DraftsBox");

class SubmitCode extends core.forms.FormComponent{
    constructor(props) {
        super(props);
        this.apis = {
            submit: props.apis.submit
        };
        this.state = {
            config: props.judge_config,
            problem: props.problem,
            lang: 0
        };
        this.LANGEUAGE = this.LangList = [
            [1, "C语言 (GNU C)", "text/x-csrc"],
            [2, "C++ (GNU CPP)", "text/x-c++src"],
            [4, "Java 1.8", "text/x-java"],
            [8, "Python 2.7", "text/x-python"],
            [16, "Python 3.5", "text/x-python"]
        ];
        var problem = this.state.problem;
        this.LangList = [];
        if(problem.lang > 0) {
            for (var i = 0 ; i < this.LANGEUAGE.length; i++){
                var val = this.LANGEUAGE[i];
                if ((val[0] & problem.lang) > 0)
                {
                    this.LangList.push(val);
                }
            }
        }else{
            this.LangList = this.LANGEUAGE;
        }
        this.state['lang'] = this.LangList[0][0];
        this.STATUS_FLAG_DESC = {
            0: ["评测通过", "Accepted", "恭喜，评测成功通过！", "green"],
            1: ["格式错误", "Presentation Error", "请检查程序输出答案的格式", "yellow"],
            2: ["超过时间限制", "Time Limit Exceeded", "请检查程序是否陷入死循环或者算法没有在限定的时间内完成", "red"],
            3: ["超过内存限制", "Memory Limit Exceeded", "请检查程序是否消耗了大量的内存没有释放", "red"],
            4: ["答案错误", "Wrong Answer", "请检查程序是否符合题目要求", "red"],
            5: ["运行时错误", "Runtime Error", "请检查程序是否存在递归未退出、除数为0、数组越界等情况", "red"],
            6: ["输出内容超限", "Output Limit Exceeded", "输出内容超过正确答案的2倍以上，建议你去除与答案无关的输出内容", "red"],
            7: ["编译失败", "Compile Error", "请先完善程序，或者是通过评测机报告检查是否存在引用本系统不支持的库", "blue"],
            8: ["系统错误", "System Error", "请与管理员联系", "red"],
            10: ["特殊评测超时", "SPJudger Timeout", "请与出题人联系", "red"],
            11: ["特殊评测错误", "SPJudger Error", "请与出题人联系", "red"]
        };
        this.changeLang = this.changeLang.bind(this);
        this.hideJudgeDimmer = this.hideJudgeDimmer.bind(this);
        this.showJudgeDimmer = this.showJudgeDimmer.bind(this);
        this.indentCode = this.indentCode.bind(this);
        this.saveDraft = this.saveDraft.bind(this);
        this.restoreDraft = this.restoreDraft.bind(this);
    }

    componentDidMount() {
        var that = this;
        if(this.state.config.judge_type === 0){
            $(this.refs.func_reset).click(function () {
                if(confirm("你确定要重置编辑器吗？代码将会被清空！")){
                    that.refs.code_area.setValue("");
                }
            }).popup({
                position: 'bottom center'
            });
        }else{
            $('pre').each(function(i, block) {
                hljs.highlightBlock(block);
            });
            $(that.refs.CODENAV).find(".item").tab();
        }
        this.refs.drafts_box.load();
    }

    doSubmitSuccess(rel){
        this.showJudgeDimmer();
        var that = this;
        var dat = rel.data;
        that.status_id = dat.sid;
        setTimeout(function () {
            that.receiveJudgeResult(that);
        }, 1000);
    }

    doSubmitFailed(rel, msg){
        if(rel.errcode !== 1010 && rel.errcode !== 3010 && rel.errcode !== 5010)
            this.refs.alertbox.showError(rel, msg);
    }

    showJudgeDimmer(){
        var $dimmer = $(this.refs.JudgingDimmer);
        $dimmer.dimmer("show");
    }
    hideJudgeDimmer(){
        var $dimmer = $(this.refs.JudgingDimmer);
        $dimmer.dimmer("hide");
    }

    indentCode(){
        var that = this;
        var codes = this.refs.code_area.getValue();
        if(!codes) return;
        core.restful({
            method: "POST",
            data:{
                code: codes
            },
            url: this.props.apis.indent_code,
            responseType: "json",
            success: function (rel) {
                that.refs.code_area.setValue(rel.data);
            }
        }).call();
    }

    receiveJudgeResult(that){
        core.restful({
            method: "POST",
            url: that.props.apis.rolling.replace("status/0", "status/" + that.status_id),
            responseType: "json",
            success: function (rel) {
                var flag = rel.data.flag;
                if (flag >= 0) {
                    var s = that.STATUS_FLAG_DESC[flag];
                    if(flag === 1 && !that.state.config.strict_mode) {
                        $(that.refs.result_title).text("数据通过(DA)");
                        $(that.refs.result_desc).text("但是呢，建议你检查一下程序输出答案的格式，比如是否多了空格换行等。把它做得更完美吧！");
                        $(that.refs.result_en_title).text("Data Accepted");
                    } else {
                        $(that.refs.result_title).text(s[0]);
                        $(that.refs.result_desc).text(s[2]);
                        $(that.refs.result_en_title).text(s[1]);
                    }

                    $(that.refs.result_tips).removeClass().addClass("ui " + s[3] + " header");

                    that.refs.ResultDialog.show(function () {
                            window.open(that.props.urls.view_detail.replace("status/0", "status/" + that.status_id));
                            that.hideJudgeDimmer();
                        }, function () {
                            that.hideJudgeDimmer();
                        }
                    );
                }else{
                    setTimeout(function () {
                        that.receiveJudgeResult(that)
                    }, 1000);
                }
            }
        }).call();
    }

    changeLang(event){
        this.setState({lang: parseInt(event.target.value)});
    }

    saveDraft(){
        if(this.submitting) return false;
        this.submitting = true;
        var that = this;
        that.refs.FormMessager.hide();
        that.refs.ProcessingDimmer.show();
        core.restful({
            method: 'POST',
            responseType: "json",
            url: that.props.apis.save_draft,
            success: function (rel) {
                that.submitting = false;
                that.refs.ProcessingDimmer.hide();
                that.refs.alertbox.showSuccess(rel, function () {
                    that.refs.drafts_box.load();
                });
            },
            error: function (rel, msg) {
                that.submitting = false;
                that.refs.ProcessingDimmer.hide();
                that.refs.alertbox.showError(rel, msg);
            }
        }).submit_form(this.refs.MainForm);
        return false;
    }

    restoreDraft(draft){
        var that = this;
        return function () {
            if(draft.lang !== that.state.lang){
                alert("请先切换到您选择的这份草稿对应的编程语言，才能恢复数据。");
                return false;
            }
            /// 恢复草稿信息
            if(that.state.config.judge_type === 1){
                var demo_cases = that.state.config.demo_cases[that.state.lang] || [];
                var codes = {};
                try{
                    codes = JSON.parse(draft.content);
                }catch(ex){
                    codes = {}
                }
                for(var i = 0; i < demo_cases.length; i++){
                    var handle = demo_cases[i].handle;
                    that.refs['code_area_' + handle].setValue(codes[handle]);
                }
            }else{
                that.refs.code_area.setValue(draft.content);
            }
        }
    }

    render(){
        var formBody;
        if(this.state.config.judge_type === 1){
            var demo_cases = this.state.config.demo_cases[this.state.lang] || [];
            var demo_code = this.state.config.demo_code_cases[this.state.lang] || "";
            var find_democases = function(handle) {
                for(var i = 0; i < demo_cases.length; i++){
                    if(demo_cases[i].handle === handle) return demo_cases[i];
                }
            };
            var area_list = [];
            var len = demo_code.length;
            var sw = true;
            var left_str;
            var right_str = demo_code;
            while(true){
                var ep;
                if(sw){
                    ep = demo_code.indexOf("/***##");
                    left_str = demo_code.substring(0, ep);
                    right_str = demo_code.substring(ep, demo_code.length);
                }else{
                    ep = demo_code.indexOf("##***/");
                    left_str = demo_code.substring(0, ep+6);
                    right_str = demo_code.substring(ep+6, demo_code.length);
                }
                if(ep === -1){
                    break;
                }
                sw = !sw; // switch;
                demo_code = right_str;
                area_list.push(left_str);
            }
            area_list.push(right_str);

            var code_handles = [];

            formBody = this.renderForm(
                <section>
                    <div className="ui two column grid">
                        <div className="column">
                            <core.forms.SelectField inline forceDefault onchange={this.changeLang} value={this.state.lang}>
                                <option value="0" disabled>执行切换语言操作，编辑器将被清空！</option>
                                {this.LangList.map((val, key) => {
                                    return (
                                        <option key={key} value={val[0]}>{val[1]}</option>
                                    );
                                })}
                            </core.forms.SelectField>
                        </div>
                        <div className="right aligned column">
                            <div className="ui compact menu" ref="CODENAV">
                                <span className="item" data-tab="code_area_submit_tab">编辑器模式</span>
                                <span className="item" data-tab="code_area_view_tab">代码模板</span>
                            </div>
                        </div>
                    </div>
                    {(area_list && area_list.length >= 2) ? (
                    <div className="ui">
                        <br />
                        <div className="ui secondary segment">
                            <div className="ui active tab" data-tab="code_area_submit_tab">
                                {area_list.map((val, key) => {
                                    if(val.indexOf("/***##") !== -1){
                                        var handle = val.replace(/\/\*\*\*\#\# (\w*) \#\#\*\*\*\//, "$1");
                                        code_handles.push(handle);
                                        return <core.forms.CodeMirrorField no_margin ref={"code_area_"+ handle }
                                              key={key} name={"code_"+ handle } lang={this.state.lang}
                                        />;
                                    }else{
                                        return <pre style={{padding: 0, margin: 0, background: "transparent"}} key={key}>{val}</pre>;
                                    }
                                })}
                            </div>
                            <div className="ui tab" data-tab="code_area_view_tab">
                                {area_list.map((val, key) => {
                                    if(val.indexOf("/***##") !== -1){
                                        var handle = val.replace(/\/\*\*\*\#\# (\w*) \#\#\*\*\*\//, "$1");
                                        var dc = find_democases(handle);
                                        var c = '/* 代码填空：请在下方输入你的代码(相关描述：' + dc.name +') */\n\n\n/* 代码填空结束 */';
                                        return <pre style={{padding: 0, margin: 0, background: "transparent"}} key={key}>{c}</pre>;
                                    }else{
                                        return <pre style={{padding: 0, margin: 0, background: "transparent"}} key={key}>{val}</pre>;
                                    }
                                })}
                            </div>
                            <br />
                        </div>
                        <input type="hidden" name="handles" value={code_handles.join(",")}/>
                        <input type="hidden" name="lang" value={this.state.lang}/>
                        <input type="hidden" name="user_id" value={this.props.user_id}/>
                        <button className="ui blue button"><i className="cloud upload icon"></i> 提交评测</button>
                        <a onClick={this.saveDraft} className="ui button"><i className="save icon"></i> 保存草稿</a>

                    </div>
                    ) : (
                        <div className="ui icon message">
                            <i className="warning circle icon"></i>
                            <div className="content">
                                <p>当前题目没有设置可用的代码模板，无法提交</p>
                            </div>
                        </div>
                    )}
                </section>
            )
        } else {
            formBody = this.renderForm(
                <section>
                    <div className="inline fields">
                        <core.forms.SelectField inline forceDefault onchange={this.changeLang} value={this.state.lang}>
                            <option value="0" disabled>执行切换语言操作，编辑器将被清空！</option>
                            {this.LangList.map((val, key) => {
                                return (
                                    <option key={key} value={val[0]}>{val[1]}</option>
                                );
                            })}
                        </core.forms.SelectField>
                        <a className="ui icon button" ref="func_reset" data-content="重置编辑器"><i className="refresh icon"></i></a>
                        <a className={`ui icon blue ${this.state.lang === 1 || this.state.lang === 2 ? "" : "disabled"} button`}
                           ref="func_format"
                           data-content="格式化代码"
                           onClick={this.indentCode}
                        >
                            <i className="code icon"></i>
                        </a>
                    </div>
                    <core.forms.CodeMirrorField ref="code_area" name="code" lang={this.state.lang}  />
                    <input type="hidden" name="lang" value={this.state.lang}/>
                    <input type="hidden" name="user_id" value={this.props.user_id}/>
                    <button className="ui blue button"><i className="cloud upload icon"></i> 提交评测</button>
                    <a onClick={this.saveDraft} className="ui button"><i className="save icon"></i> 保存草稿</a>
                </section>
            );
        }
        return (
            <div className="ui segment">
                <div className="ui stackable grid">
                    <div className="twelve wide column">
                        <div className="ui inverted dimmer" ref="JudgingDimmer">
                            <div className="ui text loader semantic">
                                <div className="ui text" id="JudgingTips">评测中...</div><br /><br />
                                <div className="ui text"><a href="javascript:void(0)" onClick={this.hideJudgeDimmer}>返回编辑器</a></div>
                            </div>
                        </div>
                        {formBody}
                        <div>
                            <core.dialog.Dialog ref="ResultDialog" title="评测结果" btnTitle="查看评测详情" size="small">
                                <div style={{textAlign: "center"}}>
                                    <h1 className="ui text" ref="result_tips">
                                        <div  ref="result_title"></div>
                                        <small className="ui text" ref="result_en_title">评测通过</small>
                                    </h1>
                                    <p className="ui text" ref="result_desc">评测通过</p>
                                </div>
                            </core.dialog.Dialog>
                            <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="" />
                            <core.dialog.Confirm ref="confirm" msg_title="" msg="" />
                        </div>
                    </div>
                    <div className="four wide column">
                        <h3>草稿箱</h3>
                        <div className="ui hidden divider"></div>
                        <DraftsBox
                            ref="drafts_box"
                            get_darfts={this.props.apis.get_drafts}
                            restore={this.restoreDraft}
                        />
                    </div>
                </div>
                <div className="ui message">
                    <i className="warning sign icon"></i>由于存在浏览器崩溃、误操作（如意外刷新页面）等不可抗拒因素，不建议直接使用在线编辑器写代码！
                    <br />
                    <i className="warning circle icon"></i>草稿箱对于同一用户同一题目，只能保留历史3条记录，超过的将自动删除
                </div>
            </div>
        )
    }
}

