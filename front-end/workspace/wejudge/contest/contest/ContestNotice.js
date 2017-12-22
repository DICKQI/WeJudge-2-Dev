
var React = require("react");
var core = require("wejudge-core");


module.exports = ContestNotice;

class ContestNotice extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.notice_list
        };
        this.showCreate = this.showCreate.bind(this);
        this.deleteNotice = this.deleteNotice.bind(this);
    }

    showCreate(){
        this.refs.editor.create();
    }

    deleteNotice(nid){
        var that = this;
        return function () {
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.delete_notice + "?nid=" + nid,
                        method: "GET",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.getData();
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
    renderBody() {
        var notice_list = this.state.data;

        return (
            <div className="ui">
                {notice_list.length > 0 ? <div className="ui feed segment"  style={{marginTop:0}}>
                    {notice_list.map((item, key)=> {
                        return <div className="event" key={key}>
                            <div className="label">
                                <img src={item.author.headimg || "/static/images/user_placeholder.png"}/>
                            </div>
                            <div className="content">
                                <div className="summary">
                                    <a>{item.author.nickname}</a> 发布了公告
                                    <div className="date">
                                        {core.tools.format_datetime(item.create_time)}
                                    </div>
                                </div>
                                <div className="extra text" dangerouslySetInnerHTML={{__html: item.content }}></div>
                                {this.props.is_admin ? <div className="meta">
                                    <a href="javascript:void(0)" onClick={this.deleteNotice(item.id)}>
                                        <i className="remove icon"></i>删除
                                    </a>
                                </div> : null}
                            </div>
                        </div>
                    })}
                </div> :
                    <div className="ui icon message">
                        <i className="warning circle icon"></i>
                        <div className="content">
                            <div className="header">暂时没有公告哦！</div>
                        </div>
                    </div>
                }
                {this.props.is_admin ? <a className="ui tiny green button" onClick={this.showCreate}><i className="add icon"></i>发布公告</a> : null}

                <NoticeEditor ref="editor" create={this.props.apis.create_notice} manager={this}/>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="你确定要删除这条信息吗？" msg_title="操作确认" ref="confirm" />
            </div>
        );
    }
}


class NoticeEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            show: false,
            entity: {}
        };
        this.hide = this.hide.bind(this);
        this.show = this.show.bind(this);
    }

    create(){
        var that = this;
        this.apis = {
            submit: this.props.create
        };
        this.show();
    }

    show(){
        this.setState({
            show: true
        });
    }

    hide(){
        this.setState({
            show: false
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.hide();
            that.manager.getData();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            <div className="ui green segment">
                <core.forms.CKEditorField label="公告内容" name="content" value="" />
                <button className="ui green button">发布</button>
                <button type="button" onClick={this.hide} className="ui red button">取消</button>
            </div>
        );
        return (
            <div className="ui">
                {this.state.show ? formBody : null}
                <core.dialog.Alert ref="alertbox" msg_title="发布成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}