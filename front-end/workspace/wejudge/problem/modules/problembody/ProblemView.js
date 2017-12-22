/**
 * Created by lancelrq on 2017/5/2.
 */

var React = require('react');
var core = require('wejudge-core');
var ProblemBodyDesc = require("./ProblemBodyDesc");
var SubmitCode = require("./SubmitCode");
var StatisticsView = require("./StatisticsView");
var JudgeStatusList = require("../judge_status/JudgeStatusList").JudgeStatusList;

module.exports = ProblemView;

class ProblemView extends core.PageView {

    // 构造
    constructor(props) {
        super(props);
        // this.state["data"] 为题目数据模块
        // 可选模块
        this.state["optionals"] = {
            statistics: props.optionals.statistics || true  // 评测统计模块是否显示
        };
        this.apis ={
            data: props.apis.problem
        }

    }

    componentDidMount() {
        var that = this;
        this.getData(null, function () {
            $(that.refs.MainTab).find(".item").tab({
                onLoad: function () {
                    var tab_name = $(this).attr("data-tab");
                    if (tab_name === "my_history") {
                        that.refs.judge_status_list.load();
                    }
                    else if(tab_name === "statistics"){
                        that.refs.statistics_view.load();
                    }
                }
            });
        });

    }

    renderBody(){
        var problem_data = this.state.data;
        return (
            <div className="ui">
                <div className="ui top tabular menu" ref="MainTab">
                    <a className="active item" data-tab="problem_description">
                        <i className="book icon"></i>
                        题目正文
                    </a>
                    <a className="item" data-tab="my_history">
                        <i className="tasks icon"></i>
                        我的记录
                    </a>
                    {this.props.optionals.statistics ?
                    <a className="item" data-tab="statistics">
                        <i className="signal icon"></i>
                        评测统计
                    </a>
                    : null}
                    {this.props.urls.manager ?
                    <a href={this.props.urls.manager} className="item" target="_blank">
                        <i className="setting icon"></i>
                        题目管理
                    </a> : null }
                </div>
                <div className="ui active tab" data-tab="problem_description">
                    <ProblemBodyDesc problem={problem_data.body} judge_config={problem_data.judge_config} />
                    <div className="ui relaxed horizontal divider">
                        <h3><i className="code icon"></i> 提交代码</h3>
                    </div>
                    {!problem_data.body.pause_judge ?
                        <SubmitCode
                            problem={problem_data.body}
                            judge_config={problem_data.judge_config}
                            apis={this.props.apis.judge}
                            urls={this.props.urls.judge}
                            user_id={this.props.optionals.user_id}
                        /> :
                        <div className="ui icon message">
                            <i className="warning circle icon"></i>
                            <div className="content">
                                当前评测暂停，请联系出题人
                            </div>
                        </div>
                    }
                </div>
                <div className="ui tab" data-tab="my_history">
                    <JudgeStatusList
                        ref="judge_status_list"
                        apis={this.props.apis.history}
                        urls={this.props.urls.history}
                        options={this.props.optionals.history}
                    />
                </div>
                {this.props.optionals.statistics ?
                <div className="ui tab" data-tab="statistics">
                    <StatisticsView
                        ref="statistics_view"
                        statistics_api={this.props.apis.statistics.data}
                    />
                </div>
                : null }
            </div>
        )
    }
}