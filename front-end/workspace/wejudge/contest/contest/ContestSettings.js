/**
 * Created by lancelrq on 2017/4/1.
 */

var React = require("react");
var moment = require("moment");
var core = require("wejudge-core");


module.exports = ContestSettings;

class ContestSettings extends core.forms.FormComponent {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            entity: null
        };
        this.apis = {
            data: props.apis.get_settings,
            submit: props.apis.save_settings
        };
        this.LangList = core.LangList;
        this.confirmRank = this.confirmRank.bind(this);
        this.refreshData = this.refreshData.bind(this);
    }

    load(){
        var that = this;
        this.getData(function (rel) {
            that.setState({
                entity: rel.data
            });
        }, function (rel, msg) {
            that.refs.alertbox.showError(rel, msg);
        });
    }

    doSubmitSuccess(rel){
        this.refs.alertbox.showSuccess(rel, function () {
            window.location.reload();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    confirmRank(){
        var that = this;
        that.refs.confirm.setContent('如果参赛人数较多，确认排名操作将要花费一定的时间，操作期间请不要重复点击。是否继续？');
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.confirm_rank,
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {

                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        });
    }

    refreshData(){
        var that = this;
        that.refs.confirm.setContent('将要在后台启动比赛数据的重算工作，执行后稍等片刻即可看到结果。是否继续？');
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.refresh_data,
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {

                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        });
    }

    render(){
        var that = this;
        var languageSelected = function() {
            var lang = that.state.entity.contest.lang;

            return that.LangList.map((value, key) => {
                var checked = (!lang || lang == 0 || ((value[0] & lang) > 0));
                return (<core.forms.CheckBoxField
                    name="lang" key={key} label={value[1]} value={value[0]} checked={checked} />);
            })
        };
        var statusSelected = function() {
            var flags = that.state.entity.contest.penalty_items ? that.state.entity.contest.penalty_items.split(",") : [] ;
            var FlagList = {
                1: "PE",
                2: "TLE",
                3: "MLE",
                4: "WA",
                5: "OLE",
                6: "RE",
                7: "CE",
                10: "特判程序错误",
                11:"特判超时"
            };
            var view = [];
            for (var key in FlagList){
                var value = FlagList[key];
                var checked = flags.indexOf(key.toString()) > -1;
                view.push(
                    <core.forms.CheckBoxField
                        name="penalty_items"
                        key={key}
                        label={value}
                        value={key}
                        checked={checked} />
                );
            }
            return view
        };
        var formBody = this.renderForm(
            this.state.entity ?
                <div>
                    <div className="ui stackable grid">
                        <div className="ten wide column">
                            <h3>比赛功能设置</h3>
                            <div className="ui four inline fields secondary segment">
                                <div className="field">
                                    <core.forms.CheckBoxField
                                        name="hide_problem_title" type="toggle" label="隐藏题目标题"
                                        value="true" checked={this.state.entity.contest.hide_problem_title} />
                                </div>
                                <div className="field">
                                    <core.forms.CheckBoxField
                                        name="pause" type="toggle" label="暂停比赛"
                                        value="true" checked={this.state.entity.contest.pause} />
                                </div>
                                <div className="field">
                                    <core.forms.CheckBoxField
                                        name="enable_printer_queue" type="toggle" label="打印功能"
                                        value="true" checked={this.state.entity.contest.enable_printer_queue} />
                                </div>
                                <div className="field">
                                    <core.forms.CheckBoxField
                                        name="archive_lock" type="toggle" label="归档保护" disabled
                                        value="true" checked={this.state.entity.contest.archive_lock} />
                                </div>
                            </div>
                            <div className="two fields">
                                <div className="field">
                                    <core.forms.TextField
                                        label="比赛名称" name="title" placeholder="请输入比赛名称"
                                        required value={this.state.entity.contest.title} />
                                </div>
                                <div className="field">
                                    <core.forms.SelectField label="隐私设置" name="rank_list_show_items" value={this.state.entity.contest.rank_list_show_items}>
                                        <option value="0">不屏蔽</option>
                                        <option value="1">屏蔽真实姓名</option>
                                        <option value="2">屏蔽昵称+真实姓名</option>
                                    </core.forms.SelectField>
                                </div>
                            </div>

                            <div className="two fields">
                                <div className="field">
                                    <core.forms.DateTimeField
                                        label="比赛开始时间" name="start_time"
                                        value={this.state.entity.contest.start_time ? core.tools.format_datetime(this.state.entity.contest.start_time) : ""}/>
                                </div>
                                <div className="field">
                                    <core.forms.DateTimeField
                                        label="比赛结束时间" name="end_time"
                                        value={this.state.entity.contest.end_time ? core.tools.format_datetime(this.state.entity.contest.end_time) : ""}/>
                                </div>
                            </div>
                            <div className="two fields">
                                <div className="field">
                                    <core.forms.DateTimeField
                                        label="封榜时间（不填写视作不启用）" name="rank_list_stop_at"
                                        value={this.state.entity.contest.rank_list_stop_at ? core.tools.format_datetime(this.state.entity.contest.rank_list_stop_at) : ""}/>
                                </div>
                                <div className="field">
                                    <core.forms.TextField
                                        label="错题罚时(秒)" name="penalty_time" placeholder="1200"
                                        value={this.state.entity.contest.penalty_time} />
                                </div>
                            </div>
                            <div className="two fields">
                                <div className="field">
                                    <core.forms.TextField
                                        label="数据令牌(用于比赛工具的只读访问)"
                                        name="access_token"
                                        placeholder="启用数据令牌进行比赛线下功能的只读访问，请设置相对复杂的token确保不泄露题目等信息，留空则不启用。"
                                        maxLength="100"
                                        value={this.state.entity.contest.access_token}/>
                                </div>
                                <div className="field">
                                    <core.forms.SelectField label="注册报名" name="register_mode" forceDefault value={this.state.entity.contest.register_mode}>
                                        <option value="none">禁用</option>
                                        <option value="register">使用WeJudge主账户报名</option>
                                    </core.forms.SelectField>
                                </div>
                            </div>
                            <div className="ui inline fields secondary segment">
                                <label>罚时项目：</label>
                                {statusSelected()}
                            </div>
                            <core.forms.TextAreaField
                                label="比赛主办方" name="sponsor" placeholder="比赛主办方"
                                value={this.state.entity.contest.sponsor} rows="3"/>
                            <div className="ui inline fields secondary segment">
                                <label>可用编译语言：</label>
                                {languageSelected()}
                            </div>

                        </div>
                        <div className="six wide column">
                            <h3>查重功能设置</h3>
                            <div className="two fields">
                                <core.forms.TextField
                                    label="查重率记录阈值(0.00-1.00)" name="cross_check_ratio" placeholder="0.8"
                                    value={this.state.entity.contest.cross_check_ratio} />
                                <core.forms.TextField
                                    label="查重公开信息阈值(0.00-1.00)" name="cross_check_public_ratio" placeholder="0.8"
                                    value={this.state.entity.contest.cross_check_public_ratio} />
                            </div>
                            <div className="two fields">
                                <core.forms.CheckBoxField
                                    name="cross_check" type="toggle" label="启用查重"
                                    value="true" checked={this.state.entity.contest.cross_check} />

                                <core.forms.CheckBoxField
                                    name="cross_check_public" type="toggle" label="公开查重信息"
                                    value="true" checked={this.state.entity.contest.cross_check_public} />
                            </div>
                            <table className="ui striped table">
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>题目名称</th>
                                    <th>操作</th>
                                </tr>
                                </thead>
                                <tbody>
                                {this.state.entity.problems.map((val, key) =>{
                                    return (
                                        <tr key={key}>
                                            <td>题目{core.tools.gen_problem_index(val.index)}({val.entity.id})</td>
                                            <td>{val.entity.title}</td>
                                            <td>
                                                <core.forms.CheckBoxField
                                                    name="cc_ig_problem"
                                                    type="toggle"
                                                    label="禁用查重"
                                                    value={val.id}
                                                    checked={this.state.entity.contest.cross_check_ignore_problem.indexOf(val.id) > -1}
                                                />
                                            </td>
                                        </tr>
                                    );
                                })}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <core.forms.CKEditorField height="30em" label="比赛介绍" name="description" value={this.state.entity.contest.description} />
                </div>
             : null
        );
        return (
            <div className="ui">
                <div className="ui top attached menu">
                    <a className="item"><strong>比赛控制</strong></a>
                    <a className="item" onClick={this.refreshData}>排行榜重算</a>
                    <a className="item" onClick={this.confirmRank}>确认最终排行</a>
                    <a className="item" href={this.props.urls.rank_board} target="_blank">滚动排行榜</a>
                    <div className="right menu">
                        <a className={`item ${!this.state.entity && "disabled"}`} onClick={this.submit}><i className="save icon"></i>保存设置</a>
                    </div>
                </div>
                <div className="ui bottom attached segment">
                    {formBody}
                </div>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="你确定？" msg_title="操作确认" ref="confirm" />
            </div>

        );
    }
}
