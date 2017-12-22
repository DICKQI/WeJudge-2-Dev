/**
 * Created by lancelrq on 2017/2/15.
 */

module.exports = ProblemsetEditor;

var React = require('react');
var core = require('wejudge-core');


class ProblemsetEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            dialog_title: "",
            disable_image_upload: true,
            entity : {
                title: "",
                description: ""
            }
        };
    }

    createProblemSet(){
        this.apis = {
            submit: this.props.apis.create
        };
        var that = this;
        this.setState({
            dialog_title: "创建题集",
            disable_image_upload: true
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    modifyProblemSet(psid){
        this.apis = {
            submit: this.props.apis.modify.replace("problemset/0", "problemset/" + psid),
            data: this.props.apis.data.replace("problemset/0", "problemset/" + psid),
            upload_image: this.props.apis.upload_image.replace("problemset/0", "problemset/" + psid)
        };
        var that = this;
        this.setState({
            dialog_title: "编辑题集",
            disable_image_upload: false
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
            that.manager.load();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var UploadArea = null;
        if(!this.state.disable_image_upload)
            UploadArea = <core.forms.ImageField label="封面" name="image" upload_api={this.apis.upload_image} />;
        var formBody = this.renderForm(
            <section>
                <core.forms.TextField label="名称" name="title" placeholder="请输入题目集名称" required value={this.state.entity.title} />
                { UploadArea }
                <core.forms.TextAreaField label="说明" name="description" placeholder="请输入题目集说明" value={this.state.entity.description} />
                <div className="ui segment">
                    <div className="three fields">
                        <core.forms.RadioField
                            name="private" type="toggle" label="公开题库" value="0" checked={this.state.entity.private === 0} />
                       <core.forms.RadioField
                            name="private" type="toggle" label="共享题库" value="1" checked={this.state.entity.private === 1} />
                       <core.forms.RadioField
                            name="private" type="toggle" label="私有题库" value="2" checked={this.state.entity.private === 2} />
                    </div>
                    <i className="info icon"></i>共享题库权限为：拥有发布题目和创建题目集权限者可以访问。
                </div>
                <div className="ui segment">
                    <core.forms.CheckBoxField
                        name="publish_private" type="toggle" label="禁止他人推送题目到此题库" value="true" checked={this.state.entity.publish_private} />
                </div>
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" size="small" title={this.state.dialog_title}>
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}