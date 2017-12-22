/**
 * Created by lancelrq on 2017/2/15.
 */
module.exports = {
    JudgeStatusList: JudgeStatusList,
    JudgeStatusFilter: JudgeStatusFilter,
    JudgeStatusListView: JudgeStatusListView
};

var React = require('react');
var core = require('wejudge-core');


class JudgeStatusList extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.onFilter = this.onFilter.bind(this);
        this.load = this.load.bind(this);
    }

    onFilter(formdata){
        this.refs.listView.setParams(formdata);
        this.refs.listView.getListData();
    }

    load(){
        this.refs.listView.getListData();
    }

    render() {
        var that = this;
        var showFilter = function () {
            that.refs.filter.show();
        };
        return (
            <div className="ui">
                {this.props.options.full ?
                    <div className="ui menu">
                        <a className="item" onClick={this.load}><i className="refresh icon"></i> 刷新</a>
                        <a className="item" onClick={showFilter}><i className="filter icon"></i> 筛选</a>
                    </div>
                : null }
                <JudgeStatusListView
                    ref="listView"
                    realname={this.props.options.realname}          // 是否显示真实姓名
                    nickname={this.props.options.nickname}          // 是否显示昵称
                    userid={this.props.options.userid}              // 是否显示用户名
                    list_status={this.props.apis.list_status}
                    view_problem={this.props.urls.view_problem}
                    view_detail={this.props.urls.view_detail}
                    app_name={this.props.options.app_name || "master"}
                />
                <JudgeStatusFilter onFilter={this.onFilter} ref="filter" />
            </div>
        )
    }
}

class JudgeStatusListView extends core.ListView {
    constructor(props) {
        super(props);
        this.apis = {
            data: props.list_status
        };
    }
    renderListHeader(){
        return (
            <tr>
                <th>ID</th>
                <th>题目ID</th>
                <th>提交者</th>
                <th>评测结果</th>
                <th>最大运行时长</th>
                <th>最大内存用量</th>
                <th>代码长度</th>
                <th>代码语言</th>
                <th>提交时间</th>
            </tr>
        );
    }
    renderListItems(){
        var flag_desc;
        if(this.state.rawdata)
            flag_desc = this.state.rawdata.flag_desc || {};
        else
            flag_desc = {};

        var that = this;

        if (this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                var view_flag_btn = function (flag) {
                    return (
                        <a className={"ui mini compact " + flag_desc[flag].color +" button"} title={flag_desc[flag].en}
                           href={that.props.view_detail.replace("status/0", "status/" + item.id)}
                           target="_blank"
                        >{(flag === 1 && !item.strict_mode) ? "数据通过(DA)" : flag_desc[flag].title}</a>
                    )
                };
                return (
                    <tr key={key}>
                        <td>{item.id}</td>
                        <td>
                            {
                                item.virtual_problem ?
                                    <a target="_blank"
                                       href={this.props.view_problem.replace("/problem/0", "/problem/" + item.virtual_problem.id)}>
                                        {
                                            item.virtual_problem.index ?
                                                `题目${core.tools.gen_problem_index(item.virtual_problem.index)}` :
                                                item.problem_id
                                        }
                                    </a>
                                    : item.problem_id
                            }
                        </td>
                        <td>
                            <a href="javascript:void(0)" onClick={core.show_account(that.props.app_name, item.author.id)} style={{color: (item.author.sex === 0) ? "red" : ""}}>
                            {this.props.realname && this.props.nickname ?
                                <span>
                                    {item.author.nickname}{this.props.userid ? `(${item.author.username})` : null}<br />
                                    <span style={{color: "gray", fontSize:"0.8em"}}>{item.author.realname}</span>
                                </span> :
                                (this.props.realname ? item.author.realname : item.author.nickname)
                            }
                            </a>
                        </td>
                        <td>{view_flag_btn(item.flag)}</td>
                        <td>{(item.flag === 2) ? "---" : item.exe_time + " MS"}</td>
                        <td>{(item.flag === 3) ? "---" : item.exe_mem + " KB"}</td>
                        <td>{item.code_len} 字节</td>
                        <td>{item.lang}</td>
                        <td>{item.create_time}</td>
                    </tr>
                )
            });
        else
            return null
    }
}

class JudgeStatusFilter extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
    }

    show(){
        var that = this;
        this.refs.FilterDialog.show(function () {
            // OK
            if(typeof that.props.onFilter === "function")
                var arraydata = $(that.refs.FilterFormPanel).serializeArray();
            var formdata = {};
            arraydata.map((val, key) => {
                formdata[val.name] = val.value;
            });
            that.props.onFilter(formdata);
        }, function () {
            // Close
        })
    }

    render(){
        return (
            <core.dialog.Dialog ref="FilterDialog" size="small" btnTitle="筛选" title="筛选评测结果">
                <form className="ui form" ref="FilterFormPanel">
                    <core.forms.TextField name="problem_id" label="题目ID" />
                    <core.forms.TextField name="author_id" label="提交者" />
                    <core.forms.SelectField name="flag" label="评测状态" forceDefault >
                        <option value="-3">全部(All)</option>
                        <option value="0">评测通过(Accepted)</option>
                        <option value="1">格式错误(Presentation Error)</option>
                        <option value="2">超过时间限制(Time Limit Exceeded)</option>
                        <option value="3">超过内存限制(Memory Limit Exceeded)</option>
                        <option value="4">答案错误(Wrong Answer)</option>
                        <option value="5">运行时错误(Runtime Error)</option>
                        <option value="6">输出内容超限(Output Limit Exceeded)</option>
                        <option value="7">编译失败(Compile Error)</option>
                        <option value="8">系统错误(System Error)</option>
                        <option value="9">等待重判(Pending Rejudge)</option>
                        <option value="10">特殊评测超时(Special Judger Time OUT)</option>
                        <option value="11">特殊评测程序错误(Special Judger ERROR)</option>
                        <option value="12">特殊评测完成(Special Judger Finish)</option>
                        <option value="20">等待人工评判(Pending Manual Judge)</option>
                        <option value="-1">评测中(Judging)</option>
                        <option value="-2">队列中(Pending)</option>
                    </core.forms.SelectField>
                    <div className="ui segment">
                        <core.forms.CheckBoxField name="asc" type="toggle" label="按ID正序排列" value="true"/>
                    </div>
                </form>
            </core.dialog.Dialog>
        )
    }
}