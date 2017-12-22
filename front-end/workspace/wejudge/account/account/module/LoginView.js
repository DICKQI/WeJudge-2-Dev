/**
 * Created by lancelrq on 2017/8/24.
 */

var React = require('react');
var core = require('wejudge-core');
var MasterAccountLoginView = require("./MasterAccountLoginView");
var ContestAccountLoginView = require("./ContestAccountLoginView");
var EducationAccountLoginView = require("./EducationAccountLoginView");

module.exports = LoginView;

class LoginView extends React.Component{

    constructor(props) {
        super(props);
        this.state = {
            app_name: props.app_name,
            hide_master: props.hide_master
        };
        this.APP_CALL = {
            master: "WeJudge账户",
            contest: "比赛账户",
            education: "教学账户"
        };
        this.submitBackend = props.app_name;
        this.submit = this.submit.bind(this);
        this.randNum = parseInt(Math.random() * 1000);
    }

    componentDidMount() {
        this.bindNav();
    }

    componentDidUpdate() {
        this.bindNav();
    }

    bindNav(){
        var that = this;
        if(!this.refs.LVNav) return;
        $(this.refs.LVNav).find('.item').tab({
            onLoad: function () {
                var tab_name = $(this).attr("data-tab");
                if(tab_name === 'tab_user' + that.randNum){
                    that.submitBackend = that.props.app_name;
                }else{
                    that.submitBackend = "master";
                }
            }
        });
    }

    show() {
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    submit(){
        this.refs[this.submitBackend + "_frontend"] && this.refs[this.submitBackend + "_frontend"].submit();
    }

    renderLoginView(){
        return (
            <section>
                {!this.state.hide_master ? <div className="ui secondary pointing menu" ref="LVNav">
                    <a className="active item" data-tab={"tab_user" + this.randNum}>{this.APP_CALL[this.state.app_name]}</a>
                    {this.state.app_name != 'master' ? <a className="item" data-tab={"tab_master" + this.randNum}>主账户 </a> : null}
                </div> : null}
                <div className="ui tab active" data-tab={"tab_user" + this.randNum} style={{margin: "10px"}}>
                    {   this.state.app_name == 'contest' ?
                        <ContestAccountLoginView ref="contest_frontend" dialog={this.props.dialog} afterSuccess={this.props.afterSuccess} />
                        : this.state.app_name == 'education' ?
                            <EducationAccountLoginView ref="education_frontend" dialog={this.props.dialog} afterSuccess={this.props.afterSuccess} />
                            : <MasterAccountLoginView ref="master_frontend" dialog={this.props.dialog} afterSuccess={this.props.afterSuccess}/>
                    }
                </div>
                {!this.state.hide_master && this.state.app_name != 'master' ?
                    <div className="ui tab" data-tab={"tab_master" + this.randNum} style={{margin: "10px"}}>
                        <MasterAccountLoginView dialog={this.props.dialog} ref="master_frontend" afterSuccess={this.props.afterSuccess}/>
                    </div>
                    : null}
            </section>
        )
    }

    render() {
        if(this.props.dialog)
            return (
                <section>
                    <core.dialog.Dialog ref="FormDialog" title="登录WeJudge" btnTitle="登录" size="mini">
                        {this.renderLoginView()}
                    </core.dialog.Dialog>
                </section>
            );
        else
            return this.renderLoginView()
    }
}

