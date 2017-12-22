/**
 * Created by lancelrq on 2017/3/2.
 */

module.exports = JudgeConfigManager;

var React = require('react');
var core = require('wejudge-core');
var FormManagerBase = require("./manager").FormManagerBase;


class JudgeConfigManager extends FormManagerBase  {
    
    constructor(props) {
        super(props);
        this.manager = props.manager;
        this.apis = {
            submit: props.save
        };
    }

    doSubmitSuccess(rel){
        var that = this;
        this.refs.alertbox.showSuccess(rel, function () {
            that.manager.getJudgeConfig();
        });
    }

    doSubmitFailed(rel, msg){
        this.refs.alertbox.showError(rel, msg);
    }


    render(){
        var that = this;
        var languageSelected = function() {
            var lang = that.state.judge_config.lang;

            return that.manager.LangList.map((value, key) => {
                var checked = (!lang || lang == 0 || ((value[0] & lang) > 0));
                return (<core.forms.CheckBoxField name="lang" type="toggle" key={key} label={value[1]} value={value[0]} checked={checked} />);
            })
        };
        var formBody = this.renderForm((
            <div className="ui">
                <div className="ui horizontal divider">可用评测语言（仅题目集内有效）</div>
                <div className="inline fields">
                    {languageSelected()}
                </div>
                <div className="ui horizontal divider">题目访问权限（对出题者本人不限制权限）</div>
                <core.forms.CheckBoxField
                    label="题目访问（内容、评测统计等）" name="permission" type="toggle"
                    value="1" checked={(this.state.judge_config.permission & 1) > 0} />
                <core.forms.CheckBoxField
                    label="提交评测" name="permission" type="toggle"
                    value="2" checked={(this.state.judge_config.permission & 2) > 0}
                />
                <core.forms.CheckBoxField
                    label="数据访问（访问题目设置、测试数据、示例代码、评测历史详情等）" name="permission" type="toggle"
                    value="4" checked={(this.state.judge_config.permission & 4) > 0}
                />
                <core.forms.CheckBoxField
                    label="管理访问（修改题目设置、测试数据、示例代码等）" name="permission" type="toggle"
                    value="8" checked={(this.state.judge_config.permission & 8) > 0}
                />
                <div className="ui horizontal divider">特殊评测（切换后请先保存才能开启详细设置）</div>
                <div className="ui fields">
                    <core.forms.RadioField
                        label="正常评测" name="special_judge" type="toggle"
                        value="0" checked={this.state.judge_config.special_judge==0} />
                    <core.forms.RadioField
                        label="结果检查模式" name="special_judge" type="toggle"
                        value="1" checked={this.state.judge_config.special_judge==1}
                    />
                    <core.forms.RadioField
                        label="交互评测模式" name="special_judge" type="toggle"
                        value="2" checked={this.state.judge_config.special_judge==2}
                    />
                </div>
                {this.state.judge_config.special_judge == 1 || this.state.judge_config.special_judge == 2 ?
                    <div className="ui segment">
                        <core.forms.FileField ref="SPJCodeUpload" upload_api={this.props.spj_judger} auto/>
                        <div className="ui relaxed divided list">
                            <div className="item">
                                <i className="large code middle aligned icon"></i>
                                <div className="content">
                                    <a className="header">源代码</a>
                                    <div className="description">点击下载</div>
                                </div>
                            </div>
                            <div className="item">
                                <i className="large database middle aligned icon"></i>
                                <div className="content">
                                    <span className="header">特殊评测程序</span>
                                    <div className="description">
                                        {this.state.judge_config.special_judger_program && this.state.judge_config.special_judger_program != "" ? "就绪" :"未编译"}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <i className="info circle icon"></i> 只支持使用C、C++编写的程序，并且用G++进行编译。判题程序返回值参见<a>说明</a>
                    </div> : ""}
                <br />
                <button className="ui primary button">
                    <i className="save icon"></i>
                    保存设置
                </button>
            </div>
        ));
        return (
            <div className="ui">
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="" />
            </div>
        )
    }

}