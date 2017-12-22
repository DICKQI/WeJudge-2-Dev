/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = EditableTextField;

var React = require('react');
var Field = require('./Field');

class EditableTextField extends Field{

    constructor(props) {
        super(props);
        this.state['edit'] = false;

        this.editOn = this.editOn.bind(this);
        this.editOff = this.editOff.bind(this);
        this.OKClick = this.OKClick.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        this.setState({ value : nextProps.value || ""});
    }

    editOn(){
        this.setState({edit: true});
    }

    editOff(){
        this.setState({edit: false});
    }

    OKClick(){
        if(typeof this.props.submit == 'function'){
            this.props.submit()
        }
        this.setState({edit: false});
    }

    render(){
        return this.state.edit ? (
            <div className="ui mini icon input">
                <input type={(this.props.type == "password") ? "password" : "text"}
                   name={this.props.name}
                   placeholder={this.props.placeholder}
                   value={this.state.value}
                   maxLength={this.props.maxLength}
                   onChange={this.handlerChange}
                   size={this.props.size}
                />
                <i className="save link icon" onClick={this.OKClick}></i>
            </div>
        ) : (
            <div>{this.state.value} <a onClick={this.editOn}><i className="edit icon"></i></a></div>
        )
    }

}