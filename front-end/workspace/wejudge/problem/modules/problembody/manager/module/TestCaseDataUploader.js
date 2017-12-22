/**
 * Created by lancelrq on 2017/3/19.
 */

module.exports = TestCaseDataUploader;

var React = require('react');
var core = require('wejudge-core');


class TestCaseDataUploader extends React.Component {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            entity: {},
            uploadIn: "",
            uploadOut: ""
        };
    }

    show(entity){
        var that = this;
        this.setState({
            entity: entity,
            uploadIn: this.props.apis.uploadIn+ "?handle=" + entity.handle,
            uploadOut: this.props.apis.uploadOut+ "?handle=" + entity.handle
        });
        this.refs.FormDialog.show();
    }
    render(){
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" size="small" title="上传测试数据内容" btnShow={false}>
                    <span className="header">输入</span>
                    <core.forms.FileField ref="InUpload" upload_api={this.state.uploadIn} auto/>
                    <span className="header">输出</span>
                    <core.forms.FileField ref="OutUpload" upload_api={this.state.uploadOut} auto/>
                    <i className="info circle icon"></i> 由于处于Linux评测环境，如果测试数据文件包含中文，请务必上传UTF-8编码格式的测试数据文件，否则无法使用！
                    <br />
                    <i className="info circle icon"></i> Windows下的文本文件换行符默认是\r\n，Linux是\n，请根据题目需要注意<strong>输出数据</strong>的换行格式
                </core.dialog.Dialog>
            </div>
        );
    }

}