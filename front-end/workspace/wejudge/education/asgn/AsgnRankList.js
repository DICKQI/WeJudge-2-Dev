/**
 * Created by lancelrq on 2017/4/9.
 */

var React = require("react");
var core = require("wejudge-core");
var moment = require('moment');

module.exports = RankListView;


class RankListView extends  React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            arrangement_id: 0
        };
        this.load = this.load.bind(this);
        this.changeArrangement = this.changeArrangement.bind(this);
    }

    onFilter(formdata){
        this.refs.listView.setParams(formdata);
        this.refs.listView.getListData();
    }

    load(){
        this.refs.listView.getListData();
    }

    changeArrangement(e){
        this.refs.listView.setParams({
            arrangement_id: e.target.value
        });
        this.refs.listView.getListData();
    }

    render() {
        var that = this;
        return (
            <div className="ui">
                <div className="ui stackable grid">
                    <div className="twelve wide column">
                        <div className="ui compact menu">
                            <a className="item" onClick={this.load}><i className="refresh icon"></i> 刷新</a>
                            <a className="item" href={this.props.urls.view_rank_board} target="_blank">
                                <i className="external icon"></i> 滚动大屏幕
                            </a>

                        </div>
                    </div>
                    <div className="four wide column">
                        <core.forms.SelectField forceDefault fluid onchange={this.changeArrangement} value={this.state.arrangement_id}>
                            <option value="0">所有</option>
                            {this.props.options.arrangements.map((val, key) => {
                                return (
                                    <option key={key} value={val.id}>{val.name ? val.name : core.tools.get_arrangement_desc(val)}</option>
                                );
                            })}
                        </core.forms.SelectField>
                    </div>
                </div>

                <RankList
                    ref="listView"
                    apis={this.props.apis}
                    urls={this.props.urls}
                />
            </div>
        )
    }
}

class RankList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.ranklist
        };
        this.table_style = "celled striped";
    }

    componentDidMount() {
        var that = this;
        super.componentDidMount();
        // if(!this.refresh_timer){
        //     console.log("Asgn RankList Watcher: Start");
        //     this.refresh_timer = setInterval(function () {
        //         console.log("Asgn RankList Watcher: Tick");
        //         that.getListData();
        //     }, 60 * 1000);   // refresh after 60 s
        // }
    }

    componentDidUpdate() {
        $(".solution_items").popup()
    }

    componentWillUnmount() {
        // if(this.refresh_timer){ clearInterval(this.refresh_timer); }
    }

    renderListHeader(){
        if(!this.state.rawdata) return <tr></tr>;
        var problems = this.state.rawdata.problems;
        return (
            <tr>
                <th className="center aligned" width="80">排行</th>
                <th width="200">学生</th>
                <th className="center aligned" width="80">通过题数</th>
                <th className="center aligned" width="100">总计时间</th>
                {problems.map((val, key)=>{
                    return (
                        <th key={`th_${key}`}  className="center aligned">
                            <a target="_blank" href={this.props.urls.view_problem.replace("problem/0", "problem/"+val.id)}>
                                题{core.tools.gen_problem_index(val.index)}
                            </a>
                        </th>
                    )
                })}
            </tr>
        );
    }
    renderListItems(){
        if(!this.state.rawdata) return null;
        var problems = this.state.rawdata.problems;
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                // if (item.rank_solved == 0 && (Object.keys(item.solutions)).length == 0) return null;
                return (
                    <tr key={key}>
                        <td className="center aligned">{item.rank_solved > 0 ? item.rank : "---"}</td>
                        <td>
                            <a href="javascript:void(0)" onClick={core.show_account('education', item.author.id)} style={{color: (item.author.sex === 0) ? "red" : ""}}>
                            {item.author.realname}({item.author.username})<br />
                            <span style={{color: "gray", fontSize:"0.8em"}}>{item.realname}</span>
                            </a>
                        </td>
                        <td className="center aligned">{item.rank_solved}</td>
                        <td className="center aligned">{core.tools.rank_list_time(item.rank_timeused)}</td>
                        {problems.map((val, key)=>{
                            var sol = item.solutions[val.id];
                            if(!sol) return <td className="center aligned" key={`sol_${key}`}>&nbsp;</td>;
                            var stat_color = (sol.accepted > 0) ? "green" : "red";
                            var pop_content = `
                                提交：${sol.submission}<br />
                                通过：${sol.accepted}<br />
                                错误：${sol.penalty}<br />
                                解题用时：${core.tools.rank_list_time(sol.used_time)}<br />
                                真实用时：${core.tools.rank_list_time(sol.used_time_real)}
                            `;
                            return sol.submission > 0 ?
                                <td className={`${stat_color} center aligned solution_items`}
                                    key={`sol_${key}`}
                                    data-html={pop_content}>
                                    { sol.accepted > 0 ?
                                        <span>
                                        {core.tools.rank_list_time(sol.used_time_real)}<br />
                                        ({sol.penalty > 0 ? `-${sol.penalty}` : 0 })
                                    </span> :
                                        <span>
                                        ({sol.submission > 0 ? `${sol.submission}` : 0 })
                                    </span>
                                    }
                                </td>
                                :
                                <td key={`sol_${key}`}>&nbsp;</td>
                        })}
                    </tr>
                );
            });
        else
            return null
    }

}