/**
 * Created by lancelrq on 2017/3/5.
 */


module.exports = {
    ManagerBase: ManagerBase,
    FormManagerBase: FormManagerBase
};

var React = require('react');
var core = require('wejudge-core');


class ManagerBase extends React.Component {

    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            lang: props.lang,
            lang_call: props.manager.LangCall[props.lang],
            judge_config: props.judge_config
        };
    }
    componentWillReceiveProps(nextProps) {
        this.setState({
            lang: nextProps.lang,
            lang_call: nextProps.manager.LangCall[nextProps.lang],
            judge_config: nextProps.judge_config
        });
    }
}

class FormManagerBase extends core.forms.FormComponent {
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            lang: props.lang,
            lang_call: props.manager.LangCall[props.lang],
            judge_config: props.judge_config
        };
    }
    componentWillReceiveProps(nextProps) {
        this.setState({
            lang: nextProps.lang,
            lang_call: nextProps.manager.LangCall[nextProps.lang],
            judge_config: nextProps.judge_config
        });
    }
}