/**
 * Created by lancelrq on 2017/4/5.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = ContestListPage;


class ContestListPage extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.state['is_admin'] = props.is_admin || false;
        this.showCreate = this.showCreate.bind(this);
        this.deleteContest = this.deleteContest.bind(this);
    }

    componentDidMount() {
        this.refs.ContestList.load();
    }
    showCreate(){
        this.refs.editor.show();
    }

    deleteContest(id){
        var that = this;
        return function () {
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.delete_contest + "?id=" + id,
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                window.location.reload();
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
    
    render() {
        return (
            <div className="ui">
                {this.state.is_admin ?
                    <div className="ui">
                        <div className="ui compact menu">
                            <a className="item" onClick={this.showCreate}><i className="add icon"></i> 创建比赛</a>
                        </div><br /><br />
                    </div>
                     : null
                }
                <ContestList
                    contest_list={this.props.apis.contest_list}
                    contest_view={this.props.urls.contest_view}
                    stackable
                    ref="ContestList"
                />
                <CreateContest
                    create_contest={this.props.apis.create_contest}
                    ref="editor"
                />
                <core.dialog.Confirm msg="你确定要删除这个比赛吗？所有信息都将损坏，并且不可找回！" msg_title="操作确认" ref="confirm" />
            </div>
        );
    }
}


class ContestList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.contest_list
        }
    }

    renderListHeader(){
        return (
            <tr>
                <th>比赛名称</th>
                <th width="20%">比赛开始时间</th>
                <th width="20%">比赛结束时间</th>
            </tr>
        );
    }
    renderListItems(){
        var status_color = {
            "-1": "gray",
            0: "green",
            1: "red"
        };
        var status_call = {
            "-1": "未开始",
            0: "进行中",
            1: "已结束"
        };
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                var sponsor = item.sponsor ? item.sponsor.split('\n')[0] : "";
                return (
                    <tr key={key}>
                        <td>
                            <span className={`ui ribbon ${status_color[item.status]} label`}>
                                {status_call[item.status]}
                            </span>
                            <span className="ui header">
                                <a href={this.props.contest_view.replace('contest/0', 'contest/'+ item.id)}>
                                    {item.title}
                                </a>
                                {sponsor ?
                                    <span className="sub header" style={{paddingLeft: "2.5em", marginLeft: "2.5em"}}>
                                    主办单位：{sponsor}
                                    </span>
                                : null }
                            </span>
                        </td>
                        <td>{item.start_time}</td>
                        <td>{item.end_time}</td>
                    </tr>
                );
            });
        else
            return null
    }

}

class CreateContest extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
        };
        this.apis = {
            submit: props.create_contest
        }
    }

    show(){
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            window.location.reload();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            <section>
                <core.forms.TextField
                    label="比赛名称" name="title" required placeholder="请输入比赛名称" />
                <div className="two fields">
                    <div className="field">
                        <core.forms.TextField
                            label="比赛开始时间" name="start_time" placeholder="YYYY-MM-DD HH:mm:SS" required />
                    </div>
                    <div className="field">
                        <core.forms.TextField
                            label="比赛结束时间" name="end_time" placeholder="YYYY-MM-DD HH:mm:SS" required />
                    </div>
                </div>
                <core.forms.TextAreaField
                    label="比赛主办方" name="sponsor" placeholder="比赛主办方" rows="3"/>
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title={this.state.dialog_title} size="small" btnTitle="保存">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="创建成功" msg="比赛创建成功！初始账户为admin，密码为您当前账户的密码！" />
            </div>

        );
    }

}