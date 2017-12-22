/**
 * Created by lancelrq on 2017/5/2.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = ProblemJudgeDesc;


class ProblemJudgeDesc extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        this.state = {
            problem: props.problem,
            judge_config: props.judge_config
        }
    }

    render(){
        var problem_entity = this.state.problem;
        var judge_config = this.state.judge_config;
        return (
            <div className="ui">
                
            </div>
        )
    }
}