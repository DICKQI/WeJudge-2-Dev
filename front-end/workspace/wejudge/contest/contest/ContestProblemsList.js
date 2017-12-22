/**
 * Created by lancelrq on 2017/4/7.
 */


var React = require("react");
var core = require("wejudge-core");

module.exports = ContestProblemsList;

class ContestProblemsList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state['is_admin'] = props.is_admin || false;
        this.apis = {
            data: props.apis.problems_list
        };
        this.removeProblem = this.removeProblem.bind(this);
        this.rejudgeProblem = this.rejudgeProblem.bind(this);
        this.showEdit = this.showEdit.bind(this);
    }

    rejudgeProblem(pid){
        var that = this;

        return function () {
            if(confirm("你确定执行重判吗")){
                core.restful({
                    url: that.props.apis.rejudge_problem.replace("problem/0", "problem/" + pid),
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            window.location.reload();
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        }
    }
    removeProblem(pid){
        var that = this;

        return function () {
            if(confirm("你确定要删除这个题目吗？这将会删除这关于道题的所有评测记录和设置！")){
                core.restful({
                    url: that.props.apis.remove_problem.replace("problem/0", "problem/" + pid),
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            window.location.reload();
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        }
    }
    showEdit(entity){
        var that = this;
        return function () {
            that.refs.contest_problem_setting.viewSetting(entity)
        }
    }

    renderListHeader(){
        return (
            <tr>
                <th width="50">题号</th>
                <th>名称</th>
                <th className="center aligned" width={200}>通过 / 提交</th>
                <th className="center aligned">
                    {this.state.is_admin ? "功能" : "我的评测"}
                </th>
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key}>
                        <td>{core.tools.gen_problem_index(item.index)}</td>
                        <td>
                            <a target="_blank" href={this.props.urls.problem_view.replace("problem/0", "problem/"+item.id)}>
                                {item.entity.title ? item.entity.title : `题目${core.tools.gen_problem_index(item.index)}`}
                            </a>
                        </td>
                        <td className="center aligned">{item.accepted} / {item.submission}</td>
                        <td className="center aligned">{
                            this.state.is_admin ?
                                <div>
                                    <a className="ui mini primary button" onClick={this.showEdit(item)}>设置</a>
                                    <a className="ui mini green button"onClick={this.rejudgeProblem(item.id)}><i className="refresh icon"></i>重判</a>
                                    <a className="ui mini yellow button" href={this.props.urls.manager_view.replace('problem/0', 'problem/' + item.entity.id)} target="_blank"><i className="edit icon"></i>评测设置</a>
                                    <a className="ui mini red button" onClick={this.removeProblem(item.id)}><i className="remove icon"></i>移除</a>
                                </div> : <div>
                                    {item.status || null}
                                </div>
                        }
                        </td>
                    </tr>
                )
            });
        else
            return null
    }

    renderFooterBody(){
        return <div>
            <ContestProblemSetting
                manager={this}
                save_data={this.props.apis.save_problem_setting}
                ref="contest_problem_setting"
            />
            <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
        </div>
    }
}

class ContestProblemSetting extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.state = {
            entity : null
        };
        this.apis = {
            submit: ""
        };
        this.LangList = core.LangList;

    }

    viewSetting(entity){
        // this.refs.FormMessager.hide();
        this.setState({
            entity: entity
        });
        this.apis.submit = this.props.save_data.replace("problem/0", "problem/" + entity.id);
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }



    // doSubmitSuccess(rel){
    //     this.refs.FormMessager.show("保存成功", '刷新页面即可看到改动情况', "success");
    // }
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
                var checked = (!lang || lang == 0 || ((value[0] & lang) > 0));
                return (<core.forms.CheckBoxField name="lang"  key={key} label={value[1]} value={value[0]} checked={checked} />);
            })
        };
        var formBody = this.state.entity && this.renderForm(
            <section>
                <div className="inline fields">
                    <core.forms.TextField inline name="index" label="序号" value={this.state.entity.index} />
                    <core.forms.CheckBoxField
                        name="status_editable" type="toggle" label="允许裁判修改判题结果" value="true" checked={this.state.entity.status_editable} />
                </div>
                <div className="ui secondary inline fields segment">
                    <label>可用：</label>
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