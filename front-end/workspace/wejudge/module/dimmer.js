/**
* Created by lancelrq on 2017/3/10.
*/

var React = require('react');

module.exports = {
    Messager: Messager,
    Loader: Loader,
    FormMessager: FormMessager
};


class Loader extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            messageTitle: props.title || "加载中",
            inverted: props.inverted ? "inverted" : ""
        };
        this.hide = this.hide.bind(this);
        this.setTitle = this.setTitle.bind(this);
    }
    hide(){
        $(this.refs.Dimmer).dimmer('hide');
    }
    show(){
        $(this.refs.Dimmer).dimmer({
            closable: false
        }).dimmer('show');
    }

    setTitle(title){
        this.setState({
            messageTitle: title,
        })
    }

    componentDidMount() {
        $(this.refs.Dimmer).dimmer('hide');
    }

    render(){
        return (
            <div className={"ui "+ this.state.inverted +" dimmer"} ref="Dimmer">
                <div className="ui text loader">{this.state.messageTitle}...</div>
            </div>
        );
    }
}

class FormMessager extends React.Component {

    // 构造
    constructor(props) {

        super(props);
        // 初始状态
        this.state = {
            messageType: props.type || "info",
            messageTitle: props.title || "",
            messageBody:  props.body ||"",
            messageStatus: "hidden"
        };
        this.hide = this.hide.bind(this);
    }


    hide(){
        this.setState({ messageStatus: "hidden" });
    }

    show(title, content, type="info"){
        this.setState({
            messageType: type,
            messageTitle: title,
            messageBody: content,
            messageStatus: "visible"
        })
    }

    render(){
        return (
            <div className={"ui "+this.state.messageStatus+" "+ this.state.messageType +" message"}>
                <i className="close icon" onClick={this.hide}></i>
                <div className="content">
                    <div className="header">{this.state.messageTitle}</div>
                    {this.state.messageBody}
                </div>
            </div>
        )
    }
}

class Messager extends React.Component {

    // 构造
    constructor(props) {

        super(props);
        // 初始状态
        this.state = {
            messageType: props.type || "",
            messageTitle: props.title || "",
            messageBody: props.body || "",
            inverted: props.inverted ? "inverted" : ""
        };
        this.onRetry = this.onRetry.bind(this);
    }

    hide() {
       $(this.refs.Dimmer).dimmer("hide");
    }

    show(title, content, type = "info") {
        var micon = "";
        switch (type) {
            case "info":
                micon = "info circle";
                break;
            case "warning":
                micon = "warning circle";
                break;
            case "error":
                micon = "remove circle";
                break;
            case "success":
                micon = "check circle";
                break;
            case "help":
            default:
                micon = "help circle";
        }
        this.setState({
            messageIcon: micon,
            messageTitle: title || "",
            messageBody: content || ""
        });
        $(this.refs.Dimmer).dimmer({
            closable: false
        }).dimmer("show");
    }

    componentDidMount() {
        var that = this;
        $(this.refs.RetryBtn).click(function () {
            that.onRetry();
        })
    }

    onRetry() {
        this.hide();
        if (typeof this.props.retry === "function")
            this.props.retry()
    }

    render() {
        var retry = (this.props.retry) ? (<a href="javascript:void(0)" ref="RetryBtn" >重试</a>) : "";
        return (
            <div className={"ui " + this.state.inverted +" dimmer"} ref="Dimmer">
                <h1><i className={this.state.messageIcon + " icon"}></i></h1>
                <h3>{this.state.messageTitle}</h3>
                <h4>{this.state.messageBody}</h4>
                {retry}
            </div>
        );
    }
}
