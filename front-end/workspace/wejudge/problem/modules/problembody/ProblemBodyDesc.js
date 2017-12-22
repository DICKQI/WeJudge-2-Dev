/**
 * Created by lancelrq on 2017/5/2.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = ProblemBodyDesc;


class ProblemBodyDesc extends React.Component {
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
                <div className="ui stackable celled grid">
                    <div className="twelve wide column">
                        <div className="problem_content" dangerouslySetInnerHTML={{__html: problem_entity.description }} style={{minHeight: 120}}></div>
                        <div className="problem_content">
                            <div className="ui horizontal divider">
                                <h3><i className="bookmark icon"/>输入要求</h3>
                            </div>
                            <div className="ui secondary segment">
                                {problem_entity.input ?  <p dangerouslySetInnerHTML={{__html: problem_entity.input }} /> :  <p>(无)</p>}
                            </div>
                        </div>

                        <div className="problem_content">
                            <div className="ui horizontal divider">
                                <h3><i className="remove bookmark icon"/>输出要求</h3>
                            </div>
                            <div className="ui secondary segment">
                                {problem_entity.output ? <p dangerouslySetInnerHTML={{__html: problem_entity.output }} /> :  <p>(无)</p>}
                            </div>
                        </div>

                        <div className="problem_content">
                            <div className="ui horizontal divider">
                                <h3><i className="hashtag icon"/>测试数据</h3>
                            </div>
                            <div className="ui two column stackable grid">
                                <div className="column">
                                    <h4>输入示例</h4>
                                    <div className="ui secondary segment">
                                        {problem_entity.sample_input ? <code dangerouslySetInnerHTML={{__html: problem_entity.sample_input }}></code> :  <p>(无)</p>}
                                    </div>
                                </div>
                                <div className="column">
                                    <h4>输出示例</h4>
                                    <div className="ui secondary segment">
                                        {problem_entity.sample_output ? <code dangerouslySetInnerHTML={{__html: problem_entity.sample_output }}></code> : <p>(无)</p>}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="problem_content">
                            <div className="ui horizontal divider">
                                <h3><i className="pin icon"/>小贴士</h3>
                            </div>
                            <div className="ui secondary segment">
                                {problem_entity.hint ? <p dangerouslySetInnerHTML={{__html: problem_entity.hint }} /> : <p>(无)</p>}
                            </div>
                        </div>

                        <div className="problem_content">
                            <div className="ui horizontal divider">
                                <h3><i className="anchor icon" />题目来源</h3>
                            </div>
                            <div className="ui secondary segment">
                                {problem_entity.source ? <p dangerouslySetInnerHTML={{__html: problem_entity.source }} /> : <p>WeJudge原创</p>}
                            </div>
                        </div>
                    </div>
                    <div className="four wide column">
                        <table className="ui very basic striped table">
                            <tbody>
                            <tr>
                                <td><strong>题目类型</strong></td>
                                <td className="right aligned">{problem_entity.problem_type === 0 ? "标准题目" : "代码填空"}</td>
                            </tr>
                            <tr>
                                <td><strong>判题模式</strong></td>
                                <td className="right aligned">{judge_config.special_judge === 2 ? "特殊评测（交互判题）" : judge_config.special_judge === 1 ? "特殊评测（结果检查）" : "正常评测"}</td>
                            </tr>
                            <tr>
                                <td><strong>题目难度</strong></td>
                                <td className="right aligned"><core.forms.RatingField disabled rating={problem_entity.difficulty} /></td>
                            </tr>
                            <tr>
                                <td><strong>题目发布</strong></td>
                                <td className="right aligned">{problem_entity.author.nickname}</td>
                            </tr>
                            <tr>
                                <td><strong>发布时间</strong></td>
                                <td className="right aligned">{core.tools.format_datetime(problem_entity.create_time)}</td>
                            </tr>
                            <tr>
                                <td><strong>更新时间</strong></td>
                                <td className="right aligned">{core.tools.format_datetime(problem_entity.update_time)}</td>
                            </tr>
                            <tr>
                                <td colSpan={2}><strong>可用评测语言及资源限制</strong></td>
                            </tr>
                            {problem_entity.rules && problem_entity.rules.length > 0 && problem_entity.rules.map((val, key) => {
                                return [<tr key={key}>
                                    <td><img className="ui avatar circular image" src={"/static/images/language/" + val.lang+ ".jpg"} />&nbsp;{val.name}</td>
                                    <td className="right aligned">
                                        {val.time_limit} MS，{val.mem_limit} KB
                                    </td>
                                </tr>]
                            })}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        )
    }
}
