/**
 * Created by lancelrq on 2017/2/15.
 */

module.exports = {
    ProblemsList: ProblemsList,
    ProblemsListFilter: ProblemsListFilter,
    ProblemsListView: ProblemsListView
};

var React = require('react');
var core = require('wejudge-core');

var ProblemsetList = require("./ProblemsetList").ProblemsetList;

class ProblemsList extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            list_problem: props.apis.list_problem,
            view_problem: props.urls.view_problem,
            jstree: props.apis.jstree,
            classify_api: props.apis.classify_api,
            batch_has_selection: false,
            chooing_items: props.chooing_items || {}
        };
        this.onFilter = this.onFilter.bind(this);
        this.removeProblem = this.removeProblem.bind(this);
        this.onBatchSelectChange = this.onBatchSelectChange.bind(this);
        this.moveToClassify = this.moveToClassify.bind(this);
        this.removeFromProblemset = this.removeFromProblemset.bind(this);
        this.psetClick = this.psetClick.bind(this);
        this.moveToProblemset = this.moveToProblemset.bind(this);
        this.onClassifyFilterChange = this.onClassifyFilterChange.bind(this);
        this.load = this.load.bind(this);
    }
    onFilter(formdata){
        this.refs.listView.setParams(formdata);
        this.refs.listView.getListData();
    }

    load(){
        this.refs.listView.getListData();
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            list_problem: nextProps.apis.list_problem,
            view_problem: nextProps.urls.view_problem,
            jstree: nextProps.apis.jstree,
            classify_api: nextProps.apis.classify_api,
            chooing_items: nextProps.chooing_items || {}
        });
    }
    onClassifyFilterChange(node){
        this.refs.listView.setParams({
            classify_id: node.id
        });
        this.refs.listView.getListData();
    }


    removeProblem(pid){
        var that = this;
        return function () {
            that.refs.confirm.setContent("确定要从这个题库中移除这条题目吗？评测信息将不会被删除，再次添加时，将重新关联。", "操作确认");
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.remove_problem.replace('problem/0', 'problem/' + pid),
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.load()
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

    onBatchSelectChange(e){
        var has = e.selectedLength > 0;
        if(this.state.batch_has_selection !== has){
            this.setState({
                batch_has_selection: has
            })
        }
    }

    moveToClassify(){
        if(!this.state.batch_has_selection) return;
        var that = this;
        this.refs.classify_jstree.load();
        this.refs.MoveToDialog.show(function () {
            // OK
            var cid = that.refs.classify_jstree.node_id;
            core.restful({
                url: that.props.apis.problem_moveto_classify.replace('classify/0', 'classify/' + cid),
                method: "POST",
                success: function (rel) {
                    that.refs.alertbox.showSuccess(rel, function () {
                        that.load()
                    });
                },
                error: function (rel, msg) {
                    that.refs.alertbox.showError(rel, msg);
                }
            }).submit_form(that.refs.ProblemListBatchForm);
        });
    }

    removeFromProblemset(){
        if(!this.state.batch_has_selection) return;
        var that = this;
        that.refs.confirm.setContent("确定要从这个题库中移除这些题目吗？评测信息将不会被删除，再次添加时，将重新关联。", "操作确认");
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.problem_removefrom_problemset,
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            that.load()
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).submit_form(that.refs.ProblemListBatchForm);
            }
        });
    }

    psetClick(pset){
        if(!this.state.batch_has_selection) return;
        var that = this;
        that.refs.confirm.setContent("确定将题目推送到这个题库吗？如果存在有题目不是您发布的，它们将无法推送。", "操作确认");
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.problem_moveto_problemset + "?target_pset_id=" + pset.id + "&is_raw_id=false",
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            that.load()
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).submit_form(that.refs.ProblemListBatchForm);
            }
        });
    }

    moveToProblemset(){
        if(!this.state.batch_has_selection) return;
        this.refs.MoveToPsetDialog.show();
        this.refs.ProblemSetView.load();
    }

    render() {
        return (
            <div className="ui">
                {this.props.options.hide_filter ? null :
                <div className="ui top attached menu">
                    <a className="item" onClick={this.load}><i className="refresh icon"></i>刷新</a>
                    <a className="item" onClick={()=>{
                        $(this.refs.filter_panel).slideToggle();
                    }}><i className="filter icon"></i>筛选</a>
                    {this.props.options.show_manage ?
                        <div className="right menu">
                            <a onClick={this.moveToClassify} className={`${!this.state.batch_has_selection ? "disabled" : ""} item`}>
                                <i className="sign in icon"></i> 移入分类
                            </a>
                            <a onClick={this.moveToProblemset} className={`${!this.state.batch_has_selection ? "disabled" : ""} item`}>
                                <i className="random icon"></i> 推送到其他题库
                            </a>
                            <a onClick={this.removeFromProblemset} className={`${!this.state.batch_has_selection ? "disabled" : ""} item`}>
                                <i className="remove icon"></i> 批量移除
                            </a>
                        </div>
                        : null}
                </div>
                }
                <div className="ui bottom attached segment" ref="filter_panel">
                    {this.props.apis.classify && <ProblemsClassifyFilter apis={this.props.apis.classify} onSelect={this.onClassifyFilterChange} />}
                    {this.props.apis.classify && <div className="ui divider"></div>}
                    <ProblemsListFilter onFilter={this.onFilter} ref="filter"/>
                </div>
                <form ref="ProblemListBatchForm" method="post">
                    <ProblemsListView
                        ref="listView" batch={this.props.options.show_manage ? this.onBatchSelectChange : false}
                        list_problem={this.state.list_problem}
                        view_problem={this.state.view_problem}
                        removeProblem={this.removeProblem}
                        hide_ratio={this.props.options.hide_ratio || false}
                        show_manage={this.props.options.show_manage || false}
                        target_blank={this.props.options.target_blank || false}
                        onChoose={this.props.onChoose || false}
                        highLightItems={this.props.highLightItems || []}
                        chooing_items={this.state.chooing_items || {}}
                    />
                </form>
                {this.props.options.show_manage ?
                    <core.dialog.Dialog ref="MoveToDialog" size="small" btnTitle="移动" title="移动到分类">
                        <div style={{height: 360, overflow:"scroll"}}>
                            <core.JSTree
                                ref="classify_jstree"
                                get_data={this.state.jstree.get_data}
                            />
                            <br />
                        </div>
                        <i className="info circle icon" /> 选择“根分类”将移除题目的分类关联
                    </core.dialog.Dialog>
                : null}
                {this.props.options.show_manage ?
                    <core.dialog.Dialog ref="MoveToPsetDialog" size="large" btnShow={false} title="移动到题库">
                        <ProblemsetList
                            ref="ProblemSetView"
                            apis={{
                                list_problemset: this.props.apis.list_problemset
                            }}
                            urls={{}}
                            options={{readonly: true}}
                            psetClick={this.psetClick}
                        />
                    </core.dialog.Dialog>
                : null}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="" msg_title="操作确认" ref="confirm" />
            </div>
        )
    }

}

class ProblemsListView extends core.ListView {

    constructor(props) {
        super(props);
        this.apis = {
            data: props.list_problem
        };
        this.params = {
            page: 1,
            limit: 20,
            display: 11
        };
        this.state['view_problem'] = props.view_problem;
        this.state['chooing_items'] = props.chooing_items || {};
        this.onBatchAll = this.onBatchAll.bind(this);
        this.onBatchChange = this.onBatchChange.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        this.apis['data'] = nextProps.list_problem;
        this.setState({
            view_problem: nextProps.view_problem,
            chooing_items: nextProps.chooing_items
        })
    }

    onBatchAll(e){
        $(this.refs.listview).find('.batch_item').prop("checked", e.target.checked);
        this.onBatchChange();
    }

    onListLoaded(){
        this.clearBatch();
    }

    clearBatch(){
        $(this.refs.listview).find('.batch_item').prop("checked", false);
        this.onBatchChange();
    }
    onBatchChange(e){
        var selectedLength = $(this.refs.listview).find('.batch_item:checked').length;
        if(typeof this.props.batch === 'function')
            typeof this.props.batch({
                selectedLength: selectedLength
            })
    }

    renderListHeader(){
        return (
            <tr>
                {this.props.batch ? <th><input type="checkbox" onChange={this.onBatchAll} /></th> : null}
                <th>ID</th>
                <th>题目名称</th>
                <th>发布者</th>
                <th>难度</th>
                {this.props.hide_ratio ? null : <th>全站正确率</th>}
                {this.props.hide_ratio ? null : <th>我的正确率</th>}
                {this.props.onChoose ? <th>选题操作</th> : null}
                {this.props.show_manage ? <th>管理</th> : null}
            </tr>
        );
    }

    renderListItems(){
        var calcHighLight = (item) => {
            if (!this.props.highLightItems) return "";
            if(this.props.highLightItems.indexOf(item) > -1){
                return "active"
            }else{
                return ""
            }
        };
        if(this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                if(!this.props.hide_ratio) {
                    var all_ratio = ((item.submission > 0) ? 100 * (item.accepted / item.submission) : 0).toFixed(2);
                    var my_counter = (<td>-</td>);
                    if (item.my_submission !== undefined) {
                        var my_ratio = ((item.my_submission !== undefined && item.my_submission > 0) ? 100 * (item.my_accepted / item.my_submission) : 0).toFixed(2);
                        my_counter = (
                            <td>{my_ratio}% ({item.my_accepted} / {item.my_submission})</td>
                        )
                    }
                }
                return (
                    <tr key={key} className={calcHighLight(item.entity ? item.entity.id : item.id)}>
                        {this.props.batch ? <td><input type="checkbox" className="batch_item" name="batch_id" value={item.id} onChange={this.onBatchChange}/></td> : null}
                        <td>{item.entity ? item.entity.id : item.id}</td>
                        <td><a href={this.state.view_problem.replace("/problem/0", "/problem/" + item.id)} target={this.props.target_blank ? "_blank" : "_self"}>{item.title}</a></td>
                        <td><a href="javascript:void(0)" onClick={core.show_account('master', item.author.id)}>{item.author.nickname}</a></td>
                        <td><core.forms.RatingField disabled rating={item.diff}/></td>
                        {this.props.hide_ratio ? null : <td>{all_ratio}% ({item.accepted} / {item.submission})</td> }
                        {this.props.hide_ratio ? null : my_counter}
                        {this.props.onChoose ? <td >
                            {!this.state.chooing_items[item.entity.id] ? <a className="ui green compact button" onClick={function(val, that){return function(){that.props.onChoose(val)}}(item, this)}>
                                <i className="add icon"></i> 选择
                            </a> : <a className="ui red compact button"  onClick={function(val, that){return function(){that.props.onChoose(val)}}(item, this)}>
                                    <i className="remove icon"></i> 取消
                            </a>}
                        </td> : null}
                        {this.props.show_manage ? <td >
                            <a className="ui compact button" onClick={this.props.removeProblem(item.id)}>
                                <i className="remove icon"></i> 移除
                            </a>
                        </td> : null}
                    </tr>
                )
            });
        else
            return null;
    }
}

class ProblemsClassifyFilter extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            classify_id: 0,
            classify_list: [],
            classify_stack: [
                {id: 0, text: "根分类", children: true}
            ]
        };
        this.doSelect = this.doSelect.bind(this);
        this.doBack = this.doBack.bind(this);
        this.working = false;
    }

    getTags(){
        if(this.working) return;
        this.working = true;
        var that = this;
        core.restful({
            url: that.props.apis.get_data + "?id=" + that.state.classify_id,
            method: "POST",
            success: function (rel) {
                that.working = false;
                if(that.state.classify_id === 0) {
                    that.setState({
                        classify_list: rel.data[0].children
                    })
                }else{
                    that.setState({
                        classify_list: rel.data
                    })
                }
            },
            error: function (rel, msg) {
                that.working = false;
                alert('加载失败：' + msg);
            }
        }).call()
    }

    doSelect(item){
        var that = this;
        return function () {
            typeof that.props.onSelect === "function" && that.props.onSelect(item);
            if(item.children) {
                var classify_stack = that.state.classify_stack;
                classify_stack.push(item);
                that.setState({
                    classify_id: item.id,
                    classify_stack: classify_stack
                }, function () {
                    that.getTags();
                });
            }else{
                that.setState({
                    classify_id: item.id
                });
            }
        }
    }

    doBack(item){
        var that = this;
        return function () {
            var classify_stack = that.state.classify_stack;
            var cls = classify_stack[0];
            while(classify_stack.length > 0){
                // 退栈操作
                cls = classify_stack.pop();
                if(cls === item){
                    // 退到目标栈
                    classify_stack.push(cls);
                    break;
                }
            }
            typeof that.props.onSelect === "function" && that.props.onSelect(cls);
            that.setState({
                classify_id: cls.id,
                classify_stack: classify_stack
            }, function () {
                that.getTags();
            });
        }
    }

    componentDidMount() {
        this.getTags();
    }

    render(){
        return <div className="ui basic segment">
            <strong>分类导航：</strong>
            <div className="ui breadcrumb">
                {this.state.classify_stack && this.state.classify_stack.map((item, key)=>{
                    var is_active = key === (this.state.classify_stack.length - 1);

                    return is_active ?
                        <spa  className="active section" key={key}>{item.text}</spa>
                        : [
                            <a className="section" onClick={this.doBack(item)} key={key}>{item.text}</a>,
                            <i className="right angle icon divider" key={"div_" + key}></i>
                        ]
                })}
            </div>
            <div className="ui hidden divider"></div>
            <div style={{lineHeight: "2em"}}>
                {this.state.classify_list && this.state.classify_list.length > 0 ? this.state.classify_list.map((item, key) => {
                    return <a className={`ui ${this.state.classify_id === item.id && "blue"} label`} key={key} onClick={this.doSelect(item)}>
                        <i className="tag icon"></i>{item.text}
                    </a>
                }) : <span>当前题目集还没有创建分类信息</span> }
            </div>
        </div>
    }
}

class ProblemsListFilter extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.doSubmit = this.doSubmit.bind(this);
    }

    doSubmit(e){
        e.preventDefault();
        if(typeof this.props.onFilter === "function")
            var arraydata = $(this.refs.FilterFormPanel).serializeArray();
        var formdata = {};
        arraydata.map((val, key) => {
            formdata[val.name] = val.value;
        });
        this.props.onFilter(formdata);
        return false;
    }

    render(){
        return (
                <form className="ui form" ref="FilterFormPanel" onSubmit={this.doSubmit}>
                    <div className="five stackable fields">
                        <core.forms.TextField name="keyword" label="题目编号或名称" placeholder="题目名称支持模糊查找" />
                        <core.forms.TextField name="author" label="出题者" placeholder="支持模糊查找" />
                        <core.forms.SelectField name="diff" label="题目难度" forceDefault >
                            <option value="-1">全部</option>
                            <option value="0">未分类</option>
                            <option value="1">入门</option>
                            <option value="2">简单</option>
                            <option value="3">一般</option>
                            <option value="4">较难</option>
                            <option value="5">困难</option>
                        </core.forms.SelectField>
                        <core.forms.SelectField name="limit" label="每页数量" forceDefault value="20">
                            <option value="5">5条</option>
                            <option value="10">10条</option>
                            <option value="15">15条</option>
                            <option value="20">20条</option>
                            <option value="25">25条</option>
                            <option value="30">30条</option>
                            <option value="35">35条</option>
                            <option value="40">40条</option>
                            <option value="45">45条</option>
                            <option value="50">50条</option>
                        </core.forms.SelectField>
                        <core.forms.SelectField name="desc" label="排列方式" forceDefault >
                            <option value="false">正序排列</option>
                            <option value="true">倒序排列</option>
                        </core.forms.SelectField>
                    </div>
                    <div className="ui divider"></div>
                    <button className="ui primary button"><i className="icon filter"></i>筛选</button>
                </form>
        )
    }
}