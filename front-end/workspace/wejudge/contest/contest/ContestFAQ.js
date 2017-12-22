
var React = require("react");
var core = require("wejudge-core");


module.exports = ContestFAQ;

class ContestFAQ extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.faq_list
        };
        this.showCreate = this.showCreate.bind(this);
        this.showReply = this.showReply.bind(this);
        this.toggleFAQ = this.toggleFAQ.bind(this);
        this.deleteFAQ = this.deleteFAQ.bind(this);
    }

    showCreate(){
        this.refs.editor.create();
    }
    showReply(entity){
        var that = this;
        return function () {
            that.refs.editor.reply(entity);
        };
    }
    toggleFAQ(fid){
        var that = this;
        return function () {
            core.restful({
                url: that.props.apis.toggle_faq + "?fid=" + fid,
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
    }
    deleteFAQ(fid){
        var that = this;
        return function () {
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.delete_faq + "?fid=" + fid,
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
        var faq_list = this.state.data;

        return (
            <div className="ui">
                {this.props.is_referee ? null : <div className="ui compact menu">
                        <a className="item" onClick={this.showCreate}>
                            <i className="add icon"></i>我要提问
                        </a>
                    </div>
                }
                {faq_list.map((item, key)=>{
                    return (
                        <div key={key} className={`ui ${item.is_private ? "black" : "blue"} segment`}>
                            <div className="ui header">
                                {item.is_private ? "" : "公开"}提问：{item.title}
                                <span className="sub header">
                                    {item.author.nickname} ({item.author.username})；
                                    提问时间：{core.tools.format_datetime(item.create_time)}
                                </span>
                            </div>
                            <div className="content">{item.content || "如题"}</div>
                            <div className="ui divider"></div>
                            { item.children.length > 0 ?
                            <div className="ui comments">
                                <div className="comments">
                                {item.children.map((reply, key)=>{
                                    return (
                                        <div key={key} className="comment">
                                            <div className="content">
                                                <a className="author">{reply.author.nickname}</a>
                                                <div className="metadata">
                                                    <span className="date">{core.tools.format_datetime(reply.create_time)}</span>
                                                </div>
                                                <div className="text">{reply.content}</div>
                                                <a className="reply" onClick={this.deleteFAQ(reply.id)}>删除</a>
                                            </div>
                                        </div>
                                    )
                                })}
                                </div>
                            </div>:null}
                            <a className="ui tiny primary button" onClick={this.showReply(item)}>回复</a>
                            {
                                this.props.is_referee ?
                                item.is_private ?
                                    <a className="ui tiny green button" onClick={this.toggleFAQ(item.id)}> 设为公开</a> :
                                    <a className="ui tiny orange button" onClick={this.toggleFAQ(item.id)}> 设为私密</a>
                                : null
                            }
                            <a className="ui tiny red button" onClick={this.deleteFAQ(item.id)}> 删除</a>
                        </div>
                    )
                })}
                <FAQEditor ref="editor" create={this.props.apis.create_faq} reply={this.props.apis.reply_faq} manager={this}/>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="你确定要删除这条信息吗？" msg_title="操作确认" ref="confirm" />
            </div>
        );
    }
}


class FAQEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            dialog_title: "",
            entity: {},
            is_new: false
        };
    }

    create(){
        var that = this;
        this.apis = {
            submit: this.props.create
        };
        this.setState({
            dialog_title: "我要提问",
            is_new: true,
            entity: {}
        });
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    reply(entity){
        var that = this;
        this.apis = {
            submit: this.props.reply
        };
        this.setState({
            dialog_title: "回复",
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
            that.manager.getData();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var is_new = this.state.is_new;
        var formBody = this.renderForm(
            <section>
                <input type="hidden" name="fid" value={this.state.entity.id || ""} />
                {is_new ? <core.forms.TextField label="提问标题" name="title" required /> : null}
                <core.forms.TextAreaField label={is_new ? "提问内容" :"回复内容"} name="content" value="" />
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title={this.state.dialog_title} size="small" btnTitle="发布">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="发布成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}