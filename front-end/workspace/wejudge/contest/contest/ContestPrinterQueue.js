/**
 * Created by lancelrq on 2017/4/7.
 */


var React = require("react");
var core = require("wejudge-core");

module.exports = ContestPrinterView;

class ContestPrinterView extends React.Component{
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
    }
    load(){
        this.refs.listView.getListData();
    }
    render(){
        if(this.props.is_admin){
            return (
                <ContestPrinterQueue
                    ref="listView"
                    printer_queue={this.props.apis.printer_queue}
                    view_printer_page={this.props.urls.printer_page}
                />
            )
        }else{
            return <ContestPrinterSender send_printer={this.props.apis.send_printer} />
        }
    }
}

class ContestPrinterSender extends core.forms.FormComponent{
    constructor(props) {
        super(props);
        this.apis={
            submit: props.send_printer
        };
    }

    doSubmitSuccess(rel){
        this.refs.alertbox.showSuccess(rel, function () { });
    }

    doSubmitFailed(rel, msg){
        this.refs.FormMessager.show("错误提示", msg, "error");
    }

    render(){
        var formBody = this.renderForm(
            <div className="ui">
                <div className="ui message">
                    <div className="header">打印提示</div>
                    <br />
                    <div className="content">
                        <ol className="ui list">
                            <li>请先选择您需要的打印方式，然后填写该方式对应的字段，不能混合使用。提交后，工作人员将会给您送上打印的资料。</li>
                            <li>根据比赛规则，您只能打印自己提交的代码。输入您自己的评测记录ID，即可以打印该记录中您提交的代码。</li>
                            <li>请适当使用本服务。保护环境，节约用纸</li>
                        </ol>
                    </div>
                </div>
                <div className="ui inline fields">
                    <label>打印方式</label>
                    <core.forms.RadioField name="action" value="0" label="评测状态ID" checked/>
                    <core.forms.RadioField name="action" value="1" label="手动输入内容" />
                </div>
                <core.forms.TextField label="评测状态ID" name="status" ref="by_status" />
                <core.forms.TextAreaField label="手动输入打印内容" name="content" value="" ref="by_content"  rows="15" />
                <button className="ui green button">提交打印</button>
            </div>
        );
        return (
            <div className="ui">
                {formBody}
                <core.dialog.Alert ref="alertbox" msg_title="处理成功" msg="您的打印需求已经提交，请耐心等待工作人员为您处理" />
            </div>

        );
    }
}

class ContestPrinterQueue extends core.ListView {

    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.printer_queue
        }
    }
    componentDidMount() {
        var that = this;
        super.componentDidMount();
        if(!this.refresh_timer){
            console.log("Watch Printer Queue: Start");
            this.refresh_timer = setInterval(function () {
                console.log("Watch Printer Queue: Tick");
                that.getListData();
            }, 20 * 1000);   // refresh after 20 s
        }
    }

    renderListHeader() {
        return (
            <tr>
                <th>#ID</th>
                <th>标题</th>
                <th>提交者</th>
                <th>提交时间</th>
                <th>操作</th>
            </tr>
        );
    }

    renderListItems() {
        if (this.state.listdata && this.state.listdata.length > 0)
            return this.state.listdata.map((item, key) => {
                return (
                    <tr key={key}>
                        <td>{item.id}</td>
                        <td>{item.title}</td>
                        <td>{item.author.nickname}({item.author.username})</td>
                        <td>{core.tools.format_datetime(item.create_time)}</td>
                        <td>
                            <a  className={`ui ${item.is_finish ? "green" : "red"} button`}
                                href={this.props.view_printer_page.replace("/page/0", "/page/" + item.id)}
                                target="_blank"
                            >
                                {item.is_finish ? "已打印" : "未打印" }
                            </a>
                        </td>
                    </tr>
                )
            });
        else
            return null
    }
}