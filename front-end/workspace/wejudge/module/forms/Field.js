/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = Field;

var React = require('react');

class Field extends React.Component {
    constructor(props) {
        super(props);

        this.fieldStatus = {
            disabled: props.disabled === true,
            readonly: props.readonly === true,
            error: props.error === true,
            required: props.required === true,
            inline: props.inline === true,
            ui: props.ui === true,
            input: props.input === true,
            transparent: props.transparent === true,

        };
        this.state = {
            value: (props.value === undefined || props.value === null) ? "" : props.value,
            status: this.getFieldStatus()
        };
        this.handlerChange = this.handlerChange.bind(this);
        this.onBlur = this.onBlur.bind(this);
    }

    getValue(){
        return this.state.value;
    }

    setValue(val){
        this.setState({
            value: val
        })
    }

    onBlur(e){
        if(typeof this.props.onblur === "function"){
            this.props.onblur(e);
        }
    }

    getFieldStatus(){
        var fieldStatus = [];
        if(this.fieldStatus.disabled) fieldStatus.push("disabled");
        if(this.fieldStatus.readonly) fieldStatus.push("readonly");
        if(this.fieldStatus.error) fieldStatus.push("error");
        if(this.fieldStatus.required) fieldStatus.push("required");
        if(this.fieldStatus.inline) fieldStatus.push("inline");
        if(this.fieldStatus.ui) fieldStatus.push("ui");
        if(this.fieldStatus.input) fieldStatus.push("input");
        if(this.fieldStatus.transparent) fieldStatus.push("transparent");

        fieldStatus.push("field");
        return fieldStatus.join(" ")
    }

    componentWillReceiveProps(nextProps){
        this.fieldStatus = {
            disabled: nextProps.disabled === true,
            readonly: nextProps.readonly === true,
            error: nextProps.error === true,
            required: nextProps.required === true,
            inline: nextProps.inline === true,
            ui: nextProps.ui === true,
            input: nextProps.input === true,
            transparent: nextProps.transparent === true
        };
        this.setState({
            status: this.getFieldStatus()
        })
    }


    handlerChange (event) {
        var newValue = event.target.value;
        this.setState({value: newValue});
        if(typeof this.props.onchange === "function")
            this.props.onchange(event);
    }

}
