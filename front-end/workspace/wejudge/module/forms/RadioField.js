/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = RadioField;

var React = require('react');
var Field = require('./Field');

class RadioField extends Field{

    constructor(props){
        super(props);
        this.state['checked'] = props.checked == true;
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

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        if (nextProps.checked != undefined) {
            this.setState({checked : nextProps.checked});
        }else{
            this.setState({checked : false});
        }
        if(nextProps.value != undefined && nextProps.value != this.props.value){
            this.setState({
                value: nextProps.value
            })
        }
    }

    handlerChange (event) {
        var newValue = event.target.checked;
        if(typeof this.props.onchange == "function")
            this.props.onchange(event);
    }
  
    render(){
        var radioStyle = "";
        if(this.props.type == "slider")
            radioStyle = "slider";
        else if(this.props.type == "toggle")
            radioStyle = "toggle";
        else
            radioStyle = "";
        return (
            <div className={this.state.status}>
                <div className={"ui "+ radioStyle + " radio checkbox"} ref="CheckBox">
                    <input type="radio" name={this.props.name}  tabIndex={this.props.tabindex}
                           className="hidden" checked={this.state.checked} value={this.props.value}
                           placeholder={this.props.placeholder} onChange={this.handlerChange} />
                    {this.props.label ? <label>{this.props.label}</label> : null}
                </div>
            </div>
        )
    }

}