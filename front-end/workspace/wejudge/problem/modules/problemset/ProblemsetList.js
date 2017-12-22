/**
 * Created by lancelrq on 2017/7/13.
 */

module.exports = {
    ProblemsetList: ProblemsetList,
    ProblemsetListFilter: ProblemsetListFilter,
    ProblemsetListView: ProblemsetListView
};

var React = require('react');
var core = require('wejudge-core');
var ProblemSetEditor = require('./ProblemsetEditor');


class ProblemsetList extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.onFilter = this.onFilter.bind(this);
        this.createProblemSet = this.createProblemSet.bind(this);
        this.load = this.load.bind(this);
    }

    onFilter(formdata){
        this.refs.listView.setParams(formdata);
        this.refs.listView.getData();
    }

    load(){
        this.refs.listView.getData();
    }

    createProblemSet(){
        this.refs.editor.createProblemSet();
    }
    render() {
        var that = this;
        return (
            <div className="ui">
                <div className="ui top attached menu">
                    <a className="item" onClick={this.load}><i className="refresh icon"></i> 刷新列表</a>
                    <a className="item" onClick={()=>{
                        $(this.refs.filter_panel).slideToggle();
                    }}><i className="filter icon"></i> 筛选</a>
                </div>
                <div className="ui bottom attached segment" ref="filter_panel" style={{display:"none"}}>
                    <ProblemsetListFilter onFilter={this.onFilter} ref="filter" />
                </div>
                <br />
                <ProblemsetListView
                    ref="listView"
                    manage={this}
                    list_problemset={this.props.apis.list_problemset}
                    view_problemset={this.props.urls.view_problemset}
                    onProblemsetClick={this.props.psetClick || false}
                />
                <ProblemSetEditor ref="editor" apis={this.props.apis.editor} manager={this} />
            </div>
        )
    }
}


class ProblemsetListView extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.manager = props.manage;
        this.apis = {
            data: props.list_problemset
        };
        this.state = {
            data: [],
            pagination: {},
            inited: false
        };
        this.params = {
            page: 1,
            limit: 20,
            display: 11
        };
        this.modifyProblemSet = this.modifyProblemSet.bind(this);
        this.onPageBtnClick = this.onPageBtnClick.bind(this);
    }

    setParams(nextParams){
        this.params = $.extend(this.params, nextParams);
    }

    onPageBtnClick(page) {
        this.params.page = page;
        this.getData();
    }

    getData(){
        var that = this;
        super.getData(this.params, function (rel) {
            var data = rel.data;
            that.setState({
                inited: true,
                pagination: data.pagination
            });
        })
    }


    modifyProblemSet(psid){
        var that = this;
        return function () {
            that.manager.refs.editor.modifyProblemSet(psid);
        };
    }

    renderBody() {
        var problemset = this.state.data.data;
        var on_click = (problem) => {
            return ()=> {
                if(this.props.onProblemsetClick){
                    this.props.onProblemsetClick(problem);
                }else{
                    window.location.href=this.props.view_problemset.replace('problemset/0', 'problemset/'+problem.id)
                }
            }
        };
        return (
            <section>
                {problemset && problemset.length > 0 ?
                    <div className="ui four column stackable grid">
                        {problemset.map((val, key) => {
                            return (
                                <div key={key} className="column">
                                <div className="ui fluid card">
                                    <a href="javascript:void(0)" onClick={on_click(val)} className="image">
                                        <img src={ val.image } style={{maxHeight:"240px"}}/>
                                    </a>
                                    <div className="content">
                                        <div className="header">
                                            <a href="javascript:void(0)" onClick={on_click(val)}>{val.title}</a>
                                        </div>
                                        <p className="meta">
                                            <i className="user icon"></i><a href="javascript:void(0)" onClick={core.show_account('master', val.manager.id)}>{ val.manager.nickname }</a>
                                        </p>
                                        <p className="description">
                                            {val.description}
                                        </p>
                                    </div>
                                    <div className="extra content">
                                        <span className="right floated">

                                        {
                                            val.private === 2 ? <span><i className="lock icon"></i> 私有题库</span> :
                                                val.private === 1 ? <span><i className="share alternate icon"></i> 共享题库</span> :
                                                    <span><i className="globe icon"></i> 公开题库</span>
                                        }
                                        </span>
                                        <i className="file text outline icon"></i> { val.items_count } 题
                                    </div>
                                    {!this.manager.props.options.readonly && val.editable ? (
                                        <a className="ui bottom attached blue button" href="javascript:void(0)" onClick={this.modifyProblemSet(val.id)}><i className="edit icon"></i>编辑题库</a>
                                    ) : null}
                                </div>
                            </div>);
                        })}
                        </div>: <div className="ui icon message">
                        <i className="info circle icon"></i>
                        <div className="content">
                            <p>还没有人创建题目集哦！</p>
                        </div>
                    </div>}
            </section>
        )
    }
}


class ProblemsetListFilter extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
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
                <div className="three fields">
                <core.forms.TextField name="keyword" label="题目集名称" placeholder="支持模糊查找" />
                <core.forms.TextField name="author_id" label="创建者"  placeholder="支持模糊查找" />
                    <core.forms.SelectField name="desc" label="排列方式" forceDefault>
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