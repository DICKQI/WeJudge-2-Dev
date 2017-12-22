var React = require("react");
var core = require("wejudge-core");

module.exports = AsgnProblemsList;

class AsgnProblemsList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state['is_manager'] = props.is_manager;
        this.apis = {
            data: props.apis.problems_list
        }
    }

    renderListHeader(){
        return (
            <tr>
                <th>题号</th>
                <th>题目</th>
                <th>要求</th>
                <th>分值</th>
                <th>难度</th>
                <th>总体正确率</th>
                {is_manager ? <th>功能</th> : ""}
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return <tr key={key}></tr>
            });
        else
            return null
    }

}