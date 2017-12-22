/**
 * Created by lancelrq on 2017/2/15.
 */

module.exports = DemoCaseEditor;

var React = require('react');
var core = require('wejudge-core');


class DemoCaseEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            dialog_title: "",
            entity: {},
            lang: 1
        };
        this.apis = {
            submit: this.props.apis.submit
        };
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            lang: nextProps.lang || 1
        })
    }

    show(entity, code){
        var that = this;
        this.setState({
            dialog_title: "编辑填空区设置",
            entity: entity,
            code: code
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.getJudgeConfig();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            <section>
                <input type="hidden" name="is_new" value={false} />
                <input type="hidden" name="lang" value={this.state.lang} />
                <input type="hidden" name="handle" value={this.state.entity.handle || ""} />
                <core.forms.TextField label="名称" name="name" required value={this.state.entity.name || ""} />
                <core.forms.CodeMirrorField label="参考答案" name="code"  lang={this.state.lang} value={this.state.code} />
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title={this.state.dialog_title}>
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}