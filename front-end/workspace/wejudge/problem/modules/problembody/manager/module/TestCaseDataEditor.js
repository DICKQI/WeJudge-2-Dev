/**
 * Created by lancelrq on 2017/3/19.
 */

module.exports = TestCaseDataEditor;

var React = require('react');
var core = require('wejudge-core');


class TestCaseDataEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            entity: {},
            data: {}
        };
        this.apis = {
            submit: this.props.apis.submit,
            data: this.props.apis.data
        };
    }

    show(entity){
        var that = this;
        this.setState({
            entity: entity
        });
        this.apis = {
            submit: this.props.apis.submit+ "?handle=" + entity.handle,
            data: this.props.apis.data+ "?handle=" + entity.handle
        };
        this.getData(function (rel) {
            that.setState({
                data: rel.data
            });
            that.refs.FormDialog.show(function () {
                that.submit();
                return false;
            });
        },function (rel, msg) {
            that.refs.alertbox.showError(rel, msg);
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {});
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    render(){
        var formBody = this.renderForm(
            <section>
                <input type="hidden" name="handle" value={this.state.entity.handle || ""} />
                <div className="ui two columns grid">
                    <div className="column">
                        <core.forms.TextAreaField label="输入" name="input" rows={20} required value={this.state.data.input || ""} />
                    </div>
                    <div className="column">
                        <core.forms.TextAreaField label="输出" name="output" rows={20} required value={this.state.data.output || ""} />
                    </div>
                </div>
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog size="large" ref="FormDialog" title="编辑测试数据内容">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="测试数据保存成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}