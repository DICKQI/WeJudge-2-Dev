/**
 * Created by lancelrq on 2017/4/16.
 */


var React = require("react");
var core = require("wejudge-core");

// var MyProblemList = require('../../problem/modules/problemset/MyProblemsList');

module.exports = ContestProblemChoose;


class ContestProblemChoose extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.chooseProblem = this.chooseProblem.bind(this);
    }

    chooseProblem(item){
        var that = this;
        core.restful({
            url: that.props.apis.add_problem,
            data:{
                id: item.id
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {});
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }

    load() {
        this.refs.listView.getListData();
    }

    render() {
        var that = this;
        return (
            <div className="ui">
                <MyProblemList
                    ref="listView"
                    apis={{list_my_problems: this.props.apis.list_my_problems}}
                    urls={{
                        view_problem: this.props.urls.view_problem,
                        problem_manager: this.props.urls.problem_manager
                    }}
                    onChoose={this.chooseProblem}
                />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>
        )
    }
}
