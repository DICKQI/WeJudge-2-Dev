/**
 * Created by lancelrq on 2017/7/10.
 */

var React = require("react");
var core = require("wejudge-core");
var CourseManager = require("./CourseManager");
var LoginView = require('../../account/account/module/LoginView');

module.exports = SchoolIndexPage;

class SchoolIndexPage extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {};
    }
    render(){
        return (
            this.props.options.is_logined ? <div className="ui stackable grid">
                <div className="four wide column">
                    <CourseAsgnList
                        course_asgn_list={this.props.apis.course_asgn_list}
                        asgn_view={this.props.urls.asgn_view}
                        course_view={this.props.urls.course_view}
                    />
                </div>
                <div className="twelve wide column">
                {this.props.options.is_teacher ?
                    <CourseManager apis={this.props.apis}  urls={this.props.urls} options={this.props.options}/> :
                    <div className="ui segment" style={{textAlign: "center"}}>
                        <h3>欢迎使用WeJudge教学系统</h3>更多精彩功能正在陆续开发中...
                        <p></p><p></p><p>&copy; WeJudge工作室</p>
                    </div>
                }
                </div>
            </div>
            :
            <div className="ui stacked segment"  style={{maxWidth: 480, margin: "0 auto"}}>
                <div style={{textAlign: "center"}}><h3>登录教学系统</h3></div>
                <div className="ui divider"></div>
                <LoginView afterSuccess="reload" app_name='education' hide_master />
            </div>
        );
    }
}


class CourseAsgnList extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.course_asgn_list
        }
    }

    componentDidMount() {
        this.getData();
    }

    renderBody() {
        return (
            <section>

                {
                    this.state.data.asgns_list && this.state.data.asgns_list.length > 0 ? <div className="ui red segment">
                            <div className="ui header">待处理作业</div>
                            <div className="ui relaxed divided list">
                                {this.state.data.asgns_list.map((val, key)=> {
                                    return (
                                        <div className="item" key={key} title={val.description}>
                                            <i className="puzzle big middle aligned icon"></i>
                                            <div className="content" style={{lineHeight: "1.5rem"}}>
                                                <a className="header"
                                                   href={this.props.asgn_view.replace("asgn/0", "asgn/" + val.id)}
                                                >{val.title}</a>
                                                <div className="description">{val.problems_count}题，满分：{val.full_score}</div>
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        </div>
                        : null
                }
                <div className="ui blue segment">
                    <div className="ui header">我的课程列表</div>
                    {this.state.data.courses_list && this.state.data.courses_list.length > 0 ?
                        <div className="ui relaxed divided list">
                            {this.state.data.courses_list.map((val, key)=> {
                                return (
                                    <div className="item" key={key}>
                                        <i className="book big middle aligned icon"></i>
                                        <div className="content" style={{lineHeight: "1.5rem"}}>
                                            <a className="header"
                                               href={this.props.course_view.replace("course/0", "course/" + val.id)}
                                            >{val.name} ({val.academy.name})</a>
                                            <div className="description" title={val.description}>
                                                任课教师：<a href="javascript:void(0)" onClick={core.show_account('education', val.author.id)}>{val.author.realname}</a>
                                            </div>
                                        </div>
                                    </div>
                                )
                            })}
                        </div>
                        :
                        <div className="content">
                            还没有课程安排哦！
                        </div>
                    }
                </div>

            </section>
        );
    }
}