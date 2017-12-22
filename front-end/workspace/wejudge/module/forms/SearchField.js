/**
 * Created by lancelrq on 2017/7/7.
 */

module.exports = SearchField;

var React = require('react');
var Field = require('./Field');

class SearchField extends Field {

    constructor(props) {
        super(props);
    }

    componentDidMount(){
        var that = this;
        $(this.refs.SearchArea).search({
            apiSettings: {
                url: this.props.search_api +'?kw={query}'
            },
            fields: {
                results : 'results',
                title   : 'title',
                description: "description",
                url     : 'url'
            },
            minCharacters : that.props.minCharacters || 1,
            onSelect: function (result) {
                that.setState({
                    value: result.title
                });
                if(typeof that.props.onchange == 'function') {
                    that.props.onchange({
                        title: result.title,
                        result: result
                    });
                }
            }
        })
    }

    clearValue(){
        this.setState({
            value: ""
        });
        $(this.refs.SearchArea).search("set value", "");
    }
    
    render(){
        return (
            <div className="ui search" ref="SearchArea">
                <div className={`ui ${this.props.transparent && "transparent"} icon input`}>
                    <input className="prompt"
                           type="text"
                           value={this.state.value}
                           name={this.props.name}
                           placeholder={this.props.placeholder}
                           onChange={this.handlerChange}
                    />
                    <i className={`${this.props.icon || 'search'} icon`}></i>
                </div>
                <div className="results"></div>
            </div>
        )
    }

}
