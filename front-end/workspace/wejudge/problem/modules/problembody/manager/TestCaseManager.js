/**
 * Created by lancelrq on 2017/3/2.
 */

module.exports = TestCaseManager;

var React = require('react');
var core = require('wejudge-core');
var moment = require("moment");
var ManagerBase = require("./manager").ManagerBase;
var TestCaseEditor = require("./module/TestCaseEditor");
var TestCaseDataEditor = require("./module/TestCaseDataEditor");
var TestCaseDataUploader = require("./module/TestCaseDataUploader");

class TestCaseManager extends ManagerBase {

    constructor(props) {
        super(props);
        this.addTestCase = this.addTestCase.bind(this);
        this.modifyTestCase = this.modifyTestCase.bind(this);
        this.modifyTestCaseData = this.modifyTestCaseData.bind(this);
        this.uploadTestCaseData = this.uploadTestCaseData.bind(this);
        this.runTCMaker = this.runTCMaker.bind(this);
        this.showHistory = this.showHistory.bind(this);
        this.manager = props.manager;
    }

    componentDidUpdate() {
        var tclist = this.state.judge_config.test_cases;
        if(tclist && tclist.length > 0) {
            var tol = 0;
            for(var i = 0; i < tclist.length; i++){
                tol += tclist[i].score_precent;
            }

            $(this.refs.progress_bar).progress({
                percent: tol,
                text: {
                    active: tol < 100 ? "emmm...请设置一下各个测试数据的权重值，让它们的总和是100，不然可能会出现正确的题目判题机给分不足或依然给0分的情况哦！" : "你做的很好，本题的测试数据权重设置完毕，这将有助于判题机更好的评分"
                }
            });
        }
    }

    addTestCase(){
        this.refs.tcEditor.create();
    }
    modifyTestCase(entity){
        var that = this;
        return function () {
            that.refs.tcEditor.modify(entity);
        }
    }
    modifyTestCaseData(entity){
        var that = this;
        return function () {
            that.refs.tcdEditor.show(entity);
        }
    }
    removeTestCase(entity){
        var that = this;
        return function () {
            that.refs.confirm.setContent("你确定要删除这条测试数据吗，数据内容将被永久删除不可找回！", "操作确认");
            that.refs.confirm.show(function (rel) {
                if(rel){
                    that.doRemove(entity.handle);
                }
            })
        }
    }
    uploadTestCaseData(entity){
        var that = this;
        return function () {
            that.refs.tcdUploader.show(entity);
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
                handle: handle
            },
            success: function (rel) {
                that.removing = false;
                that.refs.alertbox.showSuccess(rel, function () {
                    that.manager.getJudgeConfig();
                });

            },
            error: function (rel, msg) {
                that.removing = false;
                that.refs.alertbox.showError(rel, msg);
            }
        }).call();
    }

    runTCMaker(){
        var that = this;
        that.refs.confirm.setContent("你确定要以语言【"+that.state.lang_call+"】执行测试数据自动生成操作码？原有的参考输出数据覆盖。", "操作确认");
        that.refs.confirm.show(function (rel) {
            if(rel){
                core.restful({
                    method: 'POST',
                    responseType: "json",
                    url: that.props.tcmaker_run,
                    data: {
                        lang: that.state.lang
                    },
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {

                        });

                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call();
            }
        })
    }

    showHistory() {
        this.refs.status_list.load();
        this.refs.StatusDialog.show();
    };

    render(){
        var tclist = this.state.judge_config.test_cases;
        tclist = tclist ? tclist.sort(function (a, b) {
            return a.order > b.order;
        }) : null;
        return (
            <div className="ui">
                <div className="ui compact menu">
                    <a className="item" onClick={this.addTestCase}>
                        <i className="add icon"></i>
                        添加数据
                    </a>
                    <a className="item" onClick={this.runTCMaker}>
                        <i className="hashtag icon"></i>
                        自动生成数据
                    </a>
                    <a className="item" onClick={this.showHistory}>
                        <i className="history icon"></i>
                        操作历史
                    </a>
                </div>
                <br />
                <table className="ui stackable striped table ">
                    <thead>
                        <tr>
                            <th>标识</th>
                            <th>名称</th>
                            <th>权重</th>
                            <th>可用性</th>
                            <th>可见性</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tclist && tclist.length > 0 ? tclist.map((val, key)=> {
                            return <tr key={key}>
                                <td>{val.handle}</td>
                                <td>{val.name}</td>
                                <td>{val.score_precent} %</td>
                                <td>{val.available ? "有效" : <span style={{color:"red"}}>"无效"</span>}</td>
                                <td>{val.visible ? "可见" : <span style={{color:"red"}}>不可见</span>}</td>
                                <td>
                                    <a className="ui tiny purple basic button" onClick={this.modifyTestCase(val)}><i className="setting icon"></i>设置</a>&nbsp;
                                    <a className="ui tiny yellow basic button" onClick={this.modifyTestCaseData(val)}><i className="edit icon"></i>编辑数据</a>&nbsp;
                                    <a className="ui tiny green basic button" onClick={this.uploadTestCaseData(val)}><i className="upload icon"></i>上传数据</a>&nbsp;
                                    <a className="ui tiny red basic button" onClick={this.removeTestCase(val)}><i className="remove icon"></i>删除</a>
                                </td>
                            </tr>
                        }) : <tr>
                            <td colSpan={6} style={{padding: 0}}>
                                <div className="ui icon message" style={{margin: 0, boxShadow: "none"}}>
                                    <i className="info circle icon"></i>
                                    <div className="content">
                                        <p>还没有测试数据哦！_(:зゝ∠)_</p>
                                    </div>
                                </div>
                            </td>
                        </tr>}
                    </tbody>
                </table>
                <div className="ui purple progress" ref="progress_bar">
                    <div className="bar">
                        <div className="progress"></div>
                    </div>
                    <div className="label">测试数据权重分配情况：请先创建测试数据</div>
                </div>
                <core.dialog.Dialog size="large" ref="StatusDialog" title="历史记录" btnShow={false}>
                    <TCMakerStatusListView ref="status_list" list_status={this.props.tcmaker_hisotory} />
                </core.dialog.Dialog>
                <TestCaseEditor apis={{submit: this.props.save_settings}} ref="tcEditor" manager={this.manager} />
                <TestCaseDataEditor apis={{submit: this.props.save_data, data: this.props.get_data}} ref="tcdEditor" manager={this.manager} />
                <TestCaseDataUploader apis={{uploadIn: this.props.upload_data.in, uploadOut: this.props.upload_data.out}} ref="tcdUploader" />
                <core.dialog.Confirm msg="" msg_title="操作确认" ref="confirm" />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>
        )
    }

}


class TCMakerStatusListView extends core.ListView {
    constructor(props) {
        super(props);
        this.apis = {
            data: props.list_status
        };
    }
    renderListHeader(){
        return (
            <tr>
                <th>ID</th>
                <th>提交者</th>
                <th>评测结果</th>
                <th>最大运行时长</th>
                <th>最大内存用量</th>
                <th>代码长度</th>
                <th>代码语言</th>
                <th>提交时间</th>
                <th>写入状态</th>
            </tr>
        );
    }
    renderListItems(){
        var flag_desc;
        if(this.state.rawdata)
            flag_desc = this.state.rawdata.flag_desc || {};
        else
            flag_desc = {};

        var that = this;

        if (this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                var view_flag_btn = function (flag) {
                    return (
                        <div className={"ui mini compact " + flag_desc[flag].color +" button"} title={flag_desc[flag].en}>
                            {flag_desc[flag].title}
                        </div>
                    )
                };
                return (
                    <tr key={key}>
                        <td>{item.id}</td>
                        <td>{ item.author.nickname}</td>
                        <td>{view_flag_btn(item.flag)}</td>
                        <td>{(item.flag === 2) ? "---" : item.exe_time + " MS"}</td>
                        <td>{(item.flag === 3) ? "---" : item.exe_mem + " KB"}</td>
                        <td>{item.code_len} 字节</td>
                        <td>{item.lang}</td>
                        <td>{item.create_time}</td>
                        <td>{item.auth_code === "" ? "写入完成" : (item.flag >= 0 ? "写入失败" : "队列中") }</td>
                    </tr>
                )
            });
        else
            return null
    }
}