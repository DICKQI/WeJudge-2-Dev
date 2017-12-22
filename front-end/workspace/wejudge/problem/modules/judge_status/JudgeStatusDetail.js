/**
 * Created by lancelrq on 2017/3/27.
 */

var React = require("react");
var core = require("wejudge-core");


module.exports = JudgeStatusDetail;

class JudgeStatusDetail extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.result
        };
    }

    componentDidMount() {
        this.getData();
    }

    componentDidUpdate() {
        var that = this;
        $(this.refs.NavList).find(".item").tab({
            onLoad: function () {
                var tab_name = $(this).attr("data-tab") ;
                if(tab_name === 'code'){

                }else{
                    try {
                        var base = difflib.stringAsLines(that.refs["tdoutArea_" + tab_name].value);
                        var newtxt = difflib.stringAsLines(that.refs["tdoutdataArea_" + tab_name].value);
                        var sm = new difflib.SequenceMatcher(base, newtxt);
                        $(that.refs["differContianer_" + tab_name]).html(diffview.buildView({
                            baseTextLines: base,
                            newTextLines: newtxt,
                            opcodes: sm.get_opcodes(),
                            // set the display titles for each resource
                            baseTextName: "参考答案",
                            newTextName: "程序输出",
                            contextSize: 2,
                            viewType: 0
                        }));
                    }catch(e){}
                }
            }
        });
    }

    getTestCaseDetail(details, handle){
        for(var idx in details){
            if(details[idx].handle === handle){
                return details[idx]
            }
        }
        return null;
    }
    getJudgeExitCodeColor(desc, exitcode){
        if(desc===undefined || exitcode===undefined ) return "";
        var dd = desc[exitcode];
        return dd.color;
    }
    getJudgeText(desc, exitcode){
        if(desc===undefined  || exitcode===undefined ) return "";
        var dd = desc[exitcode];
        return dd.title + " (" + dd.en + ")";
    }


    renderBody() {
        var result = this.state.data.result || {};
        var lang= this.state.data.lang || 1;
        var config= this.state.data.config || {};
        var desc = this.state.data.desc;
        var langs_call = this.state.data.langs_call;
        var result_detail = this.state.data.result_detail || {};
        if(config.test_cases){
            config.test_cases.sort(function (a, b) {
                return a.order > b.order;
            })
        }
        return (
            <div className="ui">
                <div className="ui stackable grid">
                    <div className="three wide column">
                        <div className="ui secondary vertical pointing menu" ref="NavList">
                            <a className="active item" data-tab="code">评测结果</a>
                            {config.test_cases && config.test_cases.map((val, key) => {
                                return <a key={key}className="item" data-tab={val.handle}>{val.name}</a>
                            })}
                        </div>
                    </div>
                    <div className="thirteen wide column">
                        <div className={"ui "+this.getJudgeExitCodeColor(desc, result.exitcode)+" active segment tab"} data-tab="code">
                            <h3 className={"ui "+this.getJudgeExitCodeColor(desc, result.exitcode)+" header"}>
                                {this.getJudgeText(desc, result.exitcode)}
                                <small className="sub header">
                                    评测语言：{langs_call && langs_call[lang]}
                                    ，最长运行时间：{result.exitcode === 2 ? "---" : result.timeused}ms
                                    ，最大内存使用：{result.exitcode === 3 ? "---" : result.memused}KB

                                </small>
                            </h3>
                            {
                                result.ceinfo !== "" ?
                                <div className="ui error message">
                                    <div className="header">编译器信息</div>
                                    <code><pre>{result.ceinfo}</pre></code>
                                </div>
                                : null
                            }
                            <core.forms.CodeMirrorField lang={lang} value={result.finally_code || ""} />
                        </div>
                        {config.test_cases && config.test_cases.map((val, key) => {
                            var detail = this.getTestCaseDetail(result.details, val.handle);
                            if(!detail)
                                return (
                                    <div className="ui grey segment tab" key={key} data-tab={val.handle}>
                                        测试数据未能运行、输出，或因过期已被清理
                                    </div>
                                );
                            else {
                                var rd = {};
                                if(detail)
                                    rd = result_detail[val.handle];
                                return (
                                    <div className={"ui "+this.getJudgeExitCodeColor(desc, detail.judge_result)+" segment tab"}
                                        key={key} data-tab={val.handle}>
                                        <h3 className={"ui "+ this.getJudgeExitCodeColor(desc, detail.judge_result) +" header"}>
                                            {this.getJudgeText(desc, detail.judge_result)}
                                            <small className="sub header">
                                                最长运行时间：{detail.judge_result === 2 ? "---" : detail.time_used }ms，
                                                最大内存使用：{detail.judge_result === 3 ? "---" : detail.memory_used }KB
                                                {/*{detail.judge_result === 4 ? `，正确行数：${detail.same_lines}/${detail.total_lines}行` : null}*/}
                                                {
                                                    (detail.judge_result === 2 || detail.judge_result === 3 ||
                                                        detail.judge_result === 5 || detail.judge_result === 6 ) ?
                                                            <span>，Linux内核信号({ detail.signal }）描述：{ detail.signal_desc }</span>
                                                        : null
                                                }
                                            </small>
                                        </h3>
                                        {
                                            detail.re_msg !== "" ?
                                                <div className="ui error message">
                                                    <div className="header">运行时错误信息</div>
                                                    <code><pre>{detail.re_msg}</pre></code>
                                                </div>
                                                : null
                                        }
                                        {(rd && rd !== -1 && rd !== -2) ?
                                            <div className="ui grid">
                                                <div className="five wide column">
                                                    <core.forms.CodeMirrorField lang={0} value={
                                                        rd.indata === -1 ? "数据大于100K，请使用二进制比较工具" :
                                                        rd.indata === -2 ? "数据不存在、未生成或者被清理" : rd.indata
                                                    }/>
                                                </div>
                                                <div className="eleven wide column">
                                                    <div className="diff-cp-contianer">
                                                        <div ref={"differContianer_" + val.handle}></div>
                                                    </div>
                                                    <textarea style={{display:"none"}} ref={"tdoutArea_" + val.handle}
                                                              readOnly value={
                                                                rd.outdata === -1 ? "数据大于100K，请使用二进制比较工具" :
                                                                rd.outdata === -2 ? "数据不存在、未生成或者被清理" : rd.outdata
                                                              }></textarea>
                                                    <textarea style={{display:"none"}}
                                                              ref={"tdoutdataArea_" + val.handle} readOnly
                                                              value={
                                                                rd.userdata === -1 ? "数据大于100K，请使用二进制比较工具" :
                                                                rd.userdata === -2 ? "数据不存在、未生成或者被清理" : rd.userdata
                                                              }></textarea>
                                                </div>
                                            </div>
                                            :
                                            <div>
                                                {rd === -1 ? "测试数据已被屏蔽" : "测试数据项目被删除或者不存在"}
                                            </div>
                                        }
                                    </div>
                                );
                            }
                        })}
                    </div>
                </div>
            </div>
        );
    }
}
