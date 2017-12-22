/**
 * Created by lancelrq on 2017/1/21.
 */

var React = require('react');
var extend = require('extend');
var dialog = require('../module/dialog');

module.exports = Pagination;

class Pagination extends React.Component{
    constructor(props){
        super(props);
        var pagination_default = {
            pages: [],
            now_page: 1,
            page_total: 1
        };
        var pages = props.pagination;
        if(pages != undefined){
            pages = extend(pagination_default, pages);
        }else{
            pages = pagination_default;
        }
        this.state = {
            pagination: pages
        };
        this.onBtnClick = this.onBtnClick.bind(this);
    }
    componentWillReceiveProps(nextProps) {
        this.setState({pagination: nextProps.pagination});
    }
    onBtnClick(val){
        var that = this;
        return function() {
            if (typeof that.props.onclick == 'function') {
                typeof that.props.onclick(val);
            }
        }
    }
    render(){
        var navbtn_list = this.state.pagination.pages.map((val, key)=>{
            var actived = (val == this.state.pagination.now_page) ? "active item" : "item";
            return (
                <a key={key} className={actived} onClick={this.onBtnClick(val)}>
                    {val}
                </a>
            )
        });
        return (
            <div className="ui pagination menu">
                <a className="item" onClick={this.onBtnClick(1)}>
                    <i className="chevron left icon"></i>
                </a>
                {navbtn_list}
                <a className="item" onClick={this.onBtnClick(this.state.pagination.page_total)}>
                    <i className="chevron right icon"></i>
                </a>
            </div>
        )
    }
}