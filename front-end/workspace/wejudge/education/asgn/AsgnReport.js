/**
 * Created by lancelrq on 2017/4/1.
 */

var React = require("react");
var moment = require("moment");
var core = require("wejudge-core");
var JudgeStatusListView = require("../../problem/modules/judge_status/JudgeStatusList").JudgeStatusListView;

module.exports = AsgnReport;

class AsgnReport extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state['mode'] = props.mode || "view";
        this.apis = {
            data: props.apis.get_report
        };

    }

    componentWillReceiveProps(nextProps) {
        this.apis.data = nextProps.apis.get_report;
    }

    componentDidUpdate() {
        if(this.state.data && this.state.mode==='student' && !this.state.data.report.teacher_check)
            this.refs.myImpressionArea && this.refs.myImpressionArea.doEdit();
        if( this.state.mode==='teacher'){
            this.refs.teacherRemarkArea && this.refs.teacherRemarkArea.doEdit();
        }
    }

    showStatus(problem_id, author_id){
        var that = this;
        return function () {
            that.refs.StatusView.setParams({
                author_id: author_id,
                problem_id: problem_id
            });
            that.refs.StatusView.getListData();
            that.refs.StatusDialog.show();
        }
    }

    renderBody() {
        var report = this.state.data;
        return (report ? <div className="ui">
                <div style={{textAlign: "center"}}>
                    <h1 className="ui header">程序设计课程实验报告</h1>

                </div>
                {report.report.excellent ?
                    <img style={{position:"absolute", right: "0.5em", top:"0em"}} src="/static/images/great.png" width="100" height="100" alt=""/>
                    : null}
                <table className="ui fixed celled top attached selectable  table">
                    <tbody>
                    <tr>
                        <td className="left aligned"><strong>姓名</strong></td>
                        <td>{report.author.realname}</td>
                        <td className="left aligned"><strong>学号</strong></td>
                        <td>{report.author.username}</td>
                        <td className="left aligned"><strong>最后修改时间</strong></td>
                        <td>{core.tools.format_datetime(report.report.modify_time)}</td>
                        <td className="left aligned"><strong>批改</strong></td>
                        <td>{report.report.teacher_check ? "已批改" : report.report.impression ? "未批改" : "未提交"}</td>
                    </tr>
                    </tbody>
                </table>
                <table className="ui fixed celled bottom attached selectable table">
                    <thead>
                    <tr>
                        <th>题号</th>
                        <th>题目名称</th>
                        <th>通过/提交/判罚次数</th>
                        <th>最少时间使用</th>
                        <th>最少内存使用</th>
                        <th>最短代码</th>
                        <th>状态</th>
                        <th>最终得分</th>
                    </tr>
                    </thead>
                    <tbody>
                    {report.problems.map((val, key)=>{
                        var sol = report.soluctions[val.id];
                        if(sol)
                            return (
                                <tr key={key} onClick={this.showStatus(core.tools.gen_problem_index(val.index), report.author.username)} style={{cursor: "pointer"}}>
                                    <td>{core.tools.gen_problem_index(val.index)}</td>
                                    <td><a href={this.props.urls.view_problem.replace("problem/0", "problem/" + val.id)}>{val.entity.title}</a></td>
                                    <td>{sol.accepted} / {sol.submission} / {sol.penalty}</td>
                                    <td>{sol.accepted > 0 ? sol.best_time : "---"} MS</td>
                                    <td>{sol.accepted > 0 ? sol.best_memory : "---"} KB</td>
                                    <td>{sol.accepted > 0 ? sol.best_code_size : "---"} Byte</td>
                                    <td>{sol.first_ac_time > 0 ? <span className="ui green label">已完成</span> : <span className="ui red label">未完成</span>}</td>
                                    <td>{sol.finally_score}</td>
                                </tr>
                            );
                        else
                            return (
                                <tr key={key}>
                                    <td>{core.tools.gen_problem_index(val.index)}</td>
                                    <td><a href={this.props.urls.view_problem.replace("problem/0", "problem/" + val.id)}>{val.entity.title}</a></td>
                                    <td colSpan="6" className="center aligned">未访问</td>
                                </tr>
                            );
                    })}
                    <tr>
                        <td colSpan="6"></td>
                        <td><h4>系统给分（参考）</h4></td>
                        <td><h4>{report.report.judge_score}</h4></td>
                    </tr>
                    <tr>
                        <td colSpan={8}></td>
                    </tr>
                    <tr className="active">
                        <td colSpan="6">
                            <h3>
                                {/*{this.state.mode==='student' && !report.report.teacher_check ?*/}
                                    {/*<a className="ui mini compact primary right floated button" onClick={function (that) {*/}
                                        {/*return function () {*/}
                                            {/**/}
                                        {/*}*/}
                                    {/*}(this)}>*/}
                                        {/*<i className="edit icon"></i>编辑*/}
                                    {/*</a>*/}
                                {/*: null}*/}
                                我的实验感想
                            </h3>
                        </td>
                        <td colSpan={2}>
                            <h3>
                                {this.state.mode==='student' && !report.report.teacher_check ?
                                    report.report.attachment ?
                                        <a href={this.props.urls.download_attachment.replace("report/0", "report/" + report.report.id)}
                                            className="ui primary compact right floated mini button">
                                        点击下载
                                    </a> : <span className="ui disabled grey compact right floated mini button">未上传</span>
                                : null }
                                附件
                            </h3>
                        </td>
                    </tr>
                    <tr>
                        <td colSpan="6">
                            <MyImpressionArea
                                ref="myImpressionArea"
                                impression={report.report.impression}
                                manager={this}
                                editable={this.state.mode==='student'}
                                save={this.props.apis.save_impression}
                            />
                        </td>
                        <td colSpan={2}>
                            {this.state.mode==='student' && !report.report.teacher_check ?
                                <core.forms.FileField ref="upload" upload_api={this.props.apis.upload_attachment} auto />
                                : report.report.attachment ? <a href={this.props.urls.download_attachment.replace("report/0", "report/" + report.report.id)}
                                     className="ui primary compact fluid mini button">
                                    点击下载
                                </a> : <span className="ui disabled grey compact fluid mini button">未上传</span>
                            }
                        </td>
                    </tr>
                    <tr>
                        <td colSpan={8}></td>
                    </tr>
                    <tr className="active">
                        <td colSpan="8">
                            <h3>
                                {/*{this.state.mode==='teacher' ?*/}
                                    {/*<a className="ui mini compact green right floated button" onClick={function (that) {*/}
                                        {/*return function () {*/}
                                            {/*that.refs.teacherRemarkArea.doEdit()*/}
                                        {/*}*/}
                                    {/*}(this)}>*/}
                                        {/*<i className="edit icon"></i>批改*/}
                                    {/*</a>*/}
                                {/*: null}*/}
                                教师评语
                            </h3>
                        </td>
                    </tr>
                    <tr>
                        <td colSpan="8">
                            <TeacherRemarkArea
                                ref="teacherRemarkArea"
                                remark={report.report.teacher_remark}
                                public_code={report.report.public_code}
                                excellent={report.report.excellent}
                                editable={this.state.mode==='teacher'}
                                manager={this}
                                save={this.props.apis.save_checkup}
                                score={report.report.teacher_check ? report.report.finally_score : report.report.judge_score}
                            />
                        </td>
                    </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <th colSpan="6"></th>
                            <th><h4>最终得分</h4></th>
                            <th><h4>{report.report.teacher_check ? report.report.finally_score : "未批改"}</h4></th>
                        </tr>
                    </tfoot>
                </table>
                <core.dialog.Dialog ref="StatusDialog" title="评测记录" size="large" btnShow={false} auto_close>
                    <JudgeStatusListView
                        ref="StatusView"
                        realname={true}                             // 是否显示真实姓名
                        nickname={false}                            // 是否显示昵称
                        userid={false}                              // 是否显示用户名
                        list_status={this.props.apis.list_status}
                        view_problem={this.props.urls.view_problem}
                        view_detail={this.props.urls.view_status_detail}
                        app_name={"education"}
                    />
                </core.dialog.Dialog>
            </div> : null
        );
    }
}

class MyImpressionArea extends core.forms.FormComponent {
    constructor(props) {
        super(props);
        this.state = {
            impression: props.impression || "",
            editable: props.editable || false,
            editmode: false
        };
        this.apis = {
            submit: props.save
        };
        this.manager = props.manager;
        this.doEdit = this.doEdit.bind(this);
        this.closeEdit = this.closeEdit.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            impression: nextProps.impression || ""
        })
    }
    doEdit(){
        this.setState({
            editmode: true
        })
    }
    closeEdit(){
        this.setState({
            editmode: false
        })
    }
    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.getData(null, function () {
                that.setState({
                    editmode: false
                });
            });
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.alertbox.showError(rel, msg);
    }


    render(){
        var Body;
        if(this.state.editable && this.state.editmode) {
            var formBody = this.renderForm(
                <section>
                    <core.forms.CKEditorField name="impression" value={this.state.impression} />
                    <button className="ui mini green button"><i className="save icon"></i>保存</button>
                </section>
            );
            Body = (
                <div className="ui">
                    {formBody}
                </div>
            )
        }else{
            Body = (
                <div className="ui">
                    <div dangerouslySetInnerHTML={{__html: this.state.impression || "无"}}></div>
                    {/*{this.state.editable ?*/}

                    {/*: null }*/}
                </div>
            )
        }
        return (
            <section>
                {Body}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg=""/>
            </section>
        )

    }
}

class TeacherRemarkArea extends core.forms.FormComponent {
    constructor(props) {
        super(props);
        this.state = {
            remark: props.remark || "",
            editable: props.editable || false,
            editmode: false
        };
        this.apis = {
            submit: props.save
        };
        this.manager = props.manager;
        this.doEdit = this.doEdit.bind(this);
        this.closeEdit = this.closeEdit.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            remark: nextProps.remark || ""
        })
    }
    doEdit(){
        this.setState({
            editmode: true
        })
    }
    closeEdit(){
        this.setState({
            editmode: false
        })
    }
    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.getData(null, function () {
                that.setState({
                    editmode: false
                });
            });
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.alertbox.showError(rel, msg);
    }


    render(){
        var Body;
        if(this.state.editable && this.state.editmode) {
            var formBody = this.renderForm(
                <section className="ui">
                    <div className="ui stackable grid">
                        <div className="four wide column">
                            <core.forms.TextField label="最终得分" name="finally_score" value={this.props.score || "0"} />
                            <core.forms.CheckBoxField
                                name="excellent" type="toggle"
                                label="优秀作业" value="true" checked={this.props.excellent}
                            />
                            <core.forms.CheckBoxField
                                name="public_code" type="toggle"
                                label="公开学生代码" value="true" checked={this.props.public_code}
                            />
                            <button className="ui mini green button"><i className="save icon"></i>保存</button>
                        </div>
                        <div className="twelve wide column">
                            <core.forms.CKEditorField name="remark" value={this.state.remark} />
                        </div>
                    </div>

                </section>
            );
            Body = (
                <div className="ui">
                    {formBody}
                </div>
            )
        }else{
            Body = (
                <div className="ui">
                    <div dangerouslySetInnerHTML={{__html: this.state.remark || "无"}}></div>
                    {/*{this.state.editable ?*/}
                        {/*<div>*/}
                            {/*<br />*/}
                            {/*<a className="ui mini primary button" onClick={this.doEdit}><i className="edit icon"></i>批改/编辑</a>*/}
                        {/*</div>*/}
                    {/*: null }*/}
                </div>
            )
        }
        return (
            <section>
                {Body}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg=""/>
            </section>
        )
    }
}