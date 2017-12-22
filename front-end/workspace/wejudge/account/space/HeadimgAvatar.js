/**
 * Created by lancelrq on 2017/7/30.
 */

var React = require("react");
var core = require("wejudge-core");

module.exports = HeadimgAvatar;


class HeadimgAvatar extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            uploadable: false
        };
        this.avatar = {
            x: 0, y: 0, w: 0, h: 0
        };
        this.jcrop = null;
        this.onUploadFieldChange = this.onUploadFieldChange.bind(this);
        this.doUpload = this.doUpload.bind(this);
    }

    getJCropValue(sender) {
        return function (obj) {
            sender.avatar.x = obj.x;
            sender.avatar.y = obj.y;
            sender.avatar.w = obj.w;
            sender.avatar.h = obj.h;
        }
    }

    onUploadFieldChange() {
        if (this.jcrop !== null) {
            this.jcrop.destroy();
            this.jcrop = null;
        }
        this.setState({
            uploadable: false
        });
        var that = this;
        var holderDOM = that.refs.avatar_holder;
        var uploaderDOM = that.refs.image_upload;
        var file = uploaderDOM.files[0];
        this.avatar = {
            x: 0, y: 0, w: 0, h: 0
        };
        holderDOM.src = "/static/images/user_placeholder.png";
        this.jcrop = null;
        if (file !== undefined) {
            if (file.type.indexOf('image') < 0 || file.size > 2 * 1024 * 1024) {
                this.refs.FormMessager.show("错误", "不支持的文件格式或者文件太大，仅支持图片格式文件jpg、png，并且大小在 2MB 以内。", "error");
            } else {
                var reader = new FileReader();
                reader.onload = function (e) {
                    var imgdata = e.target.result;
                    holderDOM.src = imgdata;
                    $(holderDOM).Jcrop({
                        aspectRatio: 1,
                        onSelect: that.getJCropValue(that),
                        onChange: that.getJCropValue(that),
                        minSize: [180, 180],
                        boxWidth: 500,
                    }, function () {
                        that.jcrop = this;
                        that.setState({
                            uploadable: true
                        });
                        var img_size = that.jcrop.getBounds();
                        var img_w = img_size[0];
                        var img_h = img_size[1];
                        var scale = 500.0 / img_w;
                        console.log(scale);
                        that.jcrop.setOptions({
                            boxHeight: scale * img_h
                        });
                        that.refs.FormMessager.show("提示", "请在图片上拖动鼠标选区头像区域，再点击上传", "info");

                    });
                };
                reader.readAsDataURL(file);
            }
        } else {
            that.refs.FormMessager.hide();
        }
    }

    doUpload() {
        this.refs.FormMessager.hide();
        this.setState({
            uploadable: false
        });
        var that = this;
        var fd = new FormData();
        var uploaderDOM = this.refs.image_upload;
        if (this.avatar.w === 0 || this.avatar.h === 0) {
            this.refs.FormMessager.show("提示", "请先在图片上拖动鼠标选区头像区域", "warning");
            this.setState({
                uploadable: true
            });
            return false;
        }
        fd.append("headimg", uploaderDOM.files[0]);
        fd.append("x", this.avatar.x + 1);
        fd.append("y", this.avatar.y + 1);
        fd.append("w", this.avatar.w);
        fd.append("h", this.avatar.h);
        core.restful({
            url: that.props.upload_api,
            formdata: fd,
            responseType: 'json',
            success: function (data) {
                that.setState({
                    uploadable: true
                });
                that.refs.alertbox.showSuccess(data, function () {
                    window.location.reload();
                });
            },
            error: function (errmsg) {
                that.setState({
                    uploadable: true
                });
                that.refs.FormMessager.show("上传失败", errmsg, "error");
            },
            abort: function () {
                that.setState({
                    uploadable: true
                });
            },
            progress: function (perc, loaded, total) {
                // $("#uploadProgressBarBody").css('width', perc + "%").text(parseInt(perc) + "%");
            }
        }).upload();
    }

    render() {
        return (
            <div className="ui segment">
                <div style={{textAlign: "center", "overflow": "hidden"}}>
                    <img src="/static/images/user_placeholder.png" ref="avatar_holder" id="avatar_holder"/>
                </div>
                <div className="ui form">
                    <br/>
                    <div className="ui fluid field">
                        <label htmlFor="image_upload">上传头像</label>
                        <input type="file" ref="image_upload" name="image_upload"
                               onChange={this.onUploadFieldChange}/>
                    </div>
                    <a onClick={this.doUpload}
                       className={`ui ${!this.state.uploadable && "disabled"} fluid primary button`}>
                        <i className="upload icon"></i>上传
                    </a>
                </div>
                <core.dimmer.FormMessager inverted ref="FormMessager"/>
                <core.dialog.Alert ref="alertbox" msg_title="保存成功" msg="点击确定刷新页面"/>
            </div>
        )
    }
}