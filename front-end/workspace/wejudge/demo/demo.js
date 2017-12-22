/**
 * Created by lancelrq on 2017/5/10.
 */
var React = require("react");

class AA extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            word:"world"
        };
    }
    a(){
        this.setState({
            word: "123"
        })
    }
    render(){
        return (
            <div className="">
                hello {this.state.word}
            </div>
        )
    }
}