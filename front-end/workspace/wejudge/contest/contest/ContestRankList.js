/**
 * Created by lancelrq on 2017/4/9.
 */

var React = require("react");
var core = require("wejudge-core");
var moment = require('moment');

module.exports = RankList;

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
        if(this.props.is_referee && !this.refresh_timer){
            console.log("RankList Watcher: Start");
            this.refresh_timer = setInterval(function () {
                console.log("RankList Watcher: Tick");
                that.getListData();
            }, 60 * 1000);   // refresh after 60 s
        }
    }

    componentWillUnmount() {
        if(this.refresh_timer){ clearInterval(this.refresh_timer); }
    }

    renderListHeader(){
        return (
            <tr>
                <th className="center aligned" width="80">最终排行</th>
                <th className="center aligned" width="80">实时排行</th>
                <th width="200">参赛者</th>
                <th className="center aligned" width="80">通过题数</th>
                <th className="center aligned" width="100">总计时间</th>
                {this.state.rawdata ? this.state.rawdata.problems.map((val, key)=>{
                    return (
                        <th key={`th_${key}`}  className="center aligned">
                            <a target="_blank" href={this.props.urls.view_problem.replace("problem/0", "problem/"+val.id)}>
                                题{core.tools.gen_problem_index(val.index)}
                            </a>
                        </th>
                    )
                }) : null}
            </tr>
        );
    }
    renderListItems(){
        if(!this.state.rawdata) return null;
        var problems = this.state.rawdata.problems;
        var contest = this.state.rawdata.contest;
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                // if (item.rank_solved == 0 && (Object.keys(item.solutions)).length == 0) return null;
                return (
                    <tr key={key}>
                        <td className="center aligned">{item.finally_rank == 0 ? '---' : item.finally_rank}</td>
                        <td className="center aligned">{item.rank_solved > 0 ? item.rank : "---"}</td>
                        <td style={{color: (item.sex == 0) ? "red" : ""}}>
                            {item.ignore_rank ? "*" : null}{item.nickname}({item.username})<br />
                            <span style={{color: "gray", fontSize:"0.8em"}}>{item.realname}</span>
                        </td>
                        <td className="center aligned">{item.rank_solved}</td>
                        <td className="center aligned">{core.tools.rank_list_time(item.rank_timeused)}</td>
                        {problems.map((val, key)=>{
                            var sol = item.solutions[val.id];
                            if(!sol) return <td className="center aligned" key={`sol_${key}`}>&nbsp;</td>;
                            var stat_color = (sol.accepted > 0) ? (sol.is_first_blood ? "blue" : "green") : "red";
                            return (
                                <td className={`${stat_color} center aligned`} key={`sol_${key}`}>
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
                            )
                        })}
                    </tr>
                );
            });
        else
            return null;
    }

}