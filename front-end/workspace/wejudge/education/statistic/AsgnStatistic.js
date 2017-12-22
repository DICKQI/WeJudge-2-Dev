/**
 * Created by lancelrq on 2017/10/6.
 */

var React = require('react');
var moment = require("moment");
var core = require("wejudge-core");

class AsgnStatistic extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            // 原始信息：
            asgn: {},
            reports: [],
            solutions: [],
            judge_status: [],
            // 索引信息
            students: {},
            problems: {},
            graphics: null,
            // 配置信息
            options: {
                timeline_type: "12hr"
            }
        };
    }

    load(){
        this.refs.loader.setTitle("正在载入数据...");
        this.refs.loader.show();
        core.restful({
            method: 'GET',
            responseType: "json",
            url: this.props.apis.data,
            //url: "/static/datas.json",
            success: (rel) => {
                this.setState({
                    "asgn": rel.data.asgn,
                    "reports": rel.data.reports,
                    "solutions": rel.data.solutions,
                    "judge_status": rel.data.judge_status
                }, () => {
                    this.setState(this.createIndex(), ()=>{
                        this.createGraphics();
                    });
                    // setTimeout(this.createGraphics2.bind(this), 3000);
                });
            },
            error: (rel, msg) => {
                this.refs.loader.hide();
            }
        }).call();
    }

    createIndex(){
        this.refs.loader.setTitle("正在创建索引...");
        var problems_index = {};
        for(var i = 0; i < this.state.asgn.problems.length; i++){
            var problem = this.state.asgn.problems[i];
            var pid = problem.id;
            problems_index[pid] = problem;
        }
        var students_index = {};
        for(var j = 0; j < this.state.reports.length; j++){
            var report = this.state.reports[j];
            var student = report.author;
            var sid = student.id;
            student['report'] = report;
            students_index[sid] = student;
        }
        return {
            problems: problems_index,
            students: students_index
        };
    }

    createGraphics(){
        this.refs.loader.setTitle("正在生成图表数据...");
        var Analyzer = new StatisticAnalyzer(this.state);
        var graphics = {
            reports:{
                jscore: Analyzer.calcReportScore('judge_score'),
                tscore: Analyzer.calcReportScore('finally_score')
            },
            judge_status: Analyzer.calcJudgeStatusTimeLine(),
            solutions: Analyzer.calcSolutions()
        };
        this.setState({
            graphics: graphics
        })
    }

    componentDidUpdate(pP, pS) {

        if(!this.state.graphics) return true;
        if(this.state.graphics === pS.graphics) return true;
        var SCORE_AREA_COLOR = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db', '#1abc9c', '#9b59b6'];
        var JUDGE_FLAG_COLOR = ['#2ecc71', "#ffff00",'#f1c40f', '#e67e22', '#e74c3c', '#9b59b6', '#34495e', '#3498db', '#cccccc'];
        var TimeLineType = this.state.options.timeline_type;
        this.refs.loader.hide();
        var graphics = this.state.graphics;
        // 判题机给分情况
        var reports = graphics.reports;
        echarts.init(this.refs.report_jscore_chart).setOption({
            color: SCORE_AREA_COLOR,
            tooltip : {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: reports.jscore.legend_data
            },
            series : [
                {
                    type: 'pie',
                    radius : '90%',
                    center: ['50%', '50%'],
                    data: reports.jscore.series_data,
                    labelLine: { normal: { show: false } },
                    label: { normal: { show: false } },
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        });
        // 最终得分情况
        echarts.init(this.refs.report_tscore_chart).setOption({
            color: SCORE_AREA_COLOR,
            tooltip : {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: reports.tscore.legend_data
            },
            series : [
                {
                    type: 'pie',
                    radius : '90%',
                    center: ['50%', '50%'],
                    data: reports.tscore.series_data,
                    labelLine: { normal: { show: false } },
                    label: { normal: { show: false } },
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        });
        // 总体评测状态
        var judge_status = graphics.judge_status;
        var solutions = graphics.solutions;
        echarts.init(this.refs.judge_status_total).setOption({
            color: JUDGE_FLAG_COLOR,
            tooltip : {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: judge_status.legend_data
            },
            series : [
                {
                    type: 'pie',
                    radius : '60%',
                    center: ['65%', '40%'],
                    labelLine: { normal: { show: false } },
                    label: { normal: { show: false } },
                    data: judge_status.total.series_data,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        });
        // 时间线
        var ZoomEnd = 100;
        switch (TimeLineType){
            case "12hr": ZoomEnd = 80; break;
            case "1d": ZoomEnd = 60; break;
            case "3d": ZoomEnd = 40; break;
            case "all": ZoomEnd = 20; break;
        }
        echarts.init(this.refs.judge_status_time_line).setOption({
            color: JUDGE_FLAG_COLOR,
            legend: {
                data: judge_status.legend_data
            },
            tooltip : {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#6a7985'
                    }
                }
            },
            dataZoom: [
                {
                    show: true,
                    realtime: true,
                    start: 0,
                    end: ZoomEnd
                }
            ],
            xAxis : [{
                type: 'time',
                splitLine: {
                    show: true
                },
                boundaryGap: [0, '100%'],
            }],
            yAxis : [{
                type: "value",
            }],
            series: judge_status.timeline.series_data,
        });
        // 题目
        for(var i = 0; i < this.state.asgn.problems.length; i++){
            var problem = this.state.asgn.problems[i];
            echarts.init(this.refs["problem_"+problem.id+"_judge_status"]).setOption({
                color: ['#cccccc'],
                tooltip : {
                    trigger: 'item',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis : [
                    {
                        type : 'category',
                        data : judge_status.legend_data_en,
                        axisTick: {
                            alignWithLabel: true
                        }
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'数值',
                        type:'bar',
                        barWidth: '60%',
                        data: judge_status.problems[problem.id]
                    },{
                        type: 'pie',
                        radius: [0, '30%'],
                        center: ['80%', '25%'],
                        data: solutions.problems[problem.id],
                        selectedMode:true,
                    }
                ]
            });
            echarts.init(this.refs["problem_"+problem.id+"_timeused"]).setOption({
                xAxis: {
                    type: 'value',
                    axisLabel: {
                        formatter: (p) => {
                            return core.tools.rank_list_time(p)
                        }
                    }
                },
                yAxis: {
                    type: 'value',
                },
                dataZoom:[{
                    show: true,
                    realtime: true,
                    labelFormatter: (p) => {
                        return core.tools.rank_list_time(p)
                    }
                }],
                tooltip: {
                    formatter: (p) =>{
                        return `用时：${core.tools.rank_list_time(p.data[0])}<br />正确率：${p.data[1]}%`
                    }
                },
                series: [
                    {
                        name: 'I',
                        type: 'scatter',
                        data: solutions.timeused[problem.id],
                    }
                ]
            })
        }

    }

    onErrorReLoad(){
        this.load();
    }

    changeTimeLineSize(typename){
        return ()=>{
            this.setState({
                options: {
                    timeline_type: typename
                }
            },()=>{
                this.createGraphics();
            })
        }
    }

    render(){
        return <div className="ui" style={{minHeight: 200}}>
            <core.dimmer.Loader inverted ref="loader" />
            <div className="ui">
                <div className="ui horizontal divider">
                    <h2>作业情况统计</h2>
                </div>
                <div className="ui stackable two columns grid">
                    <div className="column" style={{textAlign:"center"}}>
                        <h3>判题机给分情况</h3>
                        <div ref="report_jscore_chart" style={{width: "100%", height: 240}}></div>
                    </div>
                    <div className="column" style={{textAlign:"center"}}>
                        <h3>最终得分情况</h3>
                        <div ref="report_tscore_chart" style={{width: "100%", height: 240}}></div>
                    </div>
                </div>
                <div className="ui horizontal divider">
                    <h2>评测数据分析</h2>
                </div>
                <div style={{textAlign:"right"}}>
                    <div className="ui mini buttons">
                        <button
                            onClick={this.changeTimeLineSize('3hr')}
                            className={`ui button ${this.state.options.timeline_type==="3hr" ? "active":""}`}>
                            3小时
                        </button>
                        <button
                            onClick={this.changeTimeLineSize('12hr')}
                            className={`ui button ${this.state.options.timeline_type==="12hr" ? "active":""}`}>
                            12小时
                        </button>
                        <button
                            onClick={this.changeTimeLineSize('1d')}
                            className={`ui button ${this.state.options.timeline_type==="1d" ? "active":""}`}>
                            1天
                        </button>
                        <button
                            onClick={this.changeTimeLineSize('3d')}
                            className={`ui button ${this.state.options.timeline_type==="3d" ? "active":""}`}>
                            3天
                        </button>
                        <button
                            onClick={this.changeTimeLineSize('all')}
                            className={`ui button ${this.state.options.timeline_type==="all" ? "active":""}`}>
                            全部
                        </button>
                    </div>
                </div>
                <div className="ui hidden divider"></div>
                <div className="ui stackable grid">
                    <div className="four wide column" style={{textAlign:"center"}}>
                        <h3>评测状态分布</h3>
                        <div ref="judge_status_total" style={{width: "100%", height: 360}}></div>
                    </div>
                    <div className=" twelve wide column" style={{textAlign:"center"}}>
                        <h3>时间线(10分钟为单位)</h3>
                        <div ref="judge_status_time_line" style={{width: "100%", height: 360}}></div>
                    </div>
                </div>
                {this.state.asgn.problems && this.state.asgn.problems.map((problem, key)=>{
                   return <div key={"problem_group_" + key}>
                       <div className="ui horizontal divider">
                           <h3>题目{core.tools.gen_problem_index(problem.index)}: {problem.entity.title}</h3>
                       </div>
                       <div className="ui stackable grid">
                           <div className="eight wide column" style={{textAlign:"center"}}>
                               <div ref={"problem_"+problem.id+"_judge_status"} style={{width: "100%", height: 360}}></div>
                           </div>
                           <div className="eight wide column" style={{textAlign:"center"}}>
                               <div ref={"problem_"+problem.id+"_timeused"} style={{width: "100%", height: 360}}></div>
                           </div>
                       </div>
                   </div>
                })}


            </div>
        </div>
    }

}

class StatisticAnalyzer{

    constructor(state){
        this.state = state;
    }

    getAreasName(area_item){
        return `${area_item[0]} ${area_item[2] ? "≤" : "<"} x ${area_item[3] ? "≤" : "<"} ${area_item[1]}`;
    }

    genFlagsList(){
        return [0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    genStatusFlagLabel(short){
        if(short){
            return [
                "AC", "PE", "TLE", "MLE", "WA",
                "RE", "OLE", "CE", "PE",
            ]
        } else {
            return [
                "评测通过", "格式错误", "时间超限", "内存超限", "答案错误",
                "运行时错误", "内容超限", "编译失败", "系统错误",
            ]
        }
    }

    calcReportScore(score_field){
        var asgn = this.state.asgn;
        /// 创建区间
        var AREAS = [];
        if(asgn.full_score > 10) {
            AREAS = [
                [0, 20, 1, 0], [20, 40, 1, 0], [40, 60, 1, 0], [60, 80, 1, 1],
                [80, 100, 0, 1], [100, 120, 0, 1], [120, 150, 0, 1],
            ];

            if (asgn.full_score <= 120) AREAS.splice(-1, 1);
            if (asgn.full_score <= 100) AREAS.splice(-1, 1);
            if (asgn.full_score <= 80) AREAS.splice(-1, 1);
            if (asgn.full_score < 60) AREAS.splice(-1, 1);
            if (asgn.full_score < 40) AREAS.splice(-1, 1);
        }else{
            AREAS = [
                [0, 2, 1, 0], [2, 4, 1, 0], [4, 6, 1, 0],
                [6, 8, 1, 0], [8, 10, 1, 0], [10, 10, 1, 1]
            ];
        }

        // 计算数据
        var reports = this.state.reports;
        var datas = [];
        for(var i = 0; i < AREAS.length; i++){
            var area = AREAS[i];
            var count = 0;
            for(var j = 0; j < reports.length; j++){
                var score = reports[j][score_field];
                var flag1 = true, flag2 = true;
                if(area[2]){
                    flag1 = (score >= area[0]);
                }else{
                    flag1 = (score > area[0]);
                }
                if(area[3]){
                    flag2 = (score <= area[1]);
                }else{
                    flag2 = (score < area[1]);
                }
                if(flag1 && flag2){
                    count += 1
                }
            }
            datas.push({
                value: count,
                name: this.getAreasName(area)
            });
        }

        return {
            legend_data: AREAS.map((item, key) => {return this.getAreasName(item)}),
            series_data: datas
        }
    }

    calcJudgeStatusTimeLine() {
        var FLAG_LABEL = this.genStatusFlagLabel();
        var FLAG_LABEL_EN = this.genStatusFlagLabel(true);
        var TIME_INTERVAL = 60 * 10 * 1000;        // 10分钟
        var judge_status = this.state.judge_status;
        // 全局统计
        var flags_list = this.genFlagsList();
        // 时间线
        var time_line_tmp = {};
        var time_line = {};
        // 题目统计
        var problems_flags = {};
        this.state.asgn.problems.map((item, key)=>{
            problems_flags[item.id] = this.genFlagsList();
        });
        if (judge_status.length > 0) {
            // 排序
            judge_status = judge_status.sort((a, b) => {
                return a.create_time > b.create_time ? 1 : -1;
            });
            var start_time = judge_status[0].create_time;
            var end_time = judge_status[judge_status.length - 1].create_time;
            var start_time_hash = Math.floor(start_time * 1.0 / TIME_INTERVAL) * TIME_INTERVAL;
            var end_time_hash = Math.ceil(end_time * 1.0 / TIME_INTERVAL) * TIME_INTERVAL;
            // 遍历评测结果
            for (var i = 0; i < judge_status.length; i++) {
                var status = judge_status[i];
                if (!this.state.students[status.author_id]) continue;
                if (status.flag >= 0 && status.flag <= 8)
                // 全局统计
                    flags_list[status.flag]++;
                // 单个题目统计
                if (problems_flags[status.virtual_problem_id])
                    problems_flags[status.virtual_problem_id][status.flag]++;

                // 筛选数据
                if (this.state.options.timeline_type === "3hr") {
                    if (status.create_time - start_time > 10800000) break;
                }
                else if (this.state.options.timeline_type === "12hr") {
                    if (status.create_time - start_time > 43200000) break;
                } else if (this.state.options.timeline_type === "1d") {
                    if (status.create_time - start_time > 86400000) break;
                } else if (this.state.options.timeline_type === "3d") {
                    if (status.create_time - start_time > 259200000) break;
                }
                // 时间区间
                var time_hash = Math.floor(status.create_time * 1.0 / TIME_INTERVAL) * TIME_INTERVAL;
                if (!time_line_tmp[time_hash]) {
                    time_line_tmp[time_hash] = this.genFlagsList();
                }
                // 统计自增
                time_line_tmp[time_hash][status.flag]++;
            }
            // 处理时间线数据
            for (var j = 0; j < FLAG_LABEL.length; j++) {
                var sdata = [];
                for (var k in time_line_tmp) {
                    var ts = parseInt(k);
                    sdata.push({
                        time_hash: ts,
                        name: new Date(ts).toString(),
                        value: [new Date(ts), time_line_tmp[k][j]]
                    })
                }
                sdata = sdata.sort((a, b) => {
                    return a.time_hash > b.time_hash ? 1 : -1;
                });
                time_line[j] = sdata;
            }
            // 处理题目评测状态数据
            var COLOR = ['#2ecc71', "#ffff00",'#f1c40f', '#e67e22', '#e74c3c', '#9b59b6', '#34495e', '#3498db', '#cccccc'];
            for (var m in problems_flags) {
                problems_flags[m] = problems_flags[m].map((item, key)=>{
                    return {
                        name: FLAG_LABEL_EN[key],
                        value: item,
                        itemStyle:{normal:{color:COLOR[key]}}
                    }
                })
            }
        }
        return {
            legend_data: FLAG_LABEL,
            legend_data_en: FLAG_LABEL_EN,
            problems: problems_flags,
            timeline: {
                series_data: FLAG_LABEL.map((item, key) => {return {
                    name: item,
                    type:'line',
                    areaStyle: {normal: {}},
                    stack: '时间线',
                    data:　time_line[key]
                }})
            },
            total: {
                series_data: FLAG_LABEL.map((item, key) => {return {name: item, value:flags_list[key]}}) || []
            },
        }
    }

    calcSolutions(){
        var problems_solutions = {};
        var solution_timeused = {};
        this.state.asgn.problems.map((item, key)=>{
            problems_solutions[item.id] = [0, 0];        // 访问总数, AC
        });
        var students_len = this.state.reports.length;
        var solutions = this.state.solutions;
        for (var i = 0; i < solutions.length; i++){
            var sol = solutions[i];
            if (!this.state.students[sol.author_id]) continue;
            var pid = sol.problem_id;
            if(!problems_solutions[pid]) continue;

            problems_solutions[pid][0]++;
            if(sol.accepted > 0) {
                problems_solutions[pid][1]++;
            }
            if(!solution_timeused[pid]){
                solution_timeused[pid] = [];
            }
            if(sol.used_time_real > 0) {
                // 筛选数据
                if (this.state.options.timeline_type === "3hr") {
                    if (sol.used_time_real > 10800) continue;
                } else if (this.state.options.timeline_type === "12hr") {
                    if (sol.used_time_real > 43200) continue;
                } else if (this.state.options.timeline_type === "1d") {
                    if (sol.used_time_real > 86400) continue;
                } else if (this.state.options.timeline_type === "3d") {
                    if (sol.used_time_real > 259200) continue;
                }
                solution_timeused[pid].push([
                    sol.used_time_real,
                    sol.submission > 0 ? parseInt((sol.accepted * 1.0 / sol.submission) * 100) : 0
                ]);
            }
        }
        for (var j in problems_solutions){
            var a = problems_solutions[j][0] - problems_solutions[j][1];
            var b = students_len - problems_solutions[j][0];
            problems_solutions[j] = [{
                name: "通过",
                value: problems_solutions[j][1],
                itemStyle:{normal:{color:"#3498db"}}
            },{
                name: "未通过",
                value: a < 0 ? 0 : a,
                itemStyle:{normal:{color:"#e74c3c"}}
            },{
                name: "未访问",
                value: b < 0 ? 0 : b,
                itemStyle:{normal:{color:"#777777"}}
            }];
        }
        return {
            problems: problems_solutions,
            timeused: solution_timeused
        }
    }
}

module.exports = AsgnStatistic;