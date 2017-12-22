/**
 * Created by lancelrq on 2017/7/26.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = JSTree;

class JSTree extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.jstree = null;
        this.get_data = props.get_data;
        this.node_id = 0;
        this.selectNode = this.selectNode.bind(this);
        this.refresh = this.refresh.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        this.get_data = nextProps.get_data;
        //this.__init();
    }

    load(){
        this.__init();
    }

    refresh(){
        $(this.refs.jstree_container).jstree('refresh');
    }

    __changeClassifyId(node){

        if(typeof this.props.onchange === 'function')
            this.props.onchange(node)
        
    }

    selectNode(node_id){
        $(this.refs.jstree_container).jstree('select_node', node_id)
    }


    __init(){
        if(this.jstree) {
            $(this.jstree).jstree().destroy();
            this.jstree = null;
        }
        var that = this;
        this.jstree = $(this.refs.jstree_container).on('changed.jstree', function (e, data) {
            if (data.selected.length > 0){
                var node_id = data.instance.get_node(data.selected[0]).id;
                var node_text = data.instance.get_node(data.selected[0]).text;
                that.node_id = node_id;
                that.__changeClassifyId({
                    id: node_id,
                    text: node_text
                });
            }
        }).jstree({
            'core': {
                "multiple" : false,
                'data': {
                    "url": this.get_data,
                    "data": function (node) {
                        return { "id" : node.id };
                    }
                }
            }
        });
    }

    render(){
        return (
            <div className="ui container" >
                <a href="javascript:void(0)" onClick={this.refresh} className=""><i className="refresh icon" /> 刷新</a>
                <div ref="jstree_container"></div>
            </div>
        )
    }

}