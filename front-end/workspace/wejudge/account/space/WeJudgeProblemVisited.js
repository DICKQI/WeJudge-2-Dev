/*
* Created by lancelrq on 2017/7/28.
*/

var React = require("react");
var core = require("wejudge-core");

module.exports = WeJudgeProblemVisited;


class WeJudgeProblemVisited extends React.Component{

        // 构造
        constructor(props) {
            super(props);
            // 初始状态
            this.state = {};
            this.doFilter = this.doFilter.bind(this);
        }

        load(){
            this.refs.listview.load();
        }

        doFilter(){
            var keyword = this.refs.search_problem.getValue();
            this.refs.listview.setParams({keyword: keyword});
            this.refs.listview.load();
        }

        render(){
            return (
                <div className="ui">
                    <div className="ui menu">
                        <div className="item">
                            <core.forms.TextField
                                ref="search_problem" transparent
                                placeholder="请输入题目ID"
                            />
                        </div>
                        <a className="item" onClick={this.doFilter}>
                            <i className="search icon"></i> 搜索
                        </a>
                    </div>
                    <div style={{marginTop: 20}}>
                        <WeJudgeProblemVisitedList
                            ref="listview"
                            vproblems_list={this.props.apis.vproblems_list}
                            views={this.props.urls}
                        />
                    </div>
                </div>
            )
        }
}

class WeJudgeProblemVisitedList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.vproblems_list
        }
    }

    renderListHeader(){
        return (
            <tr>
                <th>题库</th>
                <th>题目</th>
                <th className="center aligned">通过</th>
                <th className="center aligned">提交</th>
                <th className="center aligned">错误</th>
                <th className="center aligned">最少用时</th>
                <th className="center aligned">最少内存</th>
                <th className="center aligned">最短代码</th>
            </tr>
        );
    }
    renderListItems(){
        var that = this;
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                var url1 = that.props.views.view_problem
                    .replace('problemset/0', 'problemset/' + item.problemset.id)
                    .replace('problem/0', 'problem/' + item.virtual_problem_id);
                var url2 = that.props.views.view_problemset
                    .replace('problemset/0', 'problemset/' + item.problemset.id);
                return <tr key={key} className="center aligned">
                    <td><a href={url2}>{item.problemset.title}</a></td>
                    <td><a href={url1}>{item.problem.id}.{item.problem.title}</a></td>
                    <td className="center aligned">{item.accepted}</td>
                    <td className="center aligned">{item.submission}</td>
                    <td className="center aligned">{item.penalty}</td>
                    <td className="center aligned">{item.best_time} MS</td>
                    <td className="center aligned">{item.best_memory} KB</td>
                    <td className="center aligned">{item.best_code_size} 字节</td>
                </tr>
            });
        else
            return null
    }

}