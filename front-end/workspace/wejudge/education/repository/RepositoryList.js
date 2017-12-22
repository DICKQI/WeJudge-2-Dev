/**
 * Created by lancelrq on 2017/8/12.
 */

var React = require("react");
var core = require("wejudge-core");
var RepositoryEditor = require('./RepositoryEditor');

module.exports = RepositoryList;


class RepositoryList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.repotories_list
        };
        this.onlyMe = this.onlyMe.bind(this);
        this.viewAll = this.viewAll.bind(this);
        this.toggleToCourse = this.toggleToCourse.bind(this);
    }

    onlyMe(){
        this.setParams({
            only_me: true,
        });
        this.getListData();
    }

    viewAll(){
        this.setParams({
            only_me: false,
        });
        this.getListData();
    }

    toggleToCourse(entity){
        var that = this;
        return function () {
            core.restful({
                url: that.props.apis.toggle_in_course,
                data:{
                    repo_id: entity.id,
                },
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
    }


    renderHeaderBody(){
        return this.props.options.is_teacher ? <div>
            <div className="ui compact menu">
                {!this.props.options.toggle_in_course ? <a className="item" onClick={
                    function (that) {
                        return function () {
                            that.refs.editor.create();
                        }
                    }(this)
                }><i className="add icon"></i> 增加</a> : null}
                <a className="item" onClick={this.onlyMe}><i className="user icon"></i> 只看我的</a>
                <a className="item" onClick={this.viewAll}><i className="users icon"></i> 查看全部</a>
            </div>
        </div> : null
    }

    renderListHeader(){
        return (
            <tr>
                <th>#ID</th>
                <th>名称</th>
                <th>创建者</th>
                <th>当前容量</th>
                <th>公开等级</th>
                {this.props.options.is_teacher && this.props.options.toggle_in_course ? <th>关联</th> : null}
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return <tr key={key}>
                    <td>{item.id}</td>
                    <td><a target="_blank" href={this.props.urls.repotory_view.replace("repository/0", "repository/" + item.id)}>{item.title}</a></td>
                    <td>{item.author.realname}</td>
                    <td>{core.tools.bytesToSize(item.cur_size)}</td>
                    <td>{["私有", "校内公开", "完全公开"][item.public_level]}</td>
                    {this.props.options.is_teacher && this.props.options.toggle_in_course ? <td>
                        <a onClick={this.toggleToCourse(item)} className={`ui compact ${item.enabled ? "red" : "green"} button`}>{item.enabled ? "解除关联" : "关联"}</a>
                    </td> : null}
                </tr>
            });
        else
            return null
    }

    renderFooterBody(){
        return <div>
            <RepositoryEditor
                manager={this}
                ref="editor"
                apis={this.props.apis}
            />
            <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
        </div>
    }
}