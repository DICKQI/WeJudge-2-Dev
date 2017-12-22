/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = ImageField;

var React = require('react');
var Field = require('./Field');
var restful = require('../../module/restful');

class ImageField extends Field{

    constructor(props){
        super(props);
        this.state = {
            new_file_url: "",
            new_file_url_view: "",
            uploading: 0,
            upload_process: 0,
            errmsg: ""
        };
        this.callFileDialog = this.callFileDialog.bind(this);
        this.abortUploading = this.abortUploading.bind(this);
    }

    componentDidUpdate() {
        if(this.refs.NavViewImage) {
            $(this.refs.NavViewImage).popup({
                popup: $(this.refs.ImageViewer)
            });
        }
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

    callFileDialog(){
        var filearea = this.refs.FileArea;
        filearea.click();
    }
    abortUploading(){
        if(this.worker) this.worker.abort();
        this.worker = null;
    }

    handlerChange(e){
        var filearea = e.target;
        var file = null;
        if(filearea.files.length > 0){
            file = filearea.files[0];
            var typeAvailable = (
                file.type == "image/png" ||
                file.type == "image/jpg"  ||
                file.type == "image/jpeg"  ||
                file.type == "image/bmp"
            );
            var sizeAvailable = file.size < (this.props.max_size || (1024 * 1024));
            if( !(typeAvailable && sizeAvailable) )
                file = null;
        }
        filearea.value = "";
        this.autoUpload(file);
    }

    autoUpload(file){
        if(file != null){
            var fd = new FormData();
            fd.append("uploadImageFile", file);
            this.setState({
                uploading: 1,
                new_file_url: ""
            });
            var that = this;
            this.worker = restful({
                url: this.props.upload_api,
                formdata: fd,
                responseType: 'json',
                success:function(rel){
                    that.setState({
                        uploading: 2,
                        new_file_url: rel.data,
                        new_file_url_view: rel.data + "?_t=" + Math.random()
                    });
                },
                error: function (msg) {
                    that.setState({
                        uploading: 3,
                        new_file_url: "",
                        errmsg: msg
                    })
                },
                abort: function () {
                    // 用户终止
                    that.setState({
                        uploading: 0,
                        new_file_url: ""
                    })
                },
                progress: function (perc, loaded, total) {
                    that.setState({
                        upload_process: perc
                    })
                }
            }).upload();
        }
    }

    render(){
        var viewMessage = () => {
            if(this.state.uploading == 1){
                return (<div className="header">照片上传中...{this.state.upload_process.toFixed(2)}% <a href="javascript:void(0)" onClick={this.abortUploading}>取消上传</a></div>)
            }else if(this.state.uploading == 2){
                return (<div><div className="header">照片已经上传，<a ref="NavViewImage">查看预览</a>。</div><p>拖动图片文件到这里或者点击<a href="javascript:void(0)" onClick={this.callFileDialog}>选择图片</a></p></div>);
            }else if(this.state.uploading == 3){
                return (<div><div className="header">上传过程出现问题，请重试。问题描述：{this.state.errmsg}</div><p>拖动图片文件到这里或者点击<a href="javascript:void(0)" onClick={this.callFileDialog}>选择图片</a></p></div>);
            }
            else{
                return (<div className="header">拖动图片文件到这里或者点击<a href="javascript:void(0)" onClick={this.callFileDialog}>选择图片</a></div>);
            }
        };
        return (
            <div>
                <strong>{this.props.label}</strong>
                <div className="ui message" ref="dropArea">
                    {viewMessage()}
                </div>
                <input type="file" accept="image/png,image/jpg,image/jpeg,image/bmp"
                       placeholder={this.props.placeholder}
                       onChange={this.handlerChange}
                       ref="FileArea"
                       style={{display: "none"}}
                />
                <div className="ui popup" ref="ImageViewer">
                    <div className="header">照片预览</div>
                    <img src={this.state.new_file_url_view} alt="" width="200"/>
                </div>
                <input type="hidden" name={this.props.name} value={this.state.new_file_url} />
            </div>
        )
    }

}