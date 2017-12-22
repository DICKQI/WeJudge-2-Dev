/**
 * Created by lancelrq on 2017/7/26.
 */

var React = require("react");
var core = require("wejudge-core");


module.exports = ClassifyManager;

class ClassifyManager extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            classify_id: 0,
            classify_name: ""
        };
        this.onJsTreeChange = this.onJsTreeChange.bind(this);
        this.newChildNode = this.newChildNode.bind(this);
        this.modifyNode = this.modifyNode.bind(this);
        this.deleteNode = this.deleteNode.bind(this);
    }

    init() {
        this.refs.jstree.load()
    }


    onJsTreeChange(node){
        this.setState({
            classify_id: node.id,
            classify_name: node.text
        })
    }


    newChildNode(){
        var that = this;
        var url = that.props.apis.change_classify.replace('classify/0', 'classify/' + this.state.classify_id);
        var title = that.refs.new_node_name.getValue();
        core.restful({
            url: url + "?action=appendChild",
            data:{
                title: title
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.refs.jstree.refresh()
                });
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }

    modifyNode(){
        var that = this;
        var url = that.props.apis.change_classify.replace('classify/0', 'classify/' + this.state.classify_id);
        var title = that.refs.modify_node_name.getValue();
        core.restful({
            url: url + "?action=modify",
            data:{
                title: title
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.refs.jstree.refresh()
                });
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }

    deleteNode(){
        var that = this;
        var url = that.props.apis.change_classify.replace('classify/0', 'classify/' + this.state.classify_id);
        that.refs.confirm.show(function (rel) {
            if (rel) {
                core.restful({
                    url: url + "?action=delete",
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            that.refs.jstree.refresh();
                            that.refs.jstree.selectNode(rel.data)
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        });
    }


    render() {
        return (
            <div className="ui segment">
                <div className="ui two column very relaxed stackable grid">
                    <div className="column" style={{alignSelf:"top"}}>
                        <core.JSTree
                            ref="jstree"
                            get_data={this.props.apis.jstree.get_data}
                            onchange={this.onJsTreeChange}
                        />
                    </div>
                    <div className="ui vertical divider" style={{left: "50%"}}>
                        管理
                    </div>
                    <div className="column">
                        <div className="ui menu">
                            <div className="item">当前选中节点</div>
                            <div className="item">ID：{this.state.classify_id}</div>
                            <div className="item">名称：{this.state.classify_name}</div>
                        </div>
                        <div className="ui green inverted segment">
                            <h4>新增子节点</h4>
                            <div className="ui inverted form">
                                <core.forms.TextField label="节点名称" ref="new_node_name" />
                                <a className="ui submit button" onClick={this.newChildNode}>新增</a>
                            </div>
                        </div>
                        {this.state.classify_id > 0 ? <div className="ui blue inverted segment">
                            <h4>修改节点</h4>
                            <div className="ui inverted form">
                                <core.forms.TextField label="节点名称" ref="modify_node_name" value={this.state.classify_name} />
                                <a className="ui submit button" onClick={this.modifyNode}>保存</a>
                            </div>
                        </div> : null}
                        {this.state.classify_id > 0 ? <div className="ui red inverted segment">
                            <h4>删除节点</h4>
                            <div className="ui inverted form">
                                <a className="ui submit button" onClick={this.deleteNode}>删除</a>
                            </div>
                        </div> : null}
                    </div>
                </div>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm  ref="confirm"  msg_title="操作确认" msg="你确定要删除该分类吗？该分类以及其子分类将被删除，分类下的题目将被挂载到根节点。" />
            </div>
        );
    }
}