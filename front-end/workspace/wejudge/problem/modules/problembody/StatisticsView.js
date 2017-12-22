/**
 * Created by lancelrq on 2017/8/2.
 */

var React = require('react');
var core = require('wejudge-core');

module.exports = StatisticsView;

class StatisticsView extends core.PageView {

    // 构造
    constructor(props) {
        super(props);
        this.apis ={
            data: props.statistics_api
        }
    }


    load(){
        var that = this;
        this.getData(null, function (rel) {
            that.loadJudgeCharts();
            that.loadLangCharts();
        });
    }

    loadLangCharts(){
        var that = this;
        var language = this.state.data.language;
        var langs = [1, 2, 4, 8, 16];
        var langChart = echarts.init(that.refs.Echarts_LanguageCounter);
        var data1 = {
            wejudge: 0,
            education: 0,
            contest: 0,
        };
        for(var i = 0; i < langs.length; i++){
            data1['wejudge'] += language['wejudge'][langs[i]];
            data1['education'] += language['education'][langs[i]];
            data1['contest'] += language['contest'][langs[i]];
        }
        langChart.setOption({
            title: {
                text: "评测语言分布图",
                left: "center",
                subtext: ""
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'left',
                data:['C语言', 'C++', 'Java', 'Python 2', 'Python 3', 'WeJudge题库系统', '教学系统', '比赛系统']
            },
            series: [
                {
                    name:'子系统统计',
                    type:'pie',
                    selectedMode: 'single',
                    radius: [0, '30%'],

                    label: {
                        normal: {
                            position: 'inner'
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data:[
                        data1['wejudge'] > 0 ? {value:data1['wejudge'], name:'题库系统'} : {},
                        data1['education'] > 0 ? {value:data1['education'], name:'教学系统'} : {},
                        data1['contest'] > 0 ? {value:data1['contest'], name:'比赛系统'} : {}
                    ]
                },
                {
                    name:'编程语言',
                    type:'pie',
                    radius: ['40%', '55%'],
                    data:[
                        {value:language['total'][1], name:'C语言', itemStyle:{normal:{color:"#2980b9"}}},
                        {value:language['total'][2], name:'C++', itemStyle:{normal:{color:"#e74c3c"}}},
                        {value:language['total'][4], name:'Java', itemStyle:{normal:{color:"#8e44ad"}}},
                        {value:language['total'][8], name:'Python 2', itemStyle:{normal:{color:"#f1c40f"}}},
                        {value:language['total'][16], name:'Python 3', itemStyle:{normal:{color:"#2ecc71"}}}
                    ]
                }
            ]
        });

    }

    loadJudgeCharts(){
        var that = this;
        var judge = this.state.data.judge;
        var JUDGE_STATE = ['AC', 'PE', 'TLE', 'MLE', 'WA', 'RE', 'OLE', 'CE', 'SE'];
        var JUDGE_STATE_CALL = ['评测通过(AC)', '格式错误(PE)', '超过时间限制(TLE)',
            '内存限制(MLE)', '答案错误(WA)', '运行时错误(RE)',
            '输出内容超限(OLE)', '编译失败(CE)', '系统错误(SE)'];
        var SUB_APPS = ['wejudge', 'education', 'contest'];
        var SUB_APPS_CALL = ['WeJudge题库系统', '教学系统', '比赛系统'];
        var STATE_COLOR = ["#8BC34A", "#FFEB3B", "#FF9800", "#9C27B0", "#F44336", "#FF4081", "#795548", "#448AFF", "#727272"];
        var series = [];
        for(var i = 0; i < SUB_APPS.length; i++){
            var data = [];
            for(var j = 0 ; j < JUDGE_STATE.length; j++) {
                data.push({
                    value: judge[SUB_APPS[i]][j],
                    itemStyle: {
                        normal: {
                            color: core.tools.LightenDarkenColor(STATE_COLOR[j], i * 30)
                        }
                    }
                })
            }
            series.push({
                name:SUB_APPS_CALL[i],
                type:'bar',
                stack: "wejudge",
                data: data
            });
        }
        var judgeChart = echarts.init(that.refs.Echarts_JudgeCounter);
        judgeChart.setOption({
            title: {
                text: "评测历史统计图",
                left: "center",
                subtext: ""
            },
            color:["#333333", "#777777", "#BBBBBB"],
            //color: ["#284e9b", "#3b7de6", "#448AFF"],
            legend: {
                data: SUB_APPS_CALL,
                align: "right",
                right: 0,
                orient: "vertical",
            },
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                containLabel: true
            },
            xAxis : [
                {
                    type : 'category',
                    data : JUDGE_STATE_CALL,
                    axisLabel:{
                        formatter: function (value, index) {
                            return JUDGE_STATE[JUDGE_STATE_CALL.indexOf(value)] || ""
                        }
                    },
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
            series : series
        });
    }

    renderBody(){
        var statistics_data = this.state.data;
        return (
            <div className="ui">
                {statistics_data ? <div className="ui two column stackable grid segment">
                    <div className="column">
                        <div ref="Echarts_LanguageCounter" style={{width:"100%", height: 400}}></div>
                    </div>
                    <div className="column">
                        <div ref="Echarts_JudgeCounter" style={{width:"100%", height: 400}}></div>
                    </div>
                </div> : null}
            </div>
        )
    }
}