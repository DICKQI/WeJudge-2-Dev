/**
 * Created by lancelrq on 2017/9/13.
 */

module.exports = AsgnRankBoard;

var React = require("react");
var core = require("wejudge-core");


class AsgnRankBoard extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.time_line
        };
        this.inited = false;
        this.state['idCardDuration'] = 3000;
        this.state['animateDuration'] = 1500;
        this.state['duration'] = 1500;
        this.WeJudgeBoard = new WeJudgeAsgnRankBoardModule();
        this.loaded = false;
        this.startBoard = this.startBoard.bind(this);
        this.changeValue = this.changeValue.bind(this);
    }

    componentDidMount() {
        this.getData();
    }

    startBoard(){
        var that = this;
        if(that.inited) return;
        that.WeJudgeBoard.idCardDuration = this.state.idCardDuration;
        that.WeJudgeBoard.animateDuration = this.state.animateDuration;
        that.WeJudgeBoard.duration = this.state.duration;
        that.WeJudgeBoard.time_line_api = this.props.apis.time_line;
        that.WeJudgeBoard.avatar_api = this.props.urls.view_headimg;
        $("#Borad_Container").show();
        $("#RankBoardOption").hide();
        that.WeJudgeBoard.startBoard(this.state.data);
        that.inited = true;
    }

    changeValue(e){
        var target_name = e.target.name;
        var t = {};
        try {
            t[target_name] = parseInt(e.target.value);
        }catch (e){
            t[target_name] = 0
        }
        this.setState(t);
    }


    renderBody() {
        var data = this.state.data;
        var problem_indexs = data.problem_indexs;
        var problem_list = data.problem_list;

        return (
            <div className="ui">

                <div id="RankBoardOption">
                    <form className="ui form">
                        <div className="ui card" style={{margin:"0 auto"}}>
                            <div className="content">
                                <div className="header">
                                    滚榜设置
                                </div>
                                <div className="meta">你可以设置滚榜参数</div>
                                <div className="description">
                                    <div className="field">
                                        <label>动画时长(ms)</label>
                                        <input name="animateDuration" type="text" value={this.state.animateDuration} onChange={this.changeValue}  />
                                    </div>
                                    <div className="field">
                                        <label>名片展示时长(ms)</label>
                                        <input name="idCardDuration" type="text" value={this.state.idCardDuration} onChange={this.changeValue}  />
                                    </div>
                                    <div className="field">
                                        <label>轮询间隔(ms)</label>
                                        <input name="duration" type="text" value={this.state.duration} onChange={this.changeValue}  />
                                    </div>
                                </div>
                            </div>
                            <div className="extra content">
                                <button type="button" className="ui fluid basic green button" onClick={this.startBoard}>开始滚榜</button>
                            </div>
                        </div>
                    </form>
                </div>

                <div style={{margin: "5px 3%", display: "none"}} id="Borad_Container">
                    <table id="board" className="ui table bordered">
                        <thead>
                        <tr>
                            <td width="80">Rank</td>
                            <td>User</td>
                            <td width="80">Solved</td>
                            <td width="100">Time</td>
                            {problem_list ? problem_list.map((val, key)=>{
                                return (
                                    <td key={`th_${key}`}>
                                        {core.tools.gen_problem_index(problem_indexs[val])}
                                    </td>
                                )
                            }) : null}
                        </tr>
                        </thead>
                        <tbody id="RankBoardBody">

                        </tbody>
                    </table>
                </div>

                <div id="MoveItemImgContainer" style={{position: "absolute", display: "none"}}>
                    <img id="MoveItemImgBody" src="" alt="" />
                </div>
                <div id="TeamIdCard">
                    <div id="TeamIdCardImgLayout">
                        <img src="" width="240" height="240" alt="" id="TeamIdCardImg" />
                    </div>
                    <div id="TeamIdCardContent">

                    </div>
                </div>

            </div>
        );
    }
}

function WeJudgeAsgnRankBoardModule() {
    var WeJudgeBoard = {
        time_line_api: "",
        avatar_api: "view_headimg",
        animateDuration: 1500,
        idCardDuration: 2000,
        duration: 2000,
        timeLineDuration: 30000,
        status_total: 0,
        rankList: [],
        statusQueue:[],
        userList:{},
        problemIndexs:{},
        problemList:{},
        contestStartTime: 0,
        first_blood: {},
        time_line: 0,
        worker: null,
        worker_timeline: null,
        startBoard: function (entity) {
            // 这个方法只能执行一次!
            WeJudgeBoard.statusQueue = entity.judge_status;
            WeJudgeBoard.problemIndexs = entity.problem_indexs;
            WeJudgeBoard.userList = entity.user_list;
            WeJudgeBoard.problemList = entity.problem_list;
            WeJudgeBoard.status_total = entity.judge_status.length;
            WeJudgeBoard.time_line = entity.nowtime;
            $("#loading_layout").hide();
            WeJudgeBoard.calcInitRank();
            WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
            WeJudgeBoard.worker_timeline = setTimeout(WeJudgeBoard.time_line_worker, WeJudgeBoard.timeLineDuration);
        },
        time_line_worker: function () {
            if(WeJudgeBoard.worker_timeline != null){
                clearTimeout(WeJudgeBoard.worker_timeline);
            }
            console.log("Timeline Tick!")
            core.restful({
                method: "POST",
                responseType: "json",
                url: WeJudgeBoard.time_line_api + "?time=" + WeJudgeBoard.time_line,
                success: function (rel) {
                    var status = rel.data.judge_status;
                    for(var i = 0 ; i < status.length; i++){
                        WeJudgeBoard.statusQueue.push(status[i]);
                    }
                    WeJudgeBoard.userList = rel.data.user_list;
                    WeJudgeBoard.time_line = rel.data.nowtime;
                    WeJudgeBoard.worker_timeline = setTimeout(WeJudgeBoard.time_line_worker, WeJudgeBoard.timeLineDuration);
                },
                error:function (rel, msg) {
                    alert(msg);
                }
            }).call();
        },
        calcInitRank: function () {
            //计算初始化排名信息
            while(WeJudgeBoard.statusQueue.length > 0){
                var item = WeJudgeBoard.statusQueue.shift();
                var user_id = item.user_id;
                if(WeJudgeBoard.userList[user_id] == undefined){
                    // 如果没有数据，自动忽略
                    continue;
                }
                var problem_id = item.problem_id;
                var timestamp = item.timestamp;
                var flag = item.flag;
                var userRank = WeJudgeBoard.findEntity(WeJudgeBoard.rankList, user_id);
                var RankItem = null;
                // 如果没有找到用户数据
                if (userRank == -1) {
                    RankItem = {
                        rank: WeJudgeBoard.rankList.length,
                        user_id: user_id,
                        solved_problem: [],
                        problem_first_ac_time: {},
                        problem_submit_count: {},
                        timeuse: 0,
                        problem_ignore_count:{}
                    };
                    WeJudgeBoard.rankList.push(RankItem);
                    WeJudgeBoard.createUserRankItem(RankItem);
                    WeJudgeBoard.updateUserRankItem(RankItem);
                    userRank = WeJudgeBoard.rankList.length - 1;
                }else {
                    // 获取项目
                    RankItem = WeJudgeBoard.rankList[userRank];
                }
                // 首先检测是不是已经通过了当前的题目，如果没有才计算，这个防止重复提交
                if (RankItem.problem_first_ac_time[problem_id] == undefined) {
                    RankItem = WeJudgeBoard.rollRankItemData(RankItem, user_id, flag, problem_id, timestamp); // 更新数据
                    WeJudgeBoard.rankList[userRank] = RankItem;             // 写回
                    WeJudgeBoard.updateUserRankItem(RankItem);
                    var snapshot = WeJudgeBoard.rankList.concat();       // 创建原先的列表快照
                    var index = WeJudgeBoard.updateRankNum(RankItem, userRank);
                    if(index != userRank){
                        WeJudgeBoard.moveToNoAni($("#uitem_" + user_id), $("#uitem_" + snapshot[index].user_id))
                    }

                }
            }
            WeJudgeBoard.refreshRankNumView();
        },
        rollRankItemData: function (RankItem, user_id, flag, problem_id, timestamp) {
            var start_time = 0;
            if(WeJudgeBoard.userList[user_id] == undefined){
                // 如果没有用户数据，自动忽略
                return;
            }else{
                start_time = WeJudgeBoard.userList[user_id].start_time;
            }
            if (RankItem.problem_submit_count[problem_id] == undefined) {
                // 计算提交次数
                RankItem.problem_submit_count[problem_id] = 1
            } else {
                RankItem.problem_submit_count[problem_id] += 1
            }
            if (RankItem.problem_ignore_count[problem_id] == undefined) {
                RankItem.problem_ignore_count[problem_id] = 0;
            }
            if (flag == 0) {
                if (WeJudgeBoard.first_blood[problem_id] == undefined) {
                    WeJudgeBoard.first_blood[problem_id] = user_id;
                }
                RankItem.solved_problem.push(problem_id); // 加入到已经解决的问题列表中
                RankItem.problem_first_ac_time[problem_id] = timestamp - start_time; //AC用时（秒）
                RankItem.timeuse = 0;
                for (var i = 0; i < RankItem.solved_problem.length; i++) {
                    var pid = RankItem.solved_problem[i];
                    RankItem.timeuse += RankItem.problem_first_ac_time[pid] + 1200 * (RankItem.problem_submit_count[pid] - RankItem.problem_ignore_count[pid] - 1)
                }
            } else if (flag < 0 || flag >= 8) {
                RankItem.problem_ignore_count[problem_id] += 1;
            }
            return RankItem;
        },
        findEntity: function (rankList, user_id) {
            for(var i = 0; i < rankList.length; i++){
                if(rankList[i].user_id == user_id){
                    return i;
                }
            }
            return -1
        },
        rollRank: function () {
            if(WeJudgeBoard.worker != null){
                clearTimeout(WeJudgeBoard.worker);
            }
            if(WeJudgeBoard.statusQueue.length <= 0){
                // 如果队列为空
                setTimeout(function () {
                    WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                }, WeJudgeBoard.duration)
            }else {
                var item = WeJudgeBoard.statusQueue.shift();
                var user_id = item.user_id;
                if(WeJudgeBoard.userList[user_id]==undefined){
                    // 用户不存在就不用处理
                    return;
                }
                var problem_id = item.problem_id;
                var timestamp = item.timestamp;
                var flag = item.flag;
                var userRank = WeJudgeBoard.findEntity(WeJudgeBoard.rankList, user_id);
                var RankItem = null;
                if (userRank == -1) {
                    RankItem = {
                        rank: WeJudgeBoard.rankList.length,
                        user_id: user_id,
                        solved_problem: [],
                        problem_first_ac_time: {},
                        problem_submit_count: {},
                        timeuse: 0,
                        problem_ignore_count:{}
                    };
                    WeJudgeBoard.rankList.push(RankItem);
                    WeJudgeBoard.createUserRankItem(RankItem);
                    WeJudgeBoard.updateUserRankItem(RankItem);
                    userRank = WeJudgeBoard.rankList.length - 1;
                }else {
                    // 获取项目
                    RankItem = WeJudgeBoard.rankList[userRank];
                }
                // 首先检测是不是已经通过了当前的题目，如果没有才计算，这个防止重复提交
                if (RankItem.problem_first_ac_time[problem_id] == undefined) {
                    RankItem = WeJudgeBoard.rollRankItemData(RankItem, user_id, flag, problem_id, timestamp); // 更新数据
                    WeJudgeBoard.rankList[userRank] = RankItem; // 写回
                    WeJudgeBoard.updateUserRankItem(RankItem); //更新项目
                    var snapshot = WeJudgeBoard.rankList.concat();       // 创建原先的列表快照
                    var index = WeJudgeBoard.updateRankNum(RankItem, userRank);
                    WeJudgeBoard.refreshRankNumView();
                    if (userRank != index) {
                        var $s = $("#uitem_" + user_id);
                        $s.addClass("board_highlight");
                        $.scrollTo($s.offset().top - 100, WeJudgeBoard.animateDuration, function () {
                            WeJudgeBoard.viewTeamIdCard(user_id, problem_id, userRank, index, function () {
                                WeJudgeBoard.moveTo($s, $("#uitem_" + snapshot[index].user_id), function () {
                                    WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                                })
                            });
                        });
                    } else {
                        var $changeItem = $("#uitem_" + user_id);
                        $changeItem.addClass("board_highlight");
                        $.scrollTo($changeItem.offset().top - 100, WeJudgeBoard.animateDuration / 2, function () {
                            $changeItem.removeClass("board_highlight");
                            WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration / 4);
                        });
                    }
                }else{
                    WeJudgeBoard.rollRank();
                }
            }
        },
        viewTeamIdCard: function (user_id, pid, pre, now, callback) {
            if(typeof callback != "function"){
                callback =  function () {}
            }
            var $idcard = $("#TeamIdCard");
            var $cont = $("#TeamIdCardContent");
            var $image = $("#TeamIdCardImg");
            var user = WeJudgeBoard.userList[user_id];
            $cont.html("<h2>"+user.author.nickname+" <small>("+user.author.username+")</small></h2>" +
                "<h3>"+user.author.realname+"</h3>" +
                "<h3 style='color: #008800'>题目"+WeJudgeBoard.generateIndex(WeJudgeBoard.problemIndexs[pid])+" - Accepted<br /><br />排名："+(pre+1) + " -> " + (now +1) +"</h3>");
            $image.attr("src", WeJudgeBoard.avatar_api.replace("space/0", "space/" + user_id));
            $idcard.show();
            setTimeout(function () {
                $idcard.hide();
                callback();
            }, WeJudgeBoard.idCardDuration);
        },
        generateIndex: function (index) {
            if(index <= 26){
                return String.fromCharCode(64 + index);
            }
        },
        updateRankNum: function(item, index){
            //执行插入排序实现(传入的是处理项目和其原始位置)，由于是AC，所以一定会有提升
            for(var i = index - 1; i>=0; i--){
                var nitem = WeJudgeBoard.rankList[i]; // i位置上的元素
                if(item.solved_problem.length > nitem.solved_problem.length){
                    // 如果item解决问题数 > nitem，左移动item
                    WeJudgeBoard.rankList[i] = item;
                    WeJudgeBoard.rankList[i + 1] = nitem;
                }else if(item.solved_problem.length == nitem.solved_problem.length){
                    if(item.timeuse < nitem.timeuse){
                        // nitem比item用时多
                        WeJudgeBoard.rankList[i] = item;
                        WeJudgeBoard.rankList[i + 1] = nitem;
                    }else if(item.timeuse == nitem.timeuse){
                        return i + 1;
                    }else{
                        return i + 1;
                    }
                }
                else{
                    return i + 1;
                }
            }
            return 0;
        },
        refreshRankNumView: function () {
            for(var i = 0; i < WeJudgeBoard.rankList.length; i++){
                var item = WeJudgeBoard.rankList[i];
                $("#uitem_rank_"+item.user_id).text(i+1);
            }

        },
        updateUserRankItem: function(item) {
            var user = WeJudgeBoard.userList[item.user_id];
            $("#uitem_user_"+item.user_id).html(user.author.nickname + "("+user.author.username+")<br />" + user.author.realname);
            $("#uitem_solved_"+item.user_id).text(item.solved_problem.length);
            $("#uitem_time_"+item.user_id).text(parseInt(item.timeuse / 60));
            for(var i = 0 ; i < WeJudgeBoard.problemList.length; i++){
                var pid = WeJudgeBoard.problemList[i];
                var color;
                var text;
                if(item.problem_first_ac_time[pid] == undefined){
                    if (item.problem_submit_count[pid] > 0) {
                        color = "noac";
                        text = item.problem_submit_count[pid]
                    }else{
                        color = "";
                        text = ""
                    }
                }else{
                    if(WeJudgeBoard.first_blood[pid] == item.user_id){
                        color = "first_blood";
                    }else {
                        color = "ac";
                    }
                    text = item.problem_submit_count[pid] + "/" + parseInt(item.problem_first_ac_time[pid] / 60)
                }
                var $t = $("#uitem_problem_"+ pid +"_"+item.user_id);
                $t.text(text);
                if(color != ""){
                    $t.removeClass();
                    $t.addClass(color);
                }else{
                    $t.removeClass();
                }
            }
        },
        createUserRankItem: function (item) {
            var html = "<tr id='uitem_"+item.user_id+"'>" +
                "<td id='uitem_rank_"+item.user_id+"'></td>" +
                "<td id='uitem_user_"+item.user_id+"'></td>" +
                "<td id='uitem_solved_"+item.user_id+"'></td>" +
                "<td id='uitem_time_"+item.user_id+"'></td>";
            for(var i = 0 ; i < WeJudgeBoard.problemList.length; i++){
                html += "<td id='uitem_problem_"+WeJudgeBoard.problemList[i]+"_"+item.user_id+"'></td>";
            }

            $("#RankBoardBody").append(html + "</tr>");
        },
        moveTo: function ($source, $target, callback) {
            if(typeof callback != "function"){
                callback =  function () {}
            }
            html2canvas($source, {
                onrendered: function(canvas) {
                    var $item = $source;
                    var $clone = $item.clone();
                    var $imgLayout = $("#MoveItemImgContainer");
                    var myImage = canvas.toDataURL("image/jpg");
                    var img = document.getElementById("MoveItemImgBody");
                    img.src = myImage;
                    var ptop = $item.offset().top;
                    $imgLayout.css({
                        left: $item.offset().left,
                        top: $item.offset().top
                    });
                    $imgLayout.show();
                    $clone.css("visibility", "hidden");
                    $item.remove();
                    $target.before($clone);
                    var aniduration = Math.abs(parseInt(ptop - $clone.offset().top) / 10) + WeJudgeBoard.animateDuration;
                    var sduration = (aniduration > WeJudgeBoard.animateDuration) ? WeJudgeBoard.animateDuration : aniduration;
                    $.scrollTo($clone.offset().top - 100,  sduration, function () {});
                    $imgLayout.animate({
                        top: $clone.offset().top
                    }, aniduration, null, function () {
                        $clone.css("visibility", "visible");
                        $clone.removeClass("board_highlight");
                        $imgLayout.hide();
                        callback();
                    });

                }
            });
        },
        moveToNoAni: function ($source, $target) {
            var $item = $source;
            var $clone = $item.clone();
            $item.remove();
            $target.before($clone);
        }
    };
    return WeJudgeBoard;
}