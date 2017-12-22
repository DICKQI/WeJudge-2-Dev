/**
 * Created by lancelrq on 2017/2/15.
 */

module.exports = TestCaseEditor;

var React = require('react');
var core = require('wejudge-core');


class TestCaseEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            dialog_title: "",
            entity: {},
            is_new: false
        };
        this.apis = {
            submit: this.props.apis.submit
        };
    }

    create(){
        var that = this;
        this.setState({
            dialog_title: "创建测试数据",
            is_new: true,
            entity: {}
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    modify(entity){
        var that = this;
        this.setState({
            dialog_title: "编辑测试数据设置",
            entity: entity,
            is_new: false
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
                <input type="hidden" name="is_new" value={this.state.is_new} />
                <input type="hidden" name="handle" value={this.state.entity.handle || ""} />
                <core.forms.TextField label="名称" name="name" placeholder="请输入测试数据名称, 不填自动生成" required value={this.state.entity.name || ""} />
                <core.forms.RangeField label="比重" width="80%" step={5} label_value name="score_precent" max={100} min={0} value={this.state.entity.score_precent || 0} />
                <core.forms.CheckBoxField type="toggle" label="测试数据参与评测" name="available" checked={this.state.entity.available || true} value="true" />
                <core.forms.CheckBoxField type="toggle" label="测试数据公开" name="visible" checked={this.state.entity.visible}  value="true" />
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog  ref="FormDialog" title={this.state.dialog_title} size="mini">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}

// <core.forms.CheckBoxField type="toggle" label="测试数据可用于预评测" name="pre_judge" checked={this.state.entity.pre_judge}  value="true" />

