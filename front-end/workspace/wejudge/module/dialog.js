/**
 * Created by lancelrq on 2017/1/15.
 */

var React = require('react');

module.exports = {
    Dialog: Dialog,
    Alert: Alert,
    Confirm: Confirm
};

class Dialog extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            data: props.data
        };
        this.show = this.show.bind(this);
        this.hide = this.hide.bind(this);
        this.refresh = this.refresh.bind(this);
    }
    refresh(){
        $(this.refs.ModelBox).modal('refresh');
    }
    show(ok_callback, close_callback, show_callback){
        var that = this;
        $(this.refs.ModelBox).modal({
            allowMultiple: true,
            closable: this.props.auto_close || false,
            observeChanges: true,
            transition: this.props.transition,
            onApprove: function () {
                if(typeof ok_callback === 'function')
                    return ok_callback();
            },
            onDeny: function () {
                if(typeof close_callback === 'function')
                    return close_callback();
            },
            onVisible: function () {
                that.refresh()
            }
        }).modal("show", function () {
            if(typeof show_callback === 'function')
                show_callback();
        });
    }
    hide(callback){
        $(this.refs.ModelBox).modal("hide", function () {
            if(typeof callback === 'function')
                callback();
        });
    }
    render(){
        var btnDisplay = this.props.btnShow ? 'inline-block' : 'none';
        return (
            <div className={"ui "+ this.props.size +" modal"} ref="ModelBox">
                <div className="header">
                    {this.props.title}
                </div>
                <div className="content">
                    {this.props.children}
                </div>
                <div className="actions">
                    <div className="ui default deny button">
                        关闭
                    </div>
                    <div className={"ui " + this.props.btnColor +" approve button"} style={{display: btnDisplay}}>
                        {this.props.btnTitle}
                    </div>
                </div>
            </div>
        );
    }
}
Dialog.defaultProps = {
    data: {},
    title: '模态框',                             //模态框标题
    size: 'middle',                              //模态框大小
    transition: 'scale',                       // 动画
    btnShow: true,
    btnColor: 'primary',                        //默认按钮颜色
    btnTitle: '确定'                            //默认按钮文字,
};

class Alert extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: props.data,
            msg: props.msg || "",
            msg_title: props.msg_title || "",
            icon: props.icon || "warning sign",
            color: props.color || "yellow"
        };
        this.showError = this.showError.bind(this);
        this.showSuccess = this.showSuccess.bind(this);
        this.hide = this.hide.bind(this);
    }
    show(callback){
        $(this.refs.AlertModelBox).modal({
            closable: true,
            observeChanges: true,
            onHide: function () {
                if(typeof callback === 'function')
                    return callback();
            }
        }).modal("show");
    }
    showSuccess(rel, callback){
        this.setState({icon: "check circle"});
        this.setState({color: "green"});
        this.setState({
            msg_title:  this.props.msg_title || "处理成功",
            msg: rel.msg || this.props.msg
        });
        $(this.refs.AlertModelBox).modal({
            closable: true,
            observeChanges: true,
            onHide: function () {
                if(typeof callback === 'function')
                    return callback();
            }
        }).modal("show");
    }
    showError(rel, msg, callback) {
        this.setState({icon: "warning sign"});
        this.setState({color: "yellow"});
        this.setState({msg: msg || this.props.msg});
        if(rel !== null)
            this.setState({msg_title: "操作有误"});
        else
            this.setState({msg_title:  "网络请求错误"});
        $(this.refs.AlertModelBox).modal({
            // blurring: true,
            closable: true,
            observeChanges: true,
            onHide: function () {
                if(typeof callback === 'function')
                    return callback();
            }
        }).modal("show");
    }

    hide() {
        $(this.refs.AlertModelBox).modal("hide");
    }
    render() {
        return (
            <div className="ui basic modal" ref="AlertModelBox">
                <div className="ui icon header">
                    <i className={this.state.icon + " "+ this.state.color+" icon"}></i>
                    {this.state.msg_title}
                </div>
                <div className="content" style={{textAlign: "center"}}>
                    <p>{this.state.msg}</p>
                </div>
                <div className="actions">
                    <div className={"ui ok "+ this.state.color+" basic approve button"}>
                        <i className="checkmark icon"></i>
                        确定
                    </div>
                </div>
            </div>
        );
    }
}


class Confirm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            msg: props.msg || "",
            msg_title: props.msg_title || "",
            icon: props.icon || "warning sign",
            color: props.color || "yellow"
        };
        this.show = this.show.bind(this);
        this.hide = this.hide.bind(this);
    }

    setContent(msg, msg_title){
        this.setState({
            msg: msg || this.state.msg,
            msg_title: msg_title || this.state.msg_title
        });
        return this;
    }

    show(callback){
        $(this.refs.ConfirmModelBox).modal({
            closable: true,
            observeChanges: true,
            onApprove: function () {
                if(typeof callback === 'function')
                    return callback(true);
            },
            onDeny: function () {
                if(typeof callback === 'function')
                    return callback(false);
            }
        }).modal("show");
    }

    hide() {
        $(this.refs.ConfirmModelBox).modal("hide");
    }
    render() {
        return (
            <div className="ui basic modal" ref="ConfirmModelBox">
                <div className="ui icon header">
                    <i className={this.state.icon + " "+ this.state.color+" icon"}></i>
                    {this.state.msg_title}
                </div>
                <div className="content" style={{textAlign: "center"}}>
                    <p>{this.state.msg}</p>
                </div>
                <div className="actions">
                    <div className="ui deny red basic button">
                        <i className="remove icon"></i>
                        否
                    </div>
                    <div className={"ui ok green basic approve button"}>
                        <i className="checkmark icon"></i>
                        是
                    </div>
                </div>
            </div>
        );
    }
}