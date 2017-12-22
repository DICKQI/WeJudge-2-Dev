/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = CKEditorField;

var React = require('react');
var Field = require('./Field');

//
// var CKEditor = require("react-ckeditor-component").default;
//
// class CKEditorField extends React.Component {
//     constructor(props) {
//         super(props);
//         this.updateContent = this.updateContent.bind(this);
//         this.state = {
//             content: props.value,
//         }
//     }
//
//     updateContent(newContent) {
//         this.setState({
//             content: newContent
//         })
//     }
//
//     componentWillReceiveProps(nextProps) {
//         console.log(nextProps)
//         this.setState({ content : nextProps.value });
//     }
//
//     render() {
//         return (
//             <CKEditor activeClass="p10" content={this.state.content} onChange={this.updateContent} />
//         )
//     }
// }


class CKEditorField extends Field{

    constructor(props) {
        super(props);
        this.ckeditor = null;
    }

    componentDidMount() {
        var that = this;
        this.ckeditor = CKEDITOR.replace(this.refs.CKEditorArea, { height:this.props.height || "15em" });
        this.ckeditor.on('change', function(event) {
            var data = this.getData();
            that.setState({
                value: data
            })
        });
    }

    componentWillReceiveProps(nextProps) {
        var that = this;
        super.componentWillReceiveProps(nextProps);
        this.setState(
            { value : nextProps.value || this.state.value || ""},
            function () {
                setTimeout(function () {
                    if(that.ckeditor){
                        that.ckeditor.setData(that.state.value);
                    }
                }, 100);
            }
        );

    }

    render(){
        return (
            <div className={this.state.status}>
                {this.props.label ? <label>{this.props.label}</label> : null}
                <textarea name={this.props.name}
                          placeholder={this.props.placeholder}
                          onChange={this.handlerChange}
                          value={this.state.value}
                          ref="CKEditorArea"></textarea>
            </div>
        )
    }

}
