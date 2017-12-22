/**
 * Created by lancelrq on 2017/2/12.
 */

module.exports = ListView;


var React = require('react');
var core = require("wejudge-core");


class ListView extends React.Component{

    constructor(props){
        super(props);
        this.state = {
            listdata: [],
            pagination: {},
            inited: false,
            rawdata: null,
            show_pagination: props.show_pager || true
        };
        this.table_style = props.table_style || 'striped';
        this.api_url = "";
        this.params = {
            page: 1,
            limit: 50,
            display: 11
        };
        this.getListData = this.getListData.bind(this);
        this.onPageBtnClick = this.onPageBtnClick.bind(this);
        this.onErrorReLoad = this.onErrorReLoad.bind(this);
    }

    componentDidMount() {
        //this.getListData();
    }

    setParams(nextParams){
        this.params = $.extend(this.params, nextParams);
    }

    onPageBtnClick(page) {
        this.params.page = page;
        this.getListData();
    }

    onErrorReLoad(){
        this.getListData();
    }

    load(){
        this.getListData();
    }

    getListData() {
        var that = this;
        this.refs.loader.show();
        var core = require("wejudge-core");
        core.restful({
            method: 'GET',
            data: this.params,
            responseType: "json",
            url: that.apis.data,
            success: function (rel) {
                var data = rel.data;
                if(!data.pagination){
                    that.setState({
                        inited: true,
                        listdata: data.data,
                        rawdata: data,
                        show_pagination: false
                    })
                }else{
                    that.setState({
                        inited: true,
                        listdata: data.data,
                        rawdata: data,
                        pagination: data.pagination
                    });
                }
                that.refs.loader.hide();
                that.refs.listmessager.hide();
                if(typeof that.onListLoaded === 'function'){
                    //(listdata, rawdata);
                    that.onListLoaded(data.data, data);
                }
            },
            error: function (rel, msg) {
                that.refs.loader.hide();
                that.refs.listmessager.show("列表加载失败", msg, 'error');
            }
        }).call();
    }

    render(){
        var core = require("wejudge-core");
        var listheader = this.renderListHeader();
        var listbody = this.renderListItems();
        var footerbody = this.renderFooterBody && this.renderFooterBody() || null;
        var headerBody = this.renderHeaderBody && this.renderHeaderBody() || null;
        var colSpan = 0;
        if(listheader && listheader.props && listheader.props.children && listheader.props.children.length > 0){
            for(var i = 0 ; i < listheader.props.children.length; i++){
                if(listheader.props.children[i] instanceof Array){
                    colSpan += listheader.props.children[i].length;
                }else{
                    colSpan += 1;
                }
            }
        }
        return (
            <div className="ui" style={{minHeight: 200, height: "auto"}} ref="listview">
                <core.dimmer.Loader inverted ref="loader"/>
                <core.dimmer.Messager inverted title="列表加载失败" ref="listmessager" retry={this.onErrorReLoad} />
                {headerBody}
                <table className={`ui ${this.props.stackable ? "stackable" : "unstackable"} ${this.table_style} table`}>
                    <thead>
                    {listheader}
                    </thead>
                    <tbody>
                    {listbody ? listbody :
                        <tr>
                            <td colSpan={colSpan} style={{padding: 0}}>
                                <div className="ui icon message" style={{margin: 0, boxShadow: "none"}}>
                                    <i className="info circle icon"></i>
                                    <div className="content">
                                        <p>当前列表是空的呢！_(:зゝ∠)_</p>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    }
                    </tbody>
                    {
                        listbody && this.state.show_pagination ?
                        <tfoot>
                            <tr>
                                <th colSpan="100">
                                    <core.Pagination pagination={this.state.pagination} onclick={this.onPageBtnClick}/>
                                </th>
                            </tr>
                        </tfoot> : null
                    }
                </table>
                {footerbody}
            </div>
        );
    }

}

//
// {listbody ? (
//     <div className="ui">
//         <table className={`ui ${this.props.stackable ? "stackable" : "unstackable"} ${this.table_style} table`}>
//             <thead>
//             {listheader}
//             </thead>
//             <tbody>
//             {listbody}
//             </tbody>
//             {
//                 this.state.show_pagination ?
//                     <tfoot>
//                     <tr>
//                         <th colSpan="100">
//                             <core.Pagination pagination={this.state.pagination} onclick={this.onPageBtnClick}/>
//                         </th>
//                     </tr>
//                     </tfoot> : null
//             }
//         </table>
//     </div>
// ) : (this.state.inited) ? (
//     <div className="ui icon message" style={{margin: "10px 0"}}>
//         <i className="info circle icon"></i>
//         <div className="content">
//             <p>当前列表是空的呢！_(:зゝ∠)_</p>
//         </div>
//     </div>
// ) : null}