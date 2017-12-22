/**
 * Created by lancelrq on 2017/2/17.
 */

module.exports = RatingField;

var React = require('react');

class RatingField extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            rating: props.rating || 0
        };
    }

    componentDidMount() {
        var that = this;
        $(this.refs.rating).rating({
            onRate: function (value) {
                that.setState({
                    rating: value
                })
            }
        });
        if(this.props.disabled)
            $(this.refs.rating).rating('disable')
    }

    componentWillReceiveProps(nextProps) {
        var value = nextProps.rating;
        var that = this;
        $(this.refs.rating).rating('set rating', value);
        if(nextProps.disabled)
            $(this.refs.rating).rating('disable')
    }

    getValue(){
        return this.state.value;
    }

    rating(opt){
        $(this.refs.rating).rating(opt)
    }

    render(){
        return (
            <div
                 className={`ui ${this.props.size || ""} ${this.props.type || ""} rating`}
                 data-rating={this.state.rating || 0}
                 data-max-rating={this.props.max || 5}
                 data-min-rating={this.props.min || 1}
                 ref="rating"
            ></div>
        )
    }

}