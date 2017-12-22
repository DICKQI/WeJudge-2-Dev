
var React = require("react");
var core = require("wejudge-core");


module.exports = SchoolSettings;

class SchoolSettings extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.school_info
        };
        this.addYearTeam = this.addYearTeam.bind(this);
        this.deleteYearTerm = this.deleteYearTerm.bind(this);
    }

    addYearTeam(){
        var that = this;
        var year = that.refs.yt_year.getValue();
        var term = that.refs.yt_term.getValue();
        core.restful({
            url: that.props.apis.change_yearterm,
            data:{
                id: 0,
                term: term,
                year: year
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.refs.yt_year.setValue('');
                    that.refs.yt_term.setValue('');
                    that.load();
                });
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }


    deleteYearTerm(entity){
        var that = this;
        return function () {
            that.refs.confirm.show(function (rel) {
                if (rel) {
                    core.restful({
                        url: that.props.apis.change_yearterm,
                        data:{
                            id: entity.id,
                            remove: true
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

    renderBody() {
        var school  = this.state.data ? this.state.data.school : null;
        var term  = this.state.data ? this.state.data.terms : null;
        var that = this;
        return (
            <div className="ui grid">
                <div className="row">
                    <div className="sisteen wide column">
                        <div className="ui black segment">
                            <h3>学校设置</h3>
                            <div className="divider"></div>
                            <SchoolSetting
                                manager={this}
                                entity={this.state.data}
                            />
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="eight wide column">
                        <div className="ui top attached stackable menu">
                            <div className="header item">学年学期管理</div>
                            <div className="item"><core.forms.TextField ui input transparent ref="yt_year" placeholder="年(2017为2017-2018)" /></div>
                            <div className="item"><core.forms.TextField ui input transparent ref="yt_term" placeholder="学期"/></div>
                            <a className="item" onClick={this.addYearTeam}><i className="add icon" /> 增加</a>
                        </div>
                        <div className="ui  bottom attached  segment">
                            <table className="ui table">
                                <thead>
                                <tr>
                                    <th>学年</th>
                                    <th>学期</th>
                                    <th>操作</th>
                                </tr>
                                </thead>
                                <tbody>
                                {term && term.map(function (val, key) {
                                    return <tr key={key}>
                                        <td>{val.year} - {val.year+1}年度</td>
                                        <td>第{val.term}学期</td>
                                        <td><a className="ui red button" onClick={that.deleteYearTerm(val)}><i className="remove icon" />删除</a></td>
                                    </tr>
                                })}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div className="eight wide column">
                    <SectionsSetting
                        manager={this}
                        save_api={this.props.apis.save_sections}
                        sections={school ? school.sections : null}
                    />
                    </div>
                </div>
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                <core.dialog.Confirm  ref="confirm"  msg_title="操作确认" msg="你确定要删除这个学期信息吗？操作将会删除课程和作业信息！！" />
            </div>
        );
    }
}

class SectionsSetting extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        var sections = this.loadSections(props);
        this.state = {
            sections: sections
        };
        this.changeValue = this.changeValue.bind(this);
        this.save = this.save.bind(this);
        this.addSection = this.addSection.bind(this);
        this.removeSection = this.removeSection.bind(this);

    }

    componentWillReceiveProps(nextProps) {
        var sections = this.loadSections(nextProps);
        this.setState({
            sections: sections
        })
    }

    loadSections(props){
        var sections_data = eval("(" + props.sections + ")");
        var max_section = sections_data.max_section;
        var sections_list = [];
        for(var i in sections_data.sections){
            sections_list.push(sections_data.sections[i]);
        }
        return sections_list;
    }

    dumpSections(){
        var sections_list = this.state.sections;
        var sections = {};
        for(var i=0; i < sections_list.length; i++){
            sections[i+1] = sections_list[i];
        }
        return {
            sections: sections,
            max_section: sections_list.length
        };
    }

    convertToNum(val){
        var t = val.split(':');
        if(t.length != 3) return 0;
        var sec = parseInt(t[2]);
        var min = parseInt(t[1]);
        var hur = parseInt(t[0]);
        if(isNaN(sec) || isNaN(min) || isNaN(hur)){return 0}
        return sec + min * 60 + hur * 3600;
    }
    convertToDate(val){
        function PrefixInteger(num) {
            return (Array(2).join(0) + num).slice(-2);
        }
        var hur = parseInt(val / 3600);
        var min = parseInt(val / 60 % 60);
        var sec = parseInt(val % 60);
        if(isNaN(sec) || isNaN(min) || isNaN(hur)){return "00:00:00"}
        return PrefixInteger(hur) + ":" + PrefixInteger(min) + ":" + PrefixInteger(sec);
    }
    changeValue(key, item){
        var that = this;
        return function (e) {
            var sections_list = that.state.sections;
            var val = e.target.value;
            sections_list[key][item] = that.convertToNum(val);
            that.setState({
                sections: sections_list
            })
        }
    }

    addSection(){
        var sections_list = this.state.sections;
        sections_list.push({
            start_time: 0,
            end_time: 0
        });
        this.setState({
            sections: sections_list
        })
    }
    removeSection(){
        var sections_list = this.state.sections;
        sections_list.pop();
        this.setState({
            sections: sections_list
        })
    }
    save(){
        var that = this;
        var postdata = this.dumpSections();
        core.restful({
            url: that.props.save_api,
            data:{
                datas: JSON.stringify(postdata)
            },
            method: "POST",
            success: function (rel) {
                that.refs.alertbox.showSuccess(rel, function () {
                    that.props.manager.load();
                });
            },
            error: function (rel, msg) {
                that.refs.alertbox.showError(rel, msg);
            }
        }).call()
    }


    render(){
        var that = this;
        return <div>
                <div className="ui top attached stackable menu">
                    <div className="header item">作息时间管理</div>
                    <div className="item">总计<strong>{this.state.sections.length}</strong>节</div>
                    <a className="item" onClick={this.addSection}><i className="add icon" /> 增加一节</a>
                    <a className="item" onClick={this.removeSection}><i className="remove icon" /> 减少一节</a>
                    <div className="right menu">
                        <a className="item" onClick={this.save}><i className="save icon" /> 保存</a>
                    </div>
                </div>
                <div className="ui bottom attached  segment">
                    {this.state.sections ? <table className="ui table">
                        <thead>
                        <tr>
                            <th>节数</th>
                            <th>上课时间</th>
                            <th>下课时间</th>
                        </tr>
                        </thead>
                        <tbody>
                        {this.state.sections.map(function (val, key) {
                            return <tr key={key}>
                                <td>{key + 1}</td>
                                <td>
                                    <core.forms.TimeField ui input
                                                          value={that.convertToDate(val.start_time)}
                                                          onblur={that.changeValue(key, 'start_time')}
                                    />
                                </td>
                                <td>
                                    <core.forms.TimeField ui input
                                                          value={that.convertToDate(val.end_time)}
                                                          onblur={that.changeValue(key, 'end_time')}
                                    />
                                </td>
                            </tr>
                        })}
                        </tbody>
                    </table>
                    : null}
                    <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
                    </div>
            </div>
    }
}


class SchoolSetting extends core.forms.FormComponent{

    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.state = {
            entity: props.entity
        };
        this.apis={
            submit: this.manager.props.apis.save_settings
        }
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.load()
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            entity: nextProps.entity
        })
    }

    render(){
        var school  = this.state.entity.school;
        var terms  = this.state.entity.terms;
        var formBody = this.renderForm(
            this.state.entity ?
                <div className="ui grid">
                   <div className="twelve wide column">
                       <div className="two fields">
                           <core.forms.TextField
                               label="学校名称" name="name" placeholder="请输入学校名称"
                               required value={school.name}/>
                           <core.forms.TextField
                               label="学校英文缩写" name="short_name" placeholder="请输入学校英文缩写"
                               required value={school.short_name}/>
                       </div>
                       <core.forms.TextAreaField
                           label="学校简介" name="description" placeholder="请输入学校简介"
                           value={school.description}/>
                       <div className="two fields">
                           <core.forms.SelectField label="学年学期" name="yearterm" forceDefault value={school.now_term}>
                               {terms.map((val, key) => {
                                   return (
                                       <option key={key} value={val.id}>{`${val.year}-${val.year+1}年度第${val.term}学期`}</option>
                                   );
                               })}
                           </core.forms.SelectField>
                           <core.forms.TextField
                               label="学期最大周数" name="max_week" placeholder="比如最长的学期有25个教学周，请设置25"
                               value={school.max_week}/>
                       </div>
                       <button className="ui green button"><i className="save icon"></i>保存设置</button>
                   </div>
                    <div className="four wide column">
                        <h4>学校Logo</h4>
                        <div className="ui divider"></div>
                        <img className="ui image" src={school.logo} />
                        (上传功能开发中...)
                    </div>
                </div> : null
        );
        return (
            <div className="ui">
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>

        );
    }

}
