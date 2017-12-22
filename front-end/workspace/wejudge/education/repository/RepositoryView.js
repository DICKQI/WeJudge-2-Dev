/**
 * Created by lancelrq on 2017/8/12.
 */


var React = require("react");
var core = require("wejudge-core");
var RepositoryEditor = require('./RepositoryEditor');

module.exports = RepositoryView;


class RepositoryView extends React.Component {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            path: "./"
        };
        this.onJsTreeChange = this.onJsTreeChange.bind(this);
        this.deleteFolder = this.deleteFolder.bind(this);
        this.deleteRepo = this.deleteRepo.bind(this);
    }


    load(){
        this.refs.jstree.load()
    }
    refreshFolder(){
        this.refs.jstree.refresh()
    }
    loadFiles(){
        this.refs.files_list.load();
    }

    onJsTreeChange(node){
        var that = this;
        this.setState({
            path: node.id
        }, function () {
            that.loadFiles();
        })
    }
    deleteRepo(){
        // 删除仓库
        var that = this;
        that.refs.confirm.setContent('操作确认', "你确定要删除这个仓库吗？仓库内的所有文件都会被删除！").show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.delete_repo,
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            window.location.href = that.props.urls.repos_list
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        });
    }
    deleteFolder(){
        // 删除文件夹
        var that = this;
        var msg;
        if (this.state.path === "#" || this.state.path === "/" || this.state.path === "./" )
            msg = '你确定要清空整个文件仓库吗';
        else
            msg = '你确定要删除当前文件夹吗？将要永久删除这个文件夹内的所有文件！';
        that.refs.confirm.setContent('操作确认', msg).show(function (rel) {
            if (rel) {
                core.restful({
                    url: that.props.apis.delete_path + "?path=" + that.state.path,
                    method: "POST",
                    success: function (rel) {
                        that.refs.alertbox.showSuccess(rel, function () {
                            that.refs.jstree.refresh();
                            that.refs.jstree.selectNode(rel.data);
                        });
                    },
                    error: function (rel, msg) {
                        that.refs.alertbox.showError(rel, msg);
                    }
                }).call()
            }
        });
    }

    render() {
        var that = this;
        var path_list = this.state.path.split("/");
        return (
            <div className="ui">
                {this.props.options.is_teacher ? <div className="ui menu">
                    <a className="item" onClick={function (that) {
                        return function () {
                            that.refs.dialog_upload.show();
                        }
                    }(this)}><i className="upload icon"></i> 上传文件</a>
                    <a className="item" onClick={function (that) {
                        return function () {
                            that.refs.dialog_newfolder.show();
                        }
                    }(this)}><i className="folder icon"></i> 新建文件夹</a>
                    <a className="item" onClick={this.deleteFolder}><i className="remove icon"></i>
                        {this.state.path === "#" || this.state.path === "/" || this.state.path === "./" ? "清空仓库" : "删除文件夹"}
                    </a>
                    <div className="right menu">
                        <a className="item" onClick={function (that) {
                            return function () {
                                that.refs.editor.modify();
                            }
                        }(this)}><i className="edit icon"></i> 编辑仓库</a>
                        <a className="item" onClick={this.deleteRepo}><i className="remove circle outline icon"></i> 删除仓库</a>
                    </div>
                </div> : null}
                <div className="ui stackable grid">
                    <div className="four wide column">
                        <div className="ui black segment">
                            <core.JSTree
                                ref="jstree"
                                get_data={this.props.apis.get_folders}
                                onchange={this.onJsTreeChange}
                            />
                        </div>
                    </div>
                    <div className="twelve wide column">
                        <div className="ui segment">
                            <div className="ui breadcrumb">
                                <span className="section"><strong>当前位置：</strong></span>
                                {path_list.map(function (val, key) {
                                    if(!val) return;
                                    return [key !== 0 ? <i className="right chevron icon divider"></i> : null, <span className="section">{val === '.' ? "根目录" : val }</span>]
                                })}
                            </div>
                        </div>
                        <RepositoryFilesList
                            ref="files_list"
                            get_files={this.props.apis.get_files}
                            delete_path={this.props.apis.delete_path}
                            path={this.state.path}
                            manager={this}
                        />
                    </div>
                </div>
                <NewFolder
                    manager={this}
                    ref="dialog_newfolder"
                    new_folder={this.props.apis.new_folder}
                    path={this.state.path}
                />
                <UploadFile
                    manager={this}
                    ref="dialog_upload"
                    upload_file={this.props.apis.upload_file}
                    path={this.state.path}
                />
                <RepositoryEditor
                    manager={this}
                    ref="editor"
                    apis={this.props.apis}
                />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm msg="" msg_title="操作确认" ref="confirm" />
            </div>
        )
    }
}

class RepositoryFilesList extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.manager = props.manager;
        this.state['path'] = props.path;
        this.apis = {
            data: props.get_files
        };
        this.downloadFiles = this.downloadFiles.bind(this);
        this.deleteFiles = this.deleteFiles.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        this.setParams({
            path: nextProps.path
        });
        this.setState({
            path: nextProps.path
        });
    }


    deleteFiles(file_name){
        // 删除文件
        var that = this;
        return function(){
            var fp = that.state.path.substring(that.state.path.length-1) !== "/" ? that.state.path + "/" : that.state.path;
            fp +=  file_name;
            that.refs.confirm.setContent('操作确认', '你确定要删除当前文件吗？将要永久删除这个文件！').show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.delete_path + "?path=" + fp,
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.manager.loadFiles();
                            });
                        },
                        error: function (rel, msg) {
                            that.refs.alertbox.showError(rel, msg);
                        }
                    }).call()
                }
            });
        }
    }

    downloadFiles(file_name){
        var that = this;
        return function() {
            var fp = that.state.path.substring(that.state.path.length - 1) !== "/" ? that.state.path + "/" : that.state.path;
            fp += file_name;
            window.open(that.manager.props.urls.root + fp);
        };
    }


    renderListHeader(){
        return (
            <tr>
                <th>文件名</th>
                <th>文件大小</th>
                <th>修改时间</th>
                <th>管理</th>
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key}>
                        <td>{core.tools.generateIcon(item.file_name)}{item.file_name}</td>
                        <td>{core.tools.bytesToSize(item.size)}</td>
                        <td>{core.tools.format_datetime(item.modify_time)}</td>
                        <td>
                            <a className="ui tiny compact primary button" onClick={this.downloadFiles(item.file_name)}>下载</a>
                            {this.manager.props.options.is_teacher ? <a className="ui tiny compact red button" onClick={this.deleteFiles(item.file_name)}>删除</a> : null}
                        </td>
                    </tr>
                )
            });
        else
            return null
    }

    renderFooterBody() {
        return <div>
            <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            <core.dialog.Confirm msg="" msg_title="操作确认" ref="confirm" />
        </div>
    }
}

class NewFolder extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.apis = {
            submit: props.new_folder
        }
    }

    componentWillReceiveProps(nextProps) {
        this.apis.submit = nextProps.new_folder + "?path=" +nextProps.path
    }

    show(){
        var that = this;
        this.refs.FormDialog.show(function () {
            that.submit();
            return false;
        });
    }


    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.refreshFolder();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }


    render(){
        var formBody = this.renderForm(
            <section>
                <core.forms.TextField placeholder="新文件夹"
                    label="文件夹名称" name="folder_name" />
            </section>
        );
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="新建文件夹" size="mini" btnTitle="新建">
                    {formBody}
                </core.dialog.Dialog>
                <core.dialog.Alert ref="alertbox" msg_title="新建成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}

class UploadFile extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            path: props.path
        };
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            path: nextProps.path
        })
    }

    show(){
        var that = this;
        this.refs.FormDialog.show(function () {

        }, function () {
            that.manager.loadFiles();
        });
    }

    render(){
        return (
            <div className="ui">
                <core.dialog.Dialog ref="FormDialog" title="上传" size="tiny" btnShow={false}>
                    <core.forms.FileField ref="InUpload" upload_api={`${this.props.upload_file}?path=${this.state.path}`} auto/>
                    <i className="info circle icon"></i> 上传文件（文件存在则自动覆盖）<br />
                    <i className="info circle icon"></i> 根据服务器设置，单个文件大小限制：1000 MB
                </core.dialog.Dialog>
            </div>
        );
    }

}
