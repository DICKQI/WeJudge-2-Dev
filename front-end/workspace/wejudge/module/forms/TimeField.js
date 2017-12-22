/**
 * Created by lancelrq on 2017/7/7.
 */

module.exports = TimeField;

var React = require('react');
var Field = require('./Field');

class TimeField extends Field{

    constructor(props) {
        super(props);
    }

    componentDidMount() {
        
        $(this.refs.datetime_picker_area).datetimepicker({
            datepicker:false,
            format:'H:i:s',
            value: this.state.value
        });

    }

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        this.setState({ value : nextProps.value || this.state.value || ""});
        $(this.refs.datetime_picker_area).datetimepicker('setOptions', {
            value: nextProps.value || this.state.value || ""
        });
    }
    
    render(){
        return (
            <div className={this.state.status}>
                {this.props.label ? <label>{this.props.label}</label> : null}
                    <input
                        ref="datetime_picker_area"
                        type={"text"}
                        name={this.props.name}
                        placeholder={this.props.placeholder || "请输入时间，格式可以为HH:mm:SS"}
                        value={this.state.value}
                        onChange={this.handlerChange}
                        onBlur={this.onBlur}
                    />
            </div>
        )
    }

}