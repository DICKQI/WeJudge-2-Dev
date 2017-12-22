/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = TextField;

var React = require('react');
var Field = require('./Field');

class TextField extends Field{

    constructor(props) {
        super(props);
        
    }

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        this.setState({ value : (nextProps.value === undefined || nextProps.value === null) ? "" : nextProps.value });
    }


    render(){
        return (
            <div className={this.state.status}>
                {this.props.label ? <label>{this.props.label}</label> : null}
                <div className={`ui ${this.props.icon_align || "left"} ${this.props.transparent && "transparent"} ${this.props.icon && "icon"} input`}>
                    {this.props.icon ? <i className={`${this.props.icon || ""} icon`}></i> : null}
                    <input type={(this.props.type === "password") ? "password" : "text"}
                           name={this.props.name}
                           placeholder={this.props.placeholder}
                           value={this.state.value}
                           maxLength={this.props.maxLength}
                           onChange={this.handlerChange}
                           readOnly={this.props.readonly}
                   />
                </div>
            </div>
        )
    }

}