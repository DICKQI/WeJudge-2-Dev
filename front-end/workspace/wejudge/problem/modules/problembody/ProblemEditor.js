/**
 * Created by lancelrq on 2017/2/15.
 */

module.exports = ProblemEditor;

var React = require('react');
var core = require('wejudge-core');


class ProblemEditor extends core.forms.FormComponent {


    constructor(props) {
        super(props);
        this.state = {
            editmode: false,
            entity : {
                problem_type: 0
            }
        };
    }

    createProblem(){
        this.setState({
            editmode: false
        });
        this.apis = {
            submit: this.props.apis.create
        };
        this.views = {
            view_problem_manager: this.props.urls.view_problem_manager
        };
    }

    modifyProblem(){
        var that = this;
        this.setState({
            editmode: true
        });
        this.apis = {
            submit: this.props.apis.modify,
            data: this.props.apis.problem_info
        };
        this.getData(function (rel) {
            that.setState({
                entity: rel.data.body
            });
        });
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            if(!that.state.editmode) // 新建题目
                window.location.href = that.views.view_problem_manager.replace("/problem/0", "/problem/" + rel.data);
            else
                window.location.reload();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.alertbox.showError(rel, msg);
    }
    

    render(){
        var that = this;
        var formBody = this.renderForm(
            <section>
                <div className="ui stackable grid">
                    <div className="eight wide column">
                        <core.forms.TextField label="题目名称" name="title" placeholder="请输入题目名称" maxLength="50" required value={this.state.entity.title || ""} />
                    </div>
                    <div className="four wide column">
                        <core.forms.SelectField name="problem_type" label="题目类型(选定后不可修改)" required forceDefault disabled={this.state.editmode} value={this.state.entity.problem_type}>
                            <option value={0}>普通题目</option>
                            <option value={1}>代码填空</option>
                        </core.forms.SelectField>
                    </div>
                    <div className="four wide column">
                        <core.forms.SelectField name="difficulty" label="题目难度" required value={this.state.entity.difficulty}>
                            <option value={1}>入门</option>
                            <option value={2}>简单</option>
                            <option value={3}>一般</option>
                            <option value={4}>较难</option>
                            <option value={5}>困难</option>
                        </core.forms.SelectField>
                    </div>
                </div>
                <br />
                <core.forms.CKEditorField height="30em" label="题目正文" name="description" required value={this.state.entity.description} />
                <core.forms.CKEditorField label="输入要求" name="input" value={this.state.entity.input} />
                <core.forms.CKEditorField label="输出要求" name="output" value={this.state.entity.output} />
                <core.forms.CKEditorField label="样例输入" name="sample_input" value={this.state.entity.sample_input} />
                <core.forms.CKEditorField label="样例输出" name="sample_output" value={this.state.entity.sample_output} />
                <core.forms.CKEditorField label="小提示" name="hint" value={this.state.entity.hint} />
                <core.forms.TextAreaField label="题目来源" name="source"  value={this.state.entity.source} />

                <button className="ui primary button"><i className="save icon"></i>确定</button>
            </section>
        );
        return(
            <div className="ui">
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="点击确定刷新页面" />
            </div>
        )
    }

}