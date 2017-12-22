/*
* Created by lancelrq on 2017/8/4.
*/

var React = require("react");
var core = require("wejudge-core");

module.exports = AccountCard;


class AccountCard extends React.Component{

    // 构造
    constructor(props) {
        super(props);
        this.state = {
            data: null,
            err_message: "",
            app_name: "master",
            account_id: ""
        };
        this.apis = {
            data: "",
            view: ""
        };
        // 初始状态
        this.show = this.show.bind(this);
        this.hide = this.hide.bind(this);
    }

    getData(url, params){
        var that = this;
        this.refs.loader.show();
        var core = require('wejudge-core');
        core.restful({
            method: 'GET',
            data: params || null,
            responseType: "json",
            url: url,
            success: function (rel) {
                that.refs.loader.hide();
                that.setState({
                    data: rel.data
                }, function () {
                    $(that.refs.ModelBox).modal('refresh');
                });

            },
            error: function (rel, msg) {
                that.refs.loader.hide();
                that.setState({
                    err_message: msg
                });
                return false;
            }
        }).call();
    }

    show(app_name, account_id){
        var that = this;
        var url = window.wejudge.global.account[app_name].account_info_api.replace("space/0", "space/"+account_id);
        this.getData(url);
        this.setState({
            data: null,
            app_name: app_name,
            account_id: account_id
        });
        $(that.refs.ModelBox).modal({
            allowMultiple: true,
            closable: false,
            inverted: true,
            transition: "fade up",
        }).modal("show", function () {

        });
    }

    hide(){
        $(this.refs.ModelBox).modal("hide");
    }

    render(){
        var pv_id = {
            'master': "problem_visited",
            'education': "solution_visited",
            'contest': "solution_visited"
        };
        var url = window.wejudge.global.account[this.state.app_name].account_space_view || null;
        var avator_url = window.wejudge.global.account[this.state.app_name].account_space_avator || null;
        return (
            <div>
                <div className="ui mini inverted modal" ref="ModelBox">
                    <i className="black close icon"></i>
                    <div className="header">
                        用户信息
                    </div>
                    <div className="content" style={{minHeight: 140}}>
                        <core.dimmer.Loader inverted ref="loader"/>
                        {this.state.data ? <div className="ui card user_card">
                            <div className="user_card_image">
                                <img
                                    className="ui centered circular image"
                                    width="120" height="120"
                                    src={this.state.data ? avator_url.replace('space/0', 'space/' + this.state.data.id) : avator_url} />
                            </div>
                            <div className="content user_card_content">
                                <a className="header">{this.state.data.nickname}</a>
                                <div className="meta">
                                    <span className="date">@{this.state.data.username}</span>
                                </div>
                                <br />
                                <div className="description">
                                    {this.state.data.motto || "这人很懒，什么也没写..."}
                                </div>
                                <div className="ui two tiny statistics user_card_statistics">
                                    <div className="statistic">
                                        <div className="value">
                                            {this.state.data[pv_id[this.state.app_name]].solved}
                                        </div>
                                        <div className="label">
                                            通过题目
                                        </div>
                                    </div>
                                    <div className="statistic">
                                        <div className="value">
                                            {this.state.data[pv_id[this.state.app_name]].total}
                                        </div>
                                        <div className="label">
                                            访问题目
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div> : null}
                        {this.state.err_message ?
                        <div className="ui error icon message">
                            <i className="remove circle icon"></i>
                            <div className="content">
                                <div className="header">哎呀，出错了！</div>
                                {this.state.err_message}
                            </div>
                        </div> : null}
                    </div>
                    <div className="extra content">
                        <a
                            href={url ? url.replace("space/0", 'space/' + this.state.account_id) : ""}
                            className="ui fluid huge blue button"
                            target="_blank"
                            onClick={this.hide}
                        >
                            <i className="send icon"></i>
                            个人空间
                        </a>
                    </div>
                </div>
            </div>
        )
    }
}
