/**
 * Created by lancelrq on 2017/7/25.
 */

module.exports = ProblemRelations;

var React = require('react');
var core = require('wejudge-core');

var ProblemsetList = require("../problemset/ProblemsetList").ProblemsetList;


class ProblemRelations extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {

        };
        this.psetClick = this.psetClick.bind(this);
        this.removeProblem = this.removeProblem.bind(this);
    }

    psetClick(pset){
        var that = this;
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.publish_problem.replace("problemset/0", 'problemset/' + pset.id),
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            that.refs.relation_list.load();
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call();
            }
        });
    }

    removeProblem(psid){
        var that = this;
        return function () {
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.remove_problem.replace("problemset/0", "problemset/" + psid),
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.refs.relation_list.load();
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


    componentDidMount() {
        this.refs.relation_list.load();
        this.refs.problemset_list.load();
    }

    render() {
        var that = this;
        return (
            <div className="ui">
                <div className="ui black segment">
                    <h3>题目集关联</h3>
                    <ProblemRelationsList
                        ref="relation_list"
                        remove={this.removeProblem}
                        relations_list={this.props.apis.get_relations}
                    />
                </div>
                <div className="ui black segment">
                    <h3>点击题目集链接，向其推送此题目</h3>
                    <ProblemsetList
                        ref="problemset_list"
                        apis={{
                            list_problemset: this.props.apis.list_problemset
                        }}
                        urls={{}}
                        options={{readonly: true}}
                        psetClick={this.psetClick}
                    />
                </div>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm  ref="confirm"  msg_title="操作确认" msg="你确定要执行当前操作吗？" />
            </div>
        )
    }
}


class ProblemRelationsList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.relations_list
        }
    }

    renderListHeader() {
        return (
            <tr>
                <th>#ID</th>
                <th>题目集名称</th>
                <th>管理员</th>
                <th>私有题库</th>
                <th>禁止推送题目</th>
                <th>操作</th>
            </tr>
        );
    }

    renderListItems() {
        if (this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return <tr key={key}>
                    <td>{item.id}</td>
                    <td>{item.title}</td>
                    <td>{item.manager.nickname}</td>
                    <td>{item.private ? "是" : "不是"}</td>
                    <td>{item.publish_private ? "是" : "不是"}</td>
                    <td><a className="ui red compact button" onClick={this.props.remove(item.id)}>移除</a></td>
                </tr>
            });
        else
            return <tr colSpan="6">
                <td>此题目属于私有状态，暂未被任何题库收录</td>
            </tr>
    }

}