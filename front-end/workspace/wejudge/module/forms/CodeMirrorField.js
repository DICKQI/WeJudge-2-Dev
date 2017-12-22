/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = CodeMirrorField;

var React = require('react');
var Field = require('./Field');

class CodeMirrorField extends Field{

    constructor(props) {
        super(props);
        this.LangList = {
            0: ["纯文本", "text/plain"],
            1: ["C语言 (GNU C)", "text/x-csrc"],
            2: ["C++ (GNU CPP)", "text/x-c++src"],
            4: ["Java 1.8", "text/x-java"],
            8: ["Python 2.7", {
                name: "python",
                version: 2,
                singleLineStringErrors: false
            }],
            16: [ "Python 3.5", {
                name: "python",
                version: 3,
                singleLineStringErrors: false
            }]
        };
        this.state["lang"] = props.lang || 1;
    }

    componentDidMount() {
        this.updateCodeMirror();
    }

    componentDidUpdate() {
        this.updateCodeMirror();
    }

    appendToCursor(text){
        if(this.codemirror) {
            this.codemirror.replaceSelection(text)
        }
    }

    getValue(){
        return this.codemirror.getDoc().getValue();
    }

    setValue(txt){
        this.setState({
            value: txt
        });
        return this.codemirror.getDoc().setValue(txt);
    }

    reset(){
        this.setState({
            value: ""
        });
        this.codemirror.getDoc().setValue("");
    }

    refresh(){
        var that = this;
        setTimeout(function(){
            that.codemirror.refresh();
        }, 200);
    }

    componentWillReceiveProps(nextProps) {
        super.componentWillReceiveProps(nextProps);
        // var newValue = nextProps.value || (this.codemirror && this.codemirror.getValue()) || "";
        var newValue = nextProps.value || "";
        this.setState({
            lang: nextProps.lang,
            value:  newValue
        }, () => {
            this.codemirror.getDoc().setValue(newValue);
            this.updateCodeMirror();
        });

    }

    updateCodeMirror(){
        var that = this;
        var langdata = this.LangList[this.state.lang] || [""];
        if(this.codemirror !== undefined){
            this.codemirror.setOption("mode", langdata[1]);
        }else {
            this.codemirror = CodeMirror.fromTextArea(this.refs.CodeMirrorArea, {
                indentUnit: 4,
                indentWithTabs: true,
                lineNumbers: true,
                mode: langdata[1],
                showCursorWhenSelecting: true,
                autoRefresh: true
            });
        }
        setTimeout(function(){
            that.codemirror.refresh();
        },200);
        this.codemirror.on("change", function (editor, changes) {
            editor.save();
        });
    }

    render(){
        return (
            <div className={this.state.status} style={this.props.no_margin ? {margin: 0} : {}}>
                {this.props.label ? <label>{this.props.label}</label> : null}
                <textarea name={this.props.name}
                          placeholder={this.props.placeholder}
                          value={this.state.value}
                          onChange={this.handlerChange}
                          ref="CodeMirrorArea"></textarea>
            </div>
        )
    }

}