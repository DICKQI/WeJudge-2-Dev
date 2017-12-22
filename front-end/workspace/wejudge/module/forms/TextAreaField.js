/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = TextAreaField;

var React = require('react');
var Field = require('./Field');

class TextAreaField extends Field{

    constructor(props) {
        super(props);
    }

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        this.setState({ value : nextProps.value });
    }

    render(){
        return (
            <div className={this.state.status}>
                {this.props.label ? <label>{this.props.label}</label> : null}
                <textarea name={this.props.name} rows={this.props.rows ? this.props.rows : "5"} placeholder={this.props.placeholder} onChange={this.handlerChange} value={this.state.value}></textarea>
            </div>
        )
    }

}