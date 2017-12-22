/**
 * Created by lancelrq on 2017/2/16.
 */

module.exports = {
    FormComponent: FormComponent,
    TextField: require('./forms/TextField'),
    TextAreaField: require('./forms/TextAreaField'),
    CheckBoxField: require('./forms/CheckBoxField'),
    RadioField: require('./forms/RadioField'),
    SelectField: require('./forms/SelectField'),
    FileField: require('./forms/FileField'),
    ImageField: require('./forms/ImageField'),
    CKEditorField: require("./forms/CKEditorField"),
    RangeField: require("./forms/RangeField"),
    RatingField: require("./forms/RatingField"),
    CodeMirrorField: require("./forms/CodeMirrorField"),
    EditableTextField: require("./forms/EditableTextField"),
    DateTimeField: require("./forms/DateTimeField"),
    TimeField: require("./forms/TimeField"),
    SearchField: require("./forms/SearchField")
};

var React = require('react');


class FormComponent extends React.Component{
    constructor(props) {
        super(props);
        this.submitting = false;
        this.doSubmit = this.doSubmit.bind(this);
        this.submit = this.submit.bind(this);

    }
    componentDidMount() {
        if (this.props.autosave){
            var sis = $(this.refs.MainForm).sisyphus({
                locationBased: true,
                timeout: 0,
                onSave: function () {
                    $(window).bind('beforeunload',function(){
                        return "确定离开此页面吗？未保存的内容将会丢失！";
                    });
                }
            });
            window.onunload = function () {
                sis.manuallyReleaseData();
            };
        }
    }

    unBindAutoSave(){
        if (this.props.autosave) {
            $(window).unbind('beforeunload');
        }
    }

    getData(getDataSuccess, getDataFailed, query=null){
        // 获取Form的初始内容
        var that = this;
        that.refs.ProcessingDimmer.show();
        var core = require('wejudge-core');
        core.restful({
            method: 'POST',
            responseType: "json",
            url: that.apis.data,
            data: query,
            success: function (rel) {
                that.refs.ProcessingDimmer.hide();
                that.refs.Messager.hide();
                if(typeof getDataSuccess == "function")
                    getDataSuccess(rel);
            },
            error: function (rel, msg) {
                that.refs.ProcessingDimmer.hide();
                that.refs.Messager.show("数据加载失败，请刷新页面重试", msg, 'error');
                if(typeof getDataFailed == "function")
                    getDataFailed(rel, msg);
            }
        }).call();
    }

    submit(){
        this.refs.btnSubmitInside.click();
    }
    
    doSubmit(e) {
        e.preventDefault();
        if(this.submitting) return false;
        this.submitting = true;
        var that = this;
        that.refs.FormMessager.hide();
        that.refs.ProcessingDimmer.show();
        var core = require('wejudge-core');
        core.restful({
            method: 'POST',
            responseType: "json",
            url: that.apis.submit,
            success: function (rel) {
                that.submitting = false;
                that.refs.ProcessingDimmer.hide();
                that.unBindAutoSave();
                if(typeof that.doSubmitSuccess == "function")
                    that.doSubmitSuccess(rel);
            },
            error: function (rel, msg) {
                that.submitting = false;
                that.refs.ProcessingDimmer.hide();
                if(typeof that.doSubmitFailed == "function")
                    that.doSubmitFailed(rel, msg);
            }
        }).submit_form(e.target);
        return false;
    };

    renderForm(form_body, form_size){
        var core = require("wejudge-core");
        return (
            <form className={`ui ${form_size} form`} method="post" action={this.props.api} onSubmit={this.doSubmit} ref="MainForm">
                <core.dimmer.Loader inverted title="处理中" ref="ProcessingDimmer"/>
                <core.dimmer.Messager inverted title="数据加载失败" ref="Messager"/>
                <core.dimmer.FormMessager inverted ref="FormMessager" />
                {form_body}
                <input type="submit" style={{display: "none"}} ref="btnSubmitInside"/>
            </form>
        )
    }
}
