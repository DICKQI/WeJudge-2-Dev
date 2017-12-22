/**
 * Created by lancelrq on 2017/7/14.
 */

module.exports = ProblemChoosing;

var React = require('react');
var core = require('wejudge-core');

var ProblemsetList = require("./ProblemsetList").ProblemsetList;
var ProblemsList = require("./ProblemsList").ProblemsList;


class ProblemChoosing extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            mode: "set",
            step: 0,
            init_plist: false,
            problem_selected: [],
            highlight_items: [],
            api_list_problem: props.apis.problemset.list_problem,
            api_jstree_get_data: props.apis.jstree.get_data,
            api_classify_get_data: props.apis.classify.get_data,
            url_view_problem: "",
            choose_items: {}
        };
        this.psetClick = this.psetClick.bind(this);
        this.backToPset = this.backToPset.bind(this);
        this.backToPList = this.backToPList.bind(this);
        this.goToConfirm = this.goToConfirm.bind(this);
        this.removeChoosing = this.removeChoosing.bind(this);
        this.saveChoosing = this.saveChoosing.bind(this);
        this.onChoose = this.onChoose.bind(this);
    }

    init(){
        var that = this;
        this.refs.ProblemSetView.load();
        //TODO
        if(this.props.apis.highlight_items){
            core.restful({
                url: this.props.apis.highlight_items,
                method: "GET",
                success: function (rel) {
                    that.setState({
                        highlight_items: rel.data
                    })
                }
            }).call();
        }
    }

    psetClick (rel){
        var that = this;
        this.setState({
            step: 0,
            init_plist: true,
            mode: "problems",
            api_list_problem: this.props.apis.problemset.list_problem.replace("problemset/0", "problemset/"+rel.id),
            api_jstree_get_data: this.props.apis.jstree.get_data.replace("problemset/0", "problemset/"+rel.id),
            api_classify_get_data: this.props.apis.classify.get_data.replace("problemset/0", "problemset/"+rel.id),
            url_view_problem: this.props.urls.view_problem.replace("problemset/0", "problemset/"+rel.id)
        }, function () {
            that.refs.ProblemListView.load();
        });
    }

    backToPset(){
        this.setState({
            step: 0,
            mode: "set"
        });
    }

    backToPList(){
        this.setState({
            step: 0,
            mode: "problems"
        });
    }

    goToConfirm(){
        this.setState({
            step: 1
        });
    }

    onChoose(rel){
        var problem_selected = this.state.problem_selected;
        var choose_items = {};
        var action = "add";
        for(var i = 0; i < problem_selected.length; i++){
            var problem = problem_selected[i];
            if(problem.entity.id === rel.entity.id){
                // 移除这个选项
                problem_selected.splice(i, 1);
                action = "rm";
                break;
            }
        }
        console.log(action)
        if(action === "add") {
            rel['state'] = 0;
            problem_selected.push(rel);
        }
        for(var i = 0; i < problem_selected.length; i++) {
            var problem = problem_selected[i];
            choose_items[problem.entity.id] = true;
        }
        this.setState({
            problem_selected: problem_selected,
            choose_items: choose_items
        })
    }

    removeChoosing(rel){
        var that = this;
        return function () {
            var problem_selected = that.state.problem_selected;
            var index = problem_selected.indexOf(rel);
            if(index > -1){
                problem_selected.splice(index, 1)
            }
            var choose_items = {};
            for(var i = 0; i < problem_selected.length; i++) {
                var problem = problem_selected[i];
                choose_items[problem.entity.id] = true;
            }
            that.setState({
                problem_selected: problem_selected,
                choose_items: choose_items
            })
        }
    }

    saveChoosing(success){
        var that = this;
        var problem_selected = that.state.problem_selected;
        var problem_ids = [];
        for(var i = 0; i < problem_selected.length; i++){
            var problem = problem_selected[i];
            if(problem.state === 0 || problem.state === 1){
                problem_ids.push(problem.entity.id);
            }
        }
        core.restful({
            url: that.props.apis.save_choosing,
            data:{
                "problem_ids": problem_ids
            },
            method: "POST",
            success: function (rel) {
                var result = rel.data;
                for(var i = 0; i < problem_selected.length; i++){
                    var problem = problem_selected[i];
                    if(result[problem.entity.id] !== undefined){
                        problem_selected[i].state = result[problem.entity.id]
                    }
                }
                that.setState({
                    problem_selected: problem_selected
                }, function () {
                    that.refs.FormMessager.show("操作成功！", "5秒后页面将自动刷新，即可看到选题操作带来的变动。", 'success');
                    // if(typeof success === "function"){
                    //     success(rel);
                    // }
                    setTimeout(function () {
                        window.location.reload();
                    }, 5000);
                });
            },
            error: function (rel, msg) {
                that.refs.FormMessager.show("操作失败！", msg, "error");
            }
        }).call();
    }

    componentDidMount() {
        $(this.refs.ChoosingSteps).find(".step").tab();
    }


    render() {
        var that = this;
        return (
            <div className="ui">
                <div className="ui three steps" ref="ChoosingSteps">
                    <a onClick={this.backToPset} data-tab="problemset" className={`${this.state.step === 0 && this.state.mode==="set" ? "active" : ""} step`}>
                        <i className="list items icon"></i>
                        <div className="content">
                            <div className="title">题目集</div>
                            <div className="description">查看并选择题目集</div>
                        </div>
                    </a>
                    <a onClick={this.backToPList} data-tab="problemset" className={`${this.state.step === 0 && this.state.mode==="problems" ? "active" : ""} ${this.state.init_plist ? "" : "disabled"} step`}>
                        <i className="file text icon"></i>
                        <div className="content">
                            <div className="title">题目选择</div>
                            <div className="description">查看并选择题目</div>
                        </div>
                    </a>
                    <a onClick={this.goToConfirm} data-tab="confirm" className={`${this.state.step === 1 ? "active" : ""} ${this.state.problem_selected.length === 0 ? "disabled" : ""} step`}>
                        <i className="info icon"></i>
                        <div className="content">
                            <div className="title">确认选择</div>
                            <div className="description">当前已选<strong> {this.state.problem_selected.length} </strong>题</div>
                        </div>
                    </a>
                </div>
                <div className="ui tab" data-tab="confirm">
                    <h3>已选择题目</h3>
                    <table className="ui celled table">
                        <thead>
                            <tr>
                                <th>#ID</th>
                                <th>题目名称</th>
                                <th>状态</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                        {this.state.problem_selected.length > 0 ? this.state.problem_selected.map(function (val, key) {
                            var STATE = {
                                0: "待确认",
                                1: '<i class="icon close"></i>添加失败或是题目不存在',
                                2: '<i class="icon attention"></i>当前项已存在',
                                3: '<i class="icon checkmark"></i>添加成功'
                            };
                            var STATE_TR = {
                                0: "",
                                1: "error",
                                2: "error",
                                3: "positive"
                            };
                            return <tr key={key} className={STATE_TR[val.state] || ""}>
                                <td>{val.entity.id}</td>
                                <td>{val.title}</td>
                                <td><span dangerouslySetInnerHTML={{__html: STATE[val.state] || "未知"}}></span></td>
                                <td>
                                    <a className="ui red tiny button" onClick={that.removeChoosing(val)}><i className="remove icon" />取消选择</a>
                                </td>
                            </tr>
                        }) :
                            <tr>
                                <td colSpan="3">请先选择题目</td>
                            </tr>
                        }
                        </tbody>
                    </table>
                    <core.dimmer.FormMessager inverted ref="FormMessager" />
                    {this.props.dialog ? null : <a onClick={this.saveChoosing} className={`ui ${this.state.problem_selected.length === 0 ? "disabled" : ""} green button`}>
                        <i className="checkmark icon"></i>确认选择！
                    </a>}
                </div>
                <div className="ui black tab active" data-tab="problemset">
                    <div className="" style={{display: this.state.mode === "set" ? "block" : "none"}}>
                        <ProblemsetList
                            ref="ProblemSetView"
                            apis={{
                                list_problemset: this.props.apis.problemset.list_problemset,
                            }}
                            urls={{}}
                            options={{readonly: true}}
                            psetClick={this.psetClick}
                        />
                    </div>
                    <div className=""  style={{display: this.state.mode === "problems" ? "block" : "none"}}>
                        {this.state.mode === 'problems' ? <ProblemsList
                            ref="ProblemListView"
                            apis={{
                                list_problem: this.state.api_list_problem,
                                jstree: {
                                    get_data: this.state.api_jstree_get_data
                                },
                                classify:{
                                    get_data: this.state.api_classify_get_data
                                }
                            }}
                            urls={{
                                view_problem: this.state.url_view_problem
                            }}
                            options={{hide_filter: false, target_blank: true}}
                            onChoose={this.onChoose}
                            highLightItems={this.state.highlight_items}
                            chooing_items={this.state.choose_items}
                        /> : null}
                    </div>
                </div>
            </div>
        )
    }
}