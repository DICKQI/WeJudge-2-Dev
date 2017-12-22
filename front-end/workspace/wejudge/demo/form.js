
class AsgnProblemSetting extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.state = {
            entity: null
        };
    }

    doSubmitSuccess(rel){
    this.refs.alertbox.showSuccess(rel, function () {
        window.location.reload();
    });
}

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    componentDidMount() {
        var that = this;
        this.getData(function (rel) {
            that.setState({
                entity: rel.data
            });
        }, function (rel, msg) {
            that.refs.alertbox.showError(rel, msg);
        });
    }

    render(){
        var formBody = this.renderForm(
            this.state.entity ? <section>

            </section> : null
        );
        return (
            <div className="ui">
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}