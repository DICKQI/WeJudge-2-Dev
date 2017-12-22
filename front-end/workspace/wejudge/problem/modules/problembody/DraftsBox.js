/**
 * Created by lancelrq on 2017/9/6.
 */

var React = require('react');
var core = require('wejudge-core');

module.exports = DraftsBox;

class DraftsBox extends core.PageView {
    // 构造
    constructor(props){
        super(props);
        // 初始状态
        this.apis = {
            data: props.get_darfts
        };
        this.LangList = {};
        for (var i = 0 ; i < core.LangList.length; i++){
            this.LangList[core.LangList[i][0]] = core.LangList[i][1];
        }
    }

    renderBody() {
        var data = this.state.data;
        var that = this;
        return (<div className="ui segment">
            {data && data.length > 0 ? <div className="ui relaxed divided list">
                {data.map(function (item, key) {
                    return <div className="item" key={key}>
                        <i className="file middle aligned icon"></i>
                        <div className="content">
                            <a onClick={that.props.restore(item)} className="header">创建于{core.tools.format_datetime(item.create_time)} </a>
                            <div className="description">编程语言：{that.LangList[item.lang] || "未知" }</div>
                        </div>
                    </div>
                })}
            </div> : <div>
                你还没有保存草稿哦！
            </div>}
        </div>);
    }
}
