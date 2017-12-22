/**
 * Created by lancelrq on 2017/7/1.
 */


var React = require("react");
var core = require("wejudge-core");

module.exports = AsgnReportsList;

var AsgnReport = require('./AsgnReport');


class ReportsList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.reports_list
        };
        this.selectAll = this.selectAll.bind(this);
        // this.viewReportLink = this.viewReportLink.bind(this);
    }
    onListLoaded(listdata, rawdata){
        var chk_list = {};
        listdata.map((item, key) => {
            chk_list[item.id] = !item.teacher_check;
        });
        this.setState({
            chk_list: chk_list
        });
    }
    selectAll(e){
        var chk_list = this.state.chk_list;
        var flag = e.target.checked;
        this.state.listdata.map((item, key) => {
            chk_list[item.id] = flag;
        });
        this.setState({
            chk_list: chk_list
        });
    }
    // viewReportLink(report_id){
    //     var that = this;
    //     return function () {
    //         that.props.view_report && that.props.view_report(report_id);
    //     }
    // }
    renderListHeader(){
        return (
            <tr>
                <th>
                    <core.forms.CheckBoxField label="#ID" onchange={this.selectAll} />
                </th>
                <th>学号</th>
                <th>姓名</th>
                <th>最后更新时间</th>
                <th>完成 (通过/提交)</th>
                <th>自动评分</th>
                <th>最终成绩</th>
                <th>实验报告</th>
                <th>备注</th>
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0) {
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key}>
                        <td>
                            <core.forms.CheckBoxField
                            name="report_ids" label={item.id} value={item.id}
                            checked={this.state.chk_list ? this.state.chk_list[item.id] : null} />
                        </td>
                        <td>{item.author.username}</td>
                        <td><a href="javascript:void(0)" onClick={core.show_account('education', item.author.id)}>{item.author.realname}</a></td>
                        <td>{core.tools.format_datetime(item.modify_time)}</td>
                        <td>{item.solved_counter} ({item.ac_counter} / {item.submission_counter})</td>
                        <td>{item.judge_score}</td>
                        <td>{item.teacher_check ? item.finally_score : "---" }</td>
                        <td><a href={this.props.view_report.replace("report/0", "report/" + item.id)} target="_blank">点击查看</a></td>
                        <td>{item.teacher_check ? <i className="checkmark icon"></i> : <i className="help icon"></i> }{item.teacher_check ? "已批改" : "未批改" }{item.excellent ? "、优秀作业" : ""}{ item.public_code ? "、公开答案" : ""}</td>
                    </tr>
                )
            });
        }
        else
            return null
    }
}


class AsgnReportsList extends core.forms.FormComponent {

    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            submit: this.props.apis.save_batch_checkup
        };
        this.state = {
            mode: "list",
            api_get_report: "",
            api_save_checkup: "",
            disable_finally_score: true,
            finally_score: 100,
            use_judge_score: true,
            remark: ""
        };
        this.load = this.load.bind(this);
        this.useJudgeScoreChange = this.useJudgeScoreChange.bind(this);
        this.showBatchDialog = this.showBatchDialog.bind(this);
        this.refreshData = this.refreshData.bind(this);
    }
    showBatchDialog(){
        var that = this;
        this.refs.BatchDialog.show(function () {
            that.submit();
            return false;
        })
    }
    load(){
        this.refs.listView.getListData();
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.load();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.alertbox.showError(rel, msg);
    }

    refreshData(){
        var that = this;
        that.refs.confirm.setContent('将要在后台启动作业数据的重算工作，执行后稍等片刻即可看到结果。是否继续？');
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.refresh_datas,
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {

                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        });
    }


    useJudgeScoreChange(e){

    }
    render(){
        var formBody =  this.renderForm(
            <div className="ui">
                <ReportsList ref="listView"
                     reports_list={this.props.apis.reports_list}
                     view_report={this.props.urls.view_report}
                />
                <input type="hidden" name="finally_score" value={this.state.finally_score}/>
                <input type="hidden" name="use_judge_score" value={this.state.use_judge_score}/>
                <input type="hidden" name="remark" value={this.state.remark} />
                <core.dialog.Dialog ref="BatchDialog" title="一键批改作业" size="tiny">
                    <div className="ui form">
                        <core.forms.CheckBoxField
                            name="use_judge_score" type="toggle"
                            label="使用判题机分数" value="true" checked={this.state.disable_finally_score}
                            onchange={function (that) {
                                return function(e){
                                    that.setState({
                                        use_judge_score: e.target.checked,
                                        disable_finally_score: e.target.checked
                                    });
                                }
                            }(this)}
                        />
                        <core.forms.TextField
                            label="最终得分" value="100"
                            onchange={function (that) {
                                return function(e){
                                    that.setState({ finally_score: e.target.value});
                                }
                            }(this)}
                            disabled={this.state.disable_finally_score} inline
                        />
                        <core.forms.TextAreaField
                            label="评语" name="remark"
                            onchange={function (that) {
                                return function(e){
                                    that.setState({ remark: e.target.value});
                                }
                            }(this)}
                        />
                    </div>
                </core.dialog.Dialog>
            </div>
        );
        return (
            <div className="ui">
                <div className="ui compact menu">
                    <a onClick={this.showBatchDialog} className="item"><i className="tasks icon"></i>批量处理</a>
                    <a onClick={this.refreshData} className="item"><i className="refresh icon"></i>数据重算</a>
                </div>
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面"/>
                <core.dialog.Confirm msg="你确定？" msg_title="操作确认" ref="confirm" />
            </div>
        )
    }
}