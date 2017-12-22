/**
 * Created by lancelrq on 2017/3/4.
 */

module.exports = RangeField;

var React = require('react');
var Field = require('./Field');

class RangeField extends Field{

    constructor(props) {
        super(props);
        if(typeof this.props.format == "function")
            this.format = this.props.format;
        else
            this.format = function (v){return v;}
    }

    componentDidMount() {
        $(this.refs.IptRange).popup({
            popup: $(this.refs.PopValue),
            position: 'bottom left'
        });
    }

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        this.setState({ value : nextProps.value || 0});
    }

    render(){
        return (
            <div className={this.state.status}>
                {this.props.label ? <label>{this.props.label} {this.props.label_value ? ("(当前："+this.format(this.state.value)+")") : ""}</label> : null}
                {this.format(this.props.min)}　
                <input type="range"
                       name={this.props.name}
                       value={this.state.value}
                       min={this.props.min}
                       max={this.props.max}
                       step={this.props.step}
                       ref="IptRange"
                       onChange={this.handlerChange}
                       style={(this.props.width) ? {"width": this.props.width}: {"width": "auto"}}
                />　{this.format(this.props.max)}
                <div className="ui popup" ref="PopValue">
                    {this.format(this.state.value)}
                </div>
            </div>
        )
    }

}