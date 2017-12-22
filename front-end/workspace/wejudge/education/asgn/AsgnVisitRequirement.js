var React = require("react");
var core = require("wejudge-core");

module.exports = AsgnVisitRequirement;


class AsgnVisitRequirement extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
        this.load = this.load.bind(this);
        this.addRequirement = this.addRequirement.bind(this);
        this.deleteRequirement = this.deleteRequirement.bind(this);
    }

    load(){
        this.refs.listView.getListData();
    }

    addRequirement(){
        var that = this;
        var student_id = that.refs["search_student"].getValue();
        var arrangement_id = that.refs["arrangement"].getValue();
        core.restful({
            url: that.props.apis.add_new,
            data:{
                user_id: student_id,
                arrangement_id: arrangement_id
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.load();
                });
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }

    deleteRequirement(entity){
        var that = this;
        return function () {
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.remove,
                        data:{
                            id: entity.id
                        },
                        method: "POST",
                        success: function (rel) {
                            that.refs.alertbox.showSuccess(rel, function () {
                                that.load();
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

    render() {
        var that = this;
        return (
            <div className="ui">
                <div className="ui compact menu">
                    <a className="item" onClick={this.load}><i className="refresh icon"></i> 刷新列表</a>
                    <div className="item">学生调课：</div>
                    <div className="item">
                        <core.forms.SearchField
                            ref={`search_student`}
                            icon="arrow right" transparent
                            search_api={that.props.apis.search_student}
                        />
                    </div>
                    <div className="item">
                        <core.forms.SelectField ref="arrangement" transparent>
                            {that.props.options.arrangements.map(function (val, key) {
                                return <option key={key} value={val.id}>{val.name || val.toString}</option>
                            })}
                        </core.forms.SelectField>
                    </div>
                    <a className="item" onClick={this.addRequirement}><i className="add icon"></i> 增加</a>
                </div>
                <AsgnVisitRequirementView
                    ref="listView"
                    apis={this.props.apis}
                    urls={this.props.urls}
                    remove_click={this.deleteRequirement}
                />
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm  ref="confirm"  msg_title="操作确认" msg="确定要删除这条记录吗？" />
            </div>
        )
    }
}

class AsgnVisitRequirementView extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.data
        }
    }

    renderListHeader(){
        return (
            <tr>
                <th>#ID</th>
                <th>姓名</th>
                <th>学号</th>
                <th>目标排课</th>
                <th>创建时间</th>
                <th>功能</th>
            </tr>
        );
    }
    renderListItems(){
        if(this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return <tr key={key}>
                    <td>{item.id}</td>
                    <td><a href="javascript:void(0)" onClick={core.show_account('education', item.author.id)}>{item.author.realname}</a></td>
                    <td>{item.author.username}</td>
                    <td>{core.tools.get_arrangement_desc(item.arrangement)}</td>
                    <td>{item.create_time}</td>
                    <td><a className="ui red tiny button" onClick={this.props.remove_click(item)}>删除</a></td>
                </tr>
            });
        else
            return null
    }

}