/**
 * Created by lancelrq on 2017/3/10.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = PageView;

class PageView extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            data: null
        };
        this.onErrorReLoad = this.onErrorReLoad.bind(this);
    }

    getData(params, success, failed){
        var that = this;
        this.refs.loader.show();
        var core = require('wejudge-core');
        this.setState({
            data: null
        }, function () {
            core.restful({
                method: 'GET',
                data: params || null,
                responseType: "json",
                url: that.apis.data,
                success: function (rel) {
                    that.setState({
                        data: rel.data
                    }, function () {
                        that.refs.loader.hide();
                        that.refs.messager.hide();
                        if(typeof success === 'function')
                            success(rel);
                    });

                },
                error: function (rel, msg) {
                    that.refs.loader.hide();
                    that.refs.messager.show("数据加载失败", msg, 'error');
                    if(typeof failed === 'function')
                        failed(rel, msg);
                }
            }).call();
        });
    }

    load(success){
        this.getData(null, function () {
            if(typeof success === "function"){
                success()
            }
        });
    }

    onErrorReLoad(){
        this.getData();
    }

    render(){
        var core = require("wejudge-core");
        return (
            <div className="ui" style={{minHeight: 200}}>
                <core.dimmer.Loader inverted ref="loader"/>
                <core.dimmer.Messager inverted title="数据加载失败" ref="messager" retry={this.onErrorReLoad}/>
                {this.state.data ? this.renderBody() : null}
            </div>
        )
    }

}