/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = FileField;

var React = require('react');
var Field = require('./Field');


class FileField extends Field{

    constructor(props){
        super(props);
        this.state = {
            files: [],
            fileStatus: [],
            uploadUrls: [],
            uploading: [],
            upload_process: [],
            errmsg: []
        };
        this.callFileDialog = this.callFileDialog.bind(this);
        this.abortUploading = this.abortUploading.bind(this);
    }

    componentDidMount(){
        var droparea = this.refs.dropArea;
        var filearea = this.refs.FileArea;

        droparea.addEventListener("dragenter", dragenter, false);
        droparea.addEventListener("dragover", dragover, false);
        droparea.addEventListener("drop", drop, false);
        function dragenter(e) {
            e.stopPropagation();
            e.preventDefault();
        }

        function dragover(e) {
            e.stopPropagation();
            e.preventDefault();
        }
        function drop(e) {
            e.stopPropagation();
            e.preventDefault();

            var dt = e.dataTransfer;

            filearea.files = dt.files;
        }
    }

    getFiles(){
        return this.state.files;
    }

    refreshFileItemStatus(key, msg){
        var fileStatus = this.state.fileStatus;
        fileStatus[key] = msg;
        this.setState({
            fileStatus: fileStatus
        });
    }

    callFileDialog(){
        this.refs.FileArea.click();
    }

    handlerChange(e){
        var filearea = e.target;
        var files = [];
        var uploadUrls = [];
        var uploading = [];
        var upload_process = [];
        var errmsg = [];
        for(var i = 0; i < filearea.files.length; i++) {
            if(typeof this.props.onFileSelected == "function") {
                // 这个事件触发的时候，如果文件不符合要求，这个传入事件的函数可以返回false以不让这个文件进入到上传队列
                if(!this.props.onFileSelected(filearea.files[i])){
                    continue;
                }
            }
            files[i] = filearea.files[i];
            uploadUrls[i] = "";
            uploading[i] = 0;
            upload_process[i] = 0;
            errmsg[i] = 0;
            if(!this.props.multiple) break; // 确保只有一个可用
        }

        this.setState({
            files: files,
            uploadUrls: uploadUrls,
            uploading: uploading,
            upload_process: upload_process,
            errmsg: errmsg
        });
        this.hasChange = true;
        if(typeof this.props.onChange == "function"){
            //回调onChange事件
            this.props.onChange(this);
        }
    }

    componentDidUpdate() {
        if(this.hasChange) {
            this.hasChange = false;
            if(this.props.auto)
                this.upload();
        }
    }


    upload(){
        var that = this;
        this.uploadIndex = 0;
        if(this.state.files && this.state.files.length == 0){
            alert("请选择要上传的文件");
            return;
        }
        var run = function () {
            if(that.state.files != null){
                if(that.state.uploading[that.uploadIndex] == 2) {
                    that.uploadIndex++;
                    that.thread = setTimeout(run, 500);
                    return;
                }
                var file = that.state.files[that.uploadIndex];
                if(!file){
                    if(that.thread)
                        clearTimeout(that.thread);
                    that.thread = null;
                    return;
                }
                var fd = new FormData();
                fd.append("uploadFile", file);
                var uploadUrls = that.state.uploadUrls;
                var uploading  = that.state.uploading;
                var upload_process = that.state.upload_process;
                var errmsg = that.state.errmsg;
                uploading[that.uploadIndex] = 1;   //uploading
                uploadUrls[that.uploadIndex] = "";
                that.setState({
                    uploading: uploading,
                    uploadUrls: uploadUrls
                });
                var core = require("wejudge-core");
                that.worker = core.restful({
                    url: that.props.upload_api,
                    formdata: fd,
                    responseType: 'json',
                    success:function(rel){
                        uploading[that.uploadIndex] = 2;   //success
                        uploadUrls[that.uploadIndex] = rel.data;
                        errmsg[that.uploadIndex] = rel.msg;
                        that.setState({
                            uploading: uploading,
                            uploadUrls: uploadUrls,
                            errmsg: errmsg
                        });
                        that.uploadIndex++;
                        that.thread = setTimeout(run, 500);
                    },
                    error: function (msg) {
                        uploading[that.uploadIndex] = 3;   //error
                        uploadUrls[that.uploadIndex] = "";
                        errmsg[that.uploadIndex] = msg;
                        that.setState({
                            uploading: uploading,
                            uploadUrls: uploadUrls,
                            errmsg: errmsg
                        });
                        that.uploadIndex++;
                        // if(that.thread)
                        //     clearTimeout(that.thread);
                        // that.thread = null;
                    },
                    abort: function () {
                        // 用户终止
                        uploading[that.uploadIndex] = 0;   //pending
                        uploadUrls[that.uploadIndex] = "";
                        that.setState({
                            uploading: uploading,
                            uploadUrls: uploadUrls
                        });
                        if(that.thread)
                            clearTimeout(that.thread);
                        that.thread = null;
                    },
                    progress: function (perc, loaded, total) {
                        upload_process[that.uploadIndex] =perc;
                        that.setState({
                            upload_process: upload_process
                        })
                    }
                }).upload();
            }
        };
        that.thread = setTimeout(run, 500);
    }

    abortUploading(){
        if(this.worker) this.worker.abort();
        this.worker = null;
        if(that.thread)
            clearTimeout(that.thread);
        that.thread = null;

    }

    render(){
        var viewMessage = (key) => {
            if(this.state.uploading[key] == 1){
                return (<div>上传中...{this.state.upload_process[key].toFixed(2)}% <a href="javascript:void(0)" onClick={this.abortUploading}>取消上传</a></div>)
            }else if(this.state.uploading[key] == 2){
                return (<div>上传成功！<br/><span dangerouslySetInnerHTML={{__html: this.state.errmsg[key] }}></span></div>);
            }else if(this.state.uploading[key] == 3){
                return (<div>上传过程出现问题，请重试。<br/>问题描述：<span dangerouslySetInnerHTML={{__html: this.state.errmsg[key] }}></span></div>);
            }
            else{
                return (<div>等待上传</div>);
            }
        };
        return (
            <div>
                <strong>{this.props.label}</strong>
                <div className="ui message" ref="dropArea">
                    <div className="header">拖动文件到这里或者点击<a href="javascript:void(0)" onClick={this.callFileDialog}>选择文件</a></div>
                    {(this.state.files && this.state.files.length > 0) ?
                        <div className="ui list">
                        {
                            this.state.files.map((item, key)=> {
                                return (
                                    <div key={key} className="item">
                                        <i className="file icon"></i>
                                        <div className="content">
                                            <div>{item.name}</div>
                                            <div className="description" title={this.state.errmsg[key]}>
                                                {viewMessage(key)}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })
                        }
                    </div> : "" }

                </div>
                <input type="file"
                       multiple={this.props.multiple}
                       placeholder={this.props.placeholder}
                       onChange={this.handlerChange}
                       ref="FileArea"
                       style={{display: "none"}}
                />
            </div>
        )
    }

}