/**
 * Created by lancelrq on 2017/8/16.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = RepositoryEditor;

class RepositoryEditor extends core.forms.FormComponent {

    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            mode: "new",
            entity : {}
        };
    }

    create(){
        this.apis = {
            submit: this.props.apis.new_repo
        };
        var that = this;
        this.setState({
            mode: "new",
            dialog_title: "创建教学资源仓库",
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    modify(psid){
        this.apis = {
            submit: this.props.apis.edit_repo,
            data: this.props.apis.repo_info
        };
        var that = this;
        this.setState({
            mode: "edit",
            dialog_title: "编辑教学资源仓库",
        });
        this.getData(function (rel) {
            that.setState({
                entity: rel.data
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
        this.refs.alertbox.showSuccess(rel, function () {
            if(that.state.mode === "new")
                that.manager.load();
            else
                window.location.reload();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            <section>
                <core.forms.TextField label="名称" name="title" placeholder="请输入教学资源仓库的名称" required value={this.state.entity.title} />
                <div className="ui inline fields segment">
                    <core.forms.RadioField
                        label="私有" name="public_level"
                        value="0" checked={this.state.mode==="new" || this.state.entity.public_level===0} />
                    <core.forms.RadioField
                        label="校内公开" name="public_level"
                        value="1" checked={this.state.entity.public_level===1}
                    />
                    <core.forms.RadioField
                        label="完全公开" name="public_level"
                        value="2" checked={this.state.entity.public_level===2}
                    />
                </div>
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" size="tiny" title={this.state.dialog_title}>
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}