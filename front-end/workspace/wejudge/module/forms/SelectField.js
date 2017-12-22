/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = SelectField;

var React = require('react');
var Field = require('./Field');

class SelectField extends Field {

    constructor(props) {
        super(props);
    }

    componentDidMount(){
        $(this.refs.DropDown).dropdown();
    }

    componentWillReceiveProps(nextProps) {
        var that = this;
        super.componentWillReceiveProps(nextProps);
        if(nextProps.value === undefined || nextProps.value === null){
            this.setState({
                value: ""
            })
        }else{
            if(nextProps.value !== this.props.value){
                this.setState({
                    value: nextProps.value
                })
            }
        }
    }

    componentDidUpdate() {
        if(this.state.value === "") {$(this.refs.DropDown).dropdown("clear");}
        else{ $(this.refs.DropDown).dropdown("set selected", this.state.value); }
    }
    
    render(){
        var selectorStyle;
        if(this.props.type === "selection")
            selectorStyle = "selection";
        else if(this.props.type === "search")
            selectorStyle = "search";
        else
            selectorStyle = "";

        return (
            <div className={this.state.status}>
                {this.props.label ? <label>{this.props.label}</label> : null}
                <select className={`ui ${selectorStyle} ${this.props.fluid ? 'fluid' : ''} dropdown`}
                        value={this.state.value}
                        multiple={this.props.multiple}
                        name={this.props.name}
                        placeholder={this.props.placeholder}
                        ref="DropDown"
                        onChange={this.handlerChange}>
                    {(!this.props.forceDefault) ? (<option value="">请选择</option>) : "" }
                    {this.props.children}
                </select>
            </div>
        )
    }



    handlerChange (event) {
        var newValue = event.target.value;
        if(this.state.value !== newValue) {
            this.setState({value: newValue});
            if (typeof this.props.onchange === "function")
                this.props.onchange(event);
        }
    }

}
