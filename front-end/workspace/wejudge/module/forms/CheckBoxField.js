/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = CheckBoxField;

var React = require('react');
var Field = require('./Field');

class CheckBoxField extends Field{

    constructor(props){
        super(props);
        this.state['checked'] = props.checked;
        if(props.defaultChecked) this.state['checked'] = true;
        this.handlerChange = this.handlerChange.bind(this);
    }

    componentDidMount(){
        var that = this;
        $(this.refs.CheckBox)
            .checkbox({
                onChange: function () {
                    that.handlerChange({
                        target: this
                    });
                }
            });
    }

    handlerChange (event) {
        var that = this;
        var newValue = event.target.checked;
        this.setState({checked: newValue}, function () {
            if(typeof that.props.onchange === "function")
                that.props.onchange({
                    target:{
                        checked: newValue
                    }
                });
        });

    }

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        if (nextProps.checked !== undefined) {
            this.setState({checked : nextProps.checked});
        }
        if(nextProps.value !== undefined && nextProps.value !== this.props.value) {
            this.setState({
                value: nextProps.value
            })
        }
    }

    render(){

        var radioStyle = "";
        if(this.props.type === "slider")
            radioStyle = "slider";
        else if(this.props.type === "toggle")
            radioStyle = "toggle";
        else
            radioStyle = "";

        return (
            <div className={this.state.status}>
                <div className={"ui "+radioStyle+" checkbox"} ref="CheckBox">
                    <input type="checkbox" name={this.props.name}  tabIndex={this.props.tabindex}
                           className="hidden" checked={this.state.checked || false}
                           placeholder={this.props.placeholder} value={this.props.value || ""}
                           onChange={this.handlerChange} />
                    {this.props.label ? <label>{this.props.label}</label> : null}
                </div>
            </div>
        )
    }

}