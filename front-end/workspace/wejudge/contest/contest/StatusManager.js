/**
 * Created by lancelrq on 2017/4/20.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = StatusManager;

class StatusManager extends React.Component {

    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.doDelete = this.doDelete.bind(this);
        this.showEditor = this.showEditor.bind(this);
        this.doRejudge = this.doRejudge.bind(this);
    }


    doDelete(){
        var that = this;
        that.refs.confirm.setContent('确定要执行删除操作吗？');
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.do_delete,
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


    doRejudge(){
        var that = this;
        that.refs.confirm.setContent('确定要执行重判操作吗？');
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.rejudge,
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
        });
    }

    showEditor(){
        this.refs.editor.show();
    }

    render(){
        return (
            <div className="ui">
                <div className="ui menu">
                    <a className="item" onClick={this.showEditor}><i className="edit icon"></i>修改评测结果</a>
                    <a className="item" onClick={this.doRejudge}><i className="refresh icon"></i>重判当前评测记录</a>
                    <a className="item" onClick={this.doDelete}><i className="remove icon"></i>删除评测结果(不建议使用)</a>
                </div>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="谨慎操作：删除操作不会反映到排行榜，请在删除评测结果后，使用排行榜重算功能！" msg_title="操作确认" ref="confirm" />
                <ContestStatusEditor
                    ref="editor"
                    edit_status={this.props.apis.edit_status}
                    load_status={this.props.apis.load_status}
                />
            </div>
        )
    }
}

class ContestStatusEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            entity: null
        };
        this.apis = {
            submit: props.edit_status,
            data: props.load_status
        }
    }

    show(){
        var that = this;
        this.getData(function (rel) {
            that.setState({
                entity: rel.data
            });
            that.refs.FormDialog.show(function () {
                that.submit();
                return false;
            });
        }, function (rel, msg) {
            that.refs.alertbox.showError(rel, msg);
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            window.location.reload();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            this.state.entity ?
                <section>
                    <input type="hidden"/>
                    <core.forms.SelectField name="flag" label="更改评测结果" forceDefault value={this.state.entity.status.flag}>
                        <option value="0">评测通过(AC)</option>
                        <option value="1">格式错误(PE)</option>
                        <option value="2">超过时间限制(TLE)</option>
                        <option value="3">超过内存限制(MLE)</option>
                        <option value="4">答案错误(WA)</option>
                        <option value="5">运行时错误(RE)</option>
                        <option value="6">输出内容超限(OLE)</option>
                        <option value="7">编译失败(CE)</option>
                        <option value="8">系统错误(SE)</option>
                        <option value="9">等待重判</option>
                        <option value="10">特殊评测超时</option>
                        <option value="11">特殊评测程序错误</option>
                        <option value="12">特殊评测完成</option>
                        <option value="20">等待人工评判</option>
                        <option value="-1">评测中</option>
                        <option value="-2">队列中</option>
                    </core.forms.SelectField>
                </section>
            : <section></section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="编辑状态" size="small" btnTitle="保存">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="保存成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}
