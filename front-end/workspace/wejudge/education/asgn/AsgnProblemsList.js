/**
 * Created by lancelrq on 2017/3/27.
 */


var React = require("react");
var core = require("wejudge-core");
var ProblemChoosing = require("../../problem/modules/problemset/ProblemChoosing");

module.exports = AsgnProblemsList;

class AsgnProblemsList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state['is_teacher'] = props.is_teacher || false;
        this.apis = {
            data: props.apis.problems_list
        };
        this.showProblemSettings = this.showProblemSettings.bind(this);
        this.showProblemChoosing = this.showProblemChoosing.bind(this);
        this.rejudgeProblem = this.rejudgeProblem.bind(this);
    }

    showProblemSettings(pid){
        var that = this;
        return function () {
            that.refs[`asgn_problem_setting_${pid}`].viewSetting(pid);
        }
    }

    showProblemChoosing(){
        var that = this;
        this.refs.ChoosingDialog.show(function () {
            if(that.refs.ProblemChoosing.state.problem_selected.length <= 0){return;}
            that.refs.ProblemChoosing.saveChoosing(function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.load();
                });
            });
        },function () {

        });
        that.refs.ProblemChoosing.init();
    }

    removeProblem(pid){
        var that = this;
        return function () {
            that.refs.confirm.setContent('操作提示', '确定要从这个作业中移除这条题目吗？已有信息将不会被删除，再次添加题目时，将重新关联。');
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.remove_problem.replace('problem/0', 'problem/' + pid),
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.load()
                            });
                        },
                        error: function (rel, msg) {
                            that.refs.alertbox.showError(rel, msg);
                        }
                    }).call()
                }
            });
        }
    }

    rejudgeProblem(pid){
        var that = this;
        return function () {
            that.refs.confirm.setContent('操作提示', '确定要重判这道题目吗？');
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.rejudge_problem.replace('problem/0', 'problem/' + pid),
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
    }

    renderListHeader(){
        return (
            <tr>
                <th>题号</th>
                <th>题目</th>
                <th>要求</th>
                <th>分值</th>
                <th>难度</th>
                <th>总体正确率</th>
                {this.state.is_teacher ? <th>
                    {/*<div onClick={this.showProblemChoosing} className="ui mini green button">*/}
                        {/*<i className="add icon"></i>增加题目*/}
                    {/*</div>*/}
                    管理
                </th> : <th>状态</th>}
                {this.state.is_teacher ? null : <th>得分</th>}
            </tr>
        );
    }
    renderListItems(){
        var PROBLEM_STATUS = {
            0:"未访问",
            1:"正在做",
            2:"已完成"
        };
        var PROBLEM_STATUS_COLOR = {
            0:"grey",
            1:"yellow",
            2:"green"
        };
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                var all_ratio = ((item.submission > 0) ? 100 * (item.accepted/item.submission) : 0).toFixed(2);
                return (
                    <tr key={key}>
                        <td>{core.tools.gen_problem_index(item.index)}</td>
                        <td>
                            <a href={this.props.urls.problem_view.replace("problem/0", "problem/"+item.id)}>{item.entity.title}</a>
                        </td>
                        <td>{item.require ? <strong>必做题</strong> : "选做题"}</td>
                        <td>{item.score }</td>
                        <td><core.forms.RatingField disabled rating={item.entity.difficulty} /></td>
                        <td>{all_ratio}% ({item.accepted} / {item.submission})</td>
                        {
                            this.state.is_teacher ?
                            <td>
                                <a className="ui primary compact button" onClick={this.showProblemSettings(item.id)}>
                                    <i className="settings icon" /> 设置
                                </a>
                                <a className="ui yellow compact button" onClick={this.rejudgeProblem(item.id)}>
                                    <i className="refresh icon" /> 重判
                                </a>
                                <a className="ui red compact button" onClick={this.removeProblem(item.id)}>
                                    <i className="remove icon" /> 移除
                                </a>
                                <AsgnProblemSetting
                                    manager={this}
                                    data={item}
                                    save_data={this.props.apis.save_problem_setting.replace("problem/0", "problem/" + item.id)}
                                    ref={`asgn_problem_setting_${item.id}`}
                                />
                            </td>
                            :
                            <td>
                                <span className={`ui ${PROBLEM_STATUS_COLOR[item.status]} label`}>
                                    {PROBLEM_STATUS[item.status]}{item.status_count}
                                </span>
                            </td>
                        }
                        {this.state.is_teacher ? null : <td>{item.status_score}</td>}
                    </tr>
                )
            });
        else
            return null
    }

    renderFooterBody(){
        return <div>
            {/*{this.state.is_teacher ? <core.dialog.Dialog ref="ChoosingDialog" title="选择题目" size="fullscreen" btnTitle="选定">*/}
                {/*<ProblemChoosing*/}
                    {/*ref="ProblemChoosing" dialog*/}
                    {/*apis={this.props.apis.problem_choosing}*/}
                    {/*urls={this.props.urls.problem_choosing}*/}
                {/*/>*/}
            {/*</core.dialog.Dialog> : null}*/}
            <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            <core.dialog.Confirm msg="" msg_title="操作确认" ref="confirm" />
        </div>
    }
}

class AsgnProblemSetting extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.state = {
            entity : props.data
        };
        this.apis = {
            data: "",
            submit: props.save_data
        };
        this.LangList = core.LangList;
    }

    viewSetting(pid) {
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });

    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            entity: nextProps.data
        })
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.props.manager.load();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    render(){
        var that = this;
        var languageSelected = function() {
            var lang = that.state.entity.lang;

            return that.LangList.map((value, key) => {
                var checked = (!lang || lang === 0 || ((value[0] & lang) > 0));
                return (<core.forms.CheckBoxField  name="lang"  key={key} label={value[1]} value={value[0]} checked={checked} />);
            })
        };
        var formBody = this.renderForm(
            <section>
                <div className="two fields">
                    <core.forms.TextField name="score" label="题目分值" value={this.state.entity.score} />
                    <core.forms.TextField name="max_score_for_wrong" label="错答时最高可得分比例(%)" value={this.state.entity.max_score_for_wrong} />
                </div>
                <div className="ui horizontal divider">选项设置</div>
                <div className="ui three fields segment">
                    <core.forms.CheckBoxField
                        name="require" type="toggle" label="必做题" value="true" checked={this.state.entity.require} />
                    <core.forms.CheckBoxField
                        name="strict_mode" type="toggle" label="严格模式" value="true" checked={this.state.entity.strict_mode} />
                    <core.forms.CheckBoxField
                        name="hidden_answer" type="toggle" label="隐藏参考答案" value="true" checked={this.state.entity.hidden_answer} />
                </div>
                <div className="ui horizontal divider">可用评测语言</div>
                <div className="inline fields">
                    {languageSelected()}
                </div>

            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="题目设置" size="small" btnTitle="保存">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>
        );
    }

}