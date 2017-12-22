/**
 * Created by lancelrq on 2017/4/16.
 */


var React = require("react");
var core = require("wejudge-core");

module.exports = ContestCrossCheck;


class ContestCrossCheck extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.state['is_admin'] = props.is_admin || false;
    }

    load(){
        this.refs.listView.getListData();
    }


    render() {
        var that = this;
        return (
            <div className="ui">
                <ContestCrossCheckList
                    ref="listView"
                    crosscheck_list={this.props.apis.crosscheck_list}
                    delete_record={this.props.apis.delete_record}
                    manager={this}
                    is_admin={this.state.is_admin}
                    table_style="celled structuredstriped"
                    view_problem={this.props.urls.view_problem}
                    view_detail={this.props.urls.view_detail}
                    read_code={this.props.apis.read_code}
                />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="你确定要删除这条记录吗？" msg_title="操作确认" ref="confirm" />
            </div>
        )
    }
}

class ContestCrossCheckList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.manager = props.manager;
        this.apis = {
            data: props.crosscheck_list
        };
        this.deleteRecord = this.deleteRecord.bind(this);
        this.showRead = this.showRead.bind(this);
    }

    showRead(id){
        var that = this;
        return function(){
            that.refs.CodeView.show(id);
        }
    }
    deleteRecord(id){
        var that = this;
        return function () {
            that.manager.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.delete_record + "?id=" + id,
                        method: "GET",
                        success: function (rel) {
                            that.manager.refs.alertbox.showSuccess(rel, function () {
                                that.manager.refs.listView.getListData();
                            });
                        },
                        error: function (rel, msg) {
                            that.manager.refs.alertbox.showError(rel, msg);
                        }
                    }).call()
                }
            });
        }
    }

    renderListHeader(){
        return [
                <tr className="center aligned" key="tr_1">
                    <th rowSpan="2">编号</th>
                    <th rowSpan="2">题目</th>
                    <th colSpan="2">评测历史</th>
                    <th colSpan="2">评测历史</th>
                    <th rowSpan="2">levenshtein相似度</th>
                    {this.props.is_admin ? <th rowSpan="2">管理</th> : null}
                </tr>,
                <tr className="center aligned" key="tr_2">
                    <th style={{borderLeft: "1px solid rgba(34,36,38,.1)"}}>ID</th>
                    <th>提交</th>
                    <th>ID</th>
                    <th>提交者</th>
                </tr>
        ];
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key} className="center aligned">
                        <td>#{item.id}</td>
                        <td>
                            <a target="_blank" href={this.props.view_problem.replace("problem/0", "problem/"+item.problem.id)}>
                            题目 {core.tools.gen_problem_index(item.problem.index)}
                            </a>
                        </td>
                        <td>
                            <a target="_blank" href={this.props.view_detail.replace("status/0", "status/"+item.source.id)}>
                            {item.source.id}
                            </a>
                        </td>
                        <td>{item.source.author.username}<br />{item.source.author.realname}</td>
                        <td>
                            <a target="_blank" href={this.props.view_detail.replace("status/0", "status/"+item.target.id)}>
                                {item.target.id}
                            </a>
                        </td>
                        <td>{item.target.author.username}<br />{item.target.author.realname}</td>
                        <td>{(item.levenshtein_similarity_ratio * 100).toFixed(3)} %</td>
                        {this.props.is_admin ? <td>
                            <a className="ui tiny primary button" onClick={this.showRead(item.id)}>查看</a>
                            <a className="ui tiny red button" onClick={this.deleteRecord(item.id)}>删除</a>
                        </td> : null }
                    </tr>
                )
            });
        else
            return null
    }

    renderFooterBody () {
        return <div>
            <ContestCrossCheckCode
                ref="CodeView"
                read_code={this.props.read_code}
            />
        </div>
    }
}
class ContestCrossCheckCode extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.read_code
        };
        this.state= {
            data: {
                source: {},
                target: {}
            }
        };
        this.show = this.show.bind(this);
    }

    show(id) {
        core.restful({
            method: 'GET',
            responseType: "json",
            url: this.apis.data + "?id=" + id,
            success: (rel) => {
                this.setState({
                    data: rel.data
                }, () => {
                    this.refs.CodeDialog.show();
                });
            },
            error: (rel, msg) => {
                alert("加载失败: " + msg);
            }
        }).call();

    }

    render() {
        var data = this.state.data;
        return (
            <core.dialog.Dialog ref="CodeDialog" title="代码对比" size="large" btnShow={false}>
                <div className="ui two columns grid">
                    <div className="column">
                        <core.forms.CodeMirrorField key="code_1" lang={0} label={`评测历史(${data.source.status_id})`} value={data.source.code} />
                    </div>
                    <div className="column">
                        <core.forms.CodeMirrorField key="code_2" lang={0} label={`评测历史(${data.target.status_id})`} value={data.target.code} />
                    </div>
                </div>
            </core.dialog.Dialog>
        );
    }
}
