/**
 * Created by lancelrq on 2017/7/6.
 */

var React = require("react");
var moment = require("moment");
var core = require("wejudge-core");


module.exports = AsgnAnswer;

class AsgnAnswer extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.get_answer
        };
        this.state['lang'] = 1;
        this.load = this.load.bind(this);
        this.changeLang = this.changeLang.bind(this);
        this.LangList = [
            [1, "C语言 (GNU C)", "text/x-csrc"],
            [2, "C++ (GNU CPP)", "text/x-c++src"],
            [4, "Java 1.8", "text/x-java"],
            [8, "Python 2.7", "text/x-python"],
            [16, "Python 3.5", "text/x-python"]
        ];
    }

    load(){
        var that = this;
        this.getData(null, function(rel){
            $(that.refs.ProblemAnswers).find('.item').tab({
                onVisible: function () {
                    try {
                        that.refs["codemirror_" + $(this).attr('data-id') + "_" + that.state.lang].refresh();
                    }catch (ex){}
                }
            });
            $(that.refs.StudentAnswers).find('.item').tab({
                onVisible: function () {
                    try {
                        that.refs["ua_codemirror_" + $(this).attr('data-id')].refresh();
                    }catch (ex){}
                }
            });
        });
    }
    changeLang(event){
        this.setState({lang: event.target.value});
    }

    renderBody() {
        var problems = this.state.data.problems;
        var problems_codes = this.state.data.problems_codes;
        var reports_codes = this.state.data.reports_codes;
        var that = this;
        var lang = this.state.lang;
        if(this.state.data)
            return this.state.data.status === "ok"  ? (
                <div className="ui">
                    <div className="ui stackable grid">
                        <div className="four wide column">
                            <div ref="ProblemAnswers" className="ui vertical fluid tabular menu">
                                {problems_codes && problems_codes.map(function(val, index){
                                    return <a className={`${index==0?"active ":""}item`} data-tab={`aw_problem_${val.id}`} key={index}>
                                        {core.tools.gen_problem_index(problems[val.id].index)}.{problems[val.id].entity.title}
                                    </a>
                                })}
                            </div>
                        </div>
                        <div className="twelve wide column">
                            <core.forms.SelectField inline forceDefault onchange={this.changeLang} value={this.state.lang}>
                                {this.LangList.map((val, key) => {
                                    return (
                                        <option key={key} value={val[0]}>{val[1]}</option>
                                    );
                                })}
                            </core.forms.SelectField>
                            {problems_codes && problems_codes.map(function(val, index) {
                                var data = val.datas;
                                var code = "";
                                if (data.judge_type == 0) {
                                    code = data.answer_cases[lang] || "暂无代码";
                                }else if (data.judge_type == 1){
                                    if (data.demo_code_cases[lang] == undefined || data.demo_cases[lang] == undefined || data.demo_answer_cases[lang]== undefined){
                                        code = "暂无代码"
                                    }else {
                                        code = data.demo_code_cases[lang];
                                        var demo_answer_cases = data.demo_answer_cases[lang];
                                        data.demo_cases[lang].map(function (val, key) {
                                            var handle = val.handle;
                                            code = code.replace("/***## " + handle + " ##***/", demo_answer_cases[handle])
                                        })
                                    }
                                }
                                return <div className={`ui ${index==0?"active ":""}tab segment`}
                                            data-tab={`aw_problem_${val.id}`} data-id={val.id}  key={index}
                                            style={{padding: "0"}}
                                >
                                    <core.forms.CodeMirrorField ref={`codemirror_${val.id}_${lang}`} lang={lang} value={code} />
                                </div>
                            })}
                        </div>
                    </div>

                    {reports_codes && reports_codes.length > 0 ?
                        <div>
                            <h3>优秀学生代码</h3>
                            <div className="ui divider"></div>
                            <div className="ui stackable grid">
                                <div className="four wide column">
                                    <div className="ui vertical fluid tabular menu" ref="StudentAnswers">
                                        {reports_codes && reports_codes.map(function (val, index) {
                                            return <a className={`${index===0?"active ":""}item`} data-tab={`us_code_${val.author.id}`} key={index}>
                                                {val.author.realname}({val.author.username})
                                            </a>
                                        })}
                                    </div>
                                </div>
                                <div className="twelve wide column">
                                    <div className="ui">
                                        {reports_codes && reports_codes.map(function (val, index) {
                                            return <div className={`ui ${index===0?"active ":""}tab`}
                                                        data-tab={`us_code_${val.author.id}`}  key={index}
                                            >
                                                {val.judge_status && val.judge_status.map(function (val2, index2) {
                                                    return <div key={index2} className="ui fluid card">
                                                        <core.forms.CodeMirrorField  ref={`ua_codemirror_${val2.id}`}  lang={val2.lang} value={val2.finally_code} />
                                                        <div className="content">
                                                            <div className="header">#{val2.id} @ {core.tools.gen_problem_index(problems[val2.virtual_problem_id].index)}. {problems[val2.virtual_problem_id].entity.title}</div>
                                                            <div className="description">
                                                                <strong>最大运行时间：</strong>{val2.exe_time} ms，<strong>最大内存占用：</strong>{val2.exe_mem} KB，<strong>代码长度：</strong>{val2.code_len} Byte
                                                            </div>
                                                        </div>

                                                    </div>
                                                })}
                                            </div>
                                        })}
                                    </div>
                                </div>
                            </div>
                        </div>
                    : null
                    }
                </div>
            ) : <div className="ui icon message">
                    <i className="info circle icon"></i>
                    <div className="content">
                        <p>{this.state.data.status}</p>
                    </div>
                </div>;
        else return null;
    }
}