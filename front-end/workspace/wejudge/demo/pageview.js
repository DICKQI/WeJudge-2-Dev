
var React = require("react");
var core = require("wejudge-core");


module.exports = EduProblemSet;

class EduProblemSet extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.xxx
        };

    }

    componentDidMount() {
        this.getData();
    }


    renderBody() {
        var xx = this.state.data;
        return (<div></div>);
    }
}
