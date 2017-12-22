/**
 * Created by lancelrq on 2017/5/8.
 */

module.exports = ContestRankBoard;

var React = require("react");
var core = require("wejudge-core");


class ContestRankBoard extends core.PageView {
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.apis = {
            data: props.apis.rank_board
        };
        this.state['award_rank'] = 25;
        this.state['idCardDuration'] = 3000;
        this.state['animateDuration'] = 1500;
        this.state['duration'] = 1500;
        this.WeJudgeBoard = new WeJudgeContestBoardModule();
        this.loaded = false;
        this.startBoard = this.startBoard.bind(this);
        this.changeValue = this.changeValue.bind(this);
    }

    componentDidMount() {
        var that = this;
        this.getData();
    }

    startBoard(){
        var that = this;
        that.WeJudgeBoard.award_rank = this.state.award_rank;
        that.WeJudgeBoard.idCardDuration = this.state.idCardDuration;
        that.WeJudgeBoard.animateDuration = this.state.animateDuration;
        that.WeJudgeBoard.duration = this.state.duration;
        $("#Borad_Container").show();
        $("#RankBoardOption").hide();
        that.WeJudgeBoard.startBoard(this.state.data);
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
                                        <label>展示队伍名片(从第1名开始到？）</label>
                                        <input name="award_rank" type="text" value={this.state.award_rank} onChange={this.changeValue} />
                                    </div>
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
                            {problem_list.map((val, key)=>{
                                return (
                                    <td key={`th_${key}`}>
                                        {core.tools.gen_problem_index(problem_indexs[val])}
                                    </td>
                                )
                            })}
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

function WeJudgeContestBoardModule(){

    var WeJudgeBoard = {
        animateDuration: 1500,
        idCardDuration: 2000,
        duration: 2000,
        status_total: 0,
        rankList: [],
        judge_status: [],
        judge_status_1hr:[],
        cursor: 0,
        userList:{},
        problemIndexs:{},
        problemList:{},
        contestStartTime: 0,
        first_blood: {},
        worker: null,
        award_rank: 25,
        penalty_time: 1200,
        penalty_items: [],
        startBoard: function (entity) {
            // 这个方法建议只执行一次!
            WeJudgeBoard.judge_status = entity.judge_status_lte_1hr;               // 比赛封榜前的评测记录
            WeJudgeBoard.judge_status_1hr = entity.judge_status_1hr;               // 比赛封榜后到结束的评测记录
            WeJudgeBoard.problemIndexs = entity.problem_indexs;
            WeJudgeBoard.userList = entity.user_list;
            WeJudgeBoard.problemList = entity.problem_list;
            WeJudgeBoard.contestStartTime = entity.start_time;
            WeJudgeBoard.penalty_items = entity.penalty_items;
            WeJudgeBoard.penalty_time = entity.penalty_time;

            $("#loading_layout").hide();
            $.each(WeJudgeBoard.userList, function(index, value){
                var RankItem = {
                    rank: WeJudgeBoard.rankList.length,
                    user_id: index,
                    solved_problem: [],
                    problem_first_ac_time: {},
                    problem_submit_count: {},
                    rank_visited_problem:[],
                    timeuse: 0,
                    problem_ignore_count: {},
                    award: 0,
                    first_blood: [],
                    donot_rank: false     // 带*号的队伍不能rank
                };
                if(value.nickname.substring(0, 1) == "*"){
                    RankItem["donot_rank"] = true;
                }
                WeJudgeBoard.rankList.push(RankItem);
            });
            WeJudgeBoard.cursor = WeJudgeBoard.rankList.length - 1;     // 初始化游标
            WeJudgeBoard.calcLTEOneHourRank();
            WeJudgeBoard.fillJudgeSubmitStatus();
            $.scrollTo($("#uitem_" + WeJudgeBoard.rankList[WeJudgeBoard.rankList.length - 1].user_id).offset().top, WeJudgeBoard.animateDuration, function(){
                WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
            });

        },
        findEntity: function (rankList, user_id) {
            for(var i = 0; i < rankList.length; i++){
                if(rankList[i].user_id == user_id){
                    return i;
                }
            }
            return -1
        },
        calcRankItemData: function (RankItem, user_id, flag, problem_id, timestamp) {
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
                    RankItem.first_blood.push(problem_id);
                    WeJudgeBoard.first_blood[problem_id] = user_id;
                }
                RankItem.solved_problem.push(problem_id); // 加入到已经解决的问题列表中
                RankItem.problem_first_ac_time[problem_id] = timestamp - WeJudgeBoard.contestStartTime; //AC用时（秒）
                RankItem.timeuse = 0;
                for (var i = 0; i < RankItem.solved_problem.length; i++) {
                    var pid = RankItem.solved_problem[i];
                    //console.log(RankItem.problem_first_ac_time[pid], RankItem.problem_submit_count[pid], RankItem.problem_ignore_count[pid])
                    RankItem.timeuse += RankItem.problem_first_ac_time[pid] + WeJudgeBoard.penalty_time * (RankItem.problem_submit_count[pid] - RankItem.problem_ignore_count[pid] - 1)
                }
            } if (flag > 0) {
                if(WeJudgeBoard.penalty_items.indexOf(flag) == -1)
                    RankItem.problem_ignore_count[problem_id] += 1;
            }
            return RankItem;
        },
        calcLTEOneHourRank: function () {
            //计算一个封榜前的排行数据
            for(var i = 0; i < WeJudgeBoard.judge_status.length; i++){
                var item = WeJudgeBoard.judge_status[i];
                var user_id = item.user_id;
                var problem_id = item.problem_id;
                var timestamp = item.create_time;
                var flag = item.flag;
                var userRank = WeJudgeBoard.findEntity(WeJudgeBoard.rankList, user_id);
                var RankItem = null;
                // 获取项目
                RankItem = WeJudgeBoard.rankList[userRank];
                // 首先检测是不是已经通过了当前的题目，如果没有才计算，这个防止重复提交
                if (RankItem.problem_first_ac_time[problem_id] == undefined) {
                    RankItem = WeJudgeBoard.calcRankItemData(RankItem, user_id, flag, problem_id, timestamp); // 更新数据
                    WeJudgeBoard.rankList[userRank] = RankItem; // 写回
                    WeJudgeBoard.updateUserRankItem(RankItem); //更新项目
                    WeJudgeBoard.updateRankNum(RankItem, userRank);
                }
            }
            for(var j = 0; j < WeJudgeBoard.rankList.length; j++){
                var rankItem = WeJudgeBoard.rankList[j];
                WeJudgeBoard.createUserRankItem(rankItem);
                WeJudgeBoard.updateUserRankItem(rankItem);
            }
            WeJudgeBoard.refreshRankNumView();
        },
        fillJudgeSubmitStatus: function () {
            // 追加提交状态
            for(var i = 0; i < WeJudgeBoard.rankList.length; i++){
                var RankItem = WeJudgeBoard.rankList[i];
                var SolutionList = WeJudgeBoard.judge_status_1hr[RankItem.user_id];
                if(SolutionList == undefined) continue;
                $.each(SolutionList, function (index, value) {
                    if(value.submit_count > 0) {
                        var $t = $("#uitem_problem_" + index + "_" + RankItem.user_id);
                        if($t.html()=="")$t.html('+');
                        $t.removeClass();
                        $t.addClass("proc");
                    }
                });
            }
        },
        rollRank: function () {
            if(WeJudgeBoard.worker != null){
                clearTimeout(WeJudgeBoard.worker);
            }
            if(WeJudgeBoard.cursor >= 0){
                // 获取滚动项目
                var RankItem = WeJudgeBoard.rankList[WeJudgeBoard.cursor];
                // 高亮当前操作的用户
                var $viewItem = $("#uitem_" + RankItem.user_id);
                $viewItem.addClass("board_highlight");
                // 获取解决信息列表
                var SolutionList = WeJudgeBoard.judge_status_1hr[RankItem.user_id];
                if(SolutionList == undefined){
                    // 当前项目没有可以移动的
                    WeJudgeBoard.cursor -= 1;
                    $.scrollTo($viewItem.offset().top - 300, WeJudgeBoard.animateDuration / 2, function () {
                        $viewItem.removeClass("board_highlight");
                        if (RankItem.rank != -1 &&  RankItem.rank <= WeJudgeBoard.award_rank  && !RankItem.donot_rank) {
                            WeJudgeBoard.viewTeamIdCard(RankItem.user_id, RankItem.rank, function () {
                                WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                            });
                        }else{
                            WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                        }
                    });
                    return;
                }
                // 当前用户的rank
                var userRank = WeJudgeBoard.cursor;
                $.scrollTo($viewItem.offset().top - 300, WeJudgeBoard.animateDuration / 2, function () {
                    var i = 0;
                    for(; i < WeJudgeBoard.problemList.length; i++){

                        // 遍历这个人的过题信息
                        var problem_id = WeJudgeBoard.problemList[i];
                        var solution = SolutionList[problem_id];

                        if(RankItem.rank_visited_problem[problem_id] != undefined){
                            // 这题已经访问过了
                            continue;
                        }
                        if(solution == undefined){
                            // 没有就跳过
                            continue;
                        }
                        RankItem.rank_visited_problem[problem_id] = true;
                        if(solution.ac_flag){
                            // 如果有过题记录，重算判题时间
                            // 推入已解决的问题ID
                            RankItem.solved_problem.push(problem_id);
                            RankItem.problem_first_ac_time[problem_id] = solution.ac_time;  //AC用时（秒）
                            if (WeJudgeBoard.first_blood[problem_id] == undefined) {
                                RankItem.first_blood.push(problem_id);
                                WeJudgeBoard.first_blood[problem_id] = RankItem.user_id;
                            }
                            if(RankItem.problem_submit_count[problem_id] == undefined) RankItem.problem_submit_count[problem_id] = 0;
                            if(RankItem.problem_ignore_count[problem_id] == undefined) RankItem.problem_ignore_count[problem_id] = 0;
                            RankItem.problem_submit_count[problem_id] += solution.submit_count;
                            RankItem.problem_ignore_count[problem_id] += solution.ignore_count;
                            RankItem.timeuse = 0;
                            for (var j = 0; j < RankItem.solved_problem.length; j++) {
                                var pid = RankItem.solved_problem[j];
                                RankItem.timeuse += RankItem.problem_first_ac_time[pid] + WeJudgeBoard.penalty_time * (RankItem.problem_submit_count[pid] - RankItem.problem_ignore_count[pid] - 1)
                            }
                            WeJudgeBoard.rankList[userRank] = RankItem;     // 写回
                            WeJudgeBoard.updateUserRankItem(RankItem, problem_id);      //更新项目
                            var snapshot = WeJudgeBoard.rankList.concat();       // 创建原先的列表快照
                            var index = WeJudgeBoard.updateRankNum(RankItem, userRank); // 更新排名
                            WeJudgeBoard.refreshRankNumView(); // 更新排名视图
                            if (userRank != index) {
                                // 如果排名发生变化
                                var fb = false;
                                if(RankItem.first_blood.length > 0){
                                    for(var j = 0; j < RankItem.first_blood.length; j++){
                                        if(RankItem.first_blood[j] == problem_id){
                                            fb = true;
                                        }
                                    }
                                }
                                if(fb){
                                    WeJudgeBoard.viewTeamIdCard(RankItem.user_id, RankItem.rank, function () {
                                        WeJudgeBoard.moveTo($viewItem, $("#uitem_" + snapshot[index].user_id), function () {
                                            WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                                        });
                                    });
                                }else {
                                    WeJudgeBoard.moveTo($viewItem, $("#uitem_" + snapshot[index].user_id), function () {
                                        WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                                    });
                                }
                                return;
                            }else{
                                $viewItem.removeClass("board_highlight");
                                // 如果没有发生变化，继续执行扫描下一道题
                                WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                                return;
                            }
                        }else{
                            if(RankItem.problem_submit_count[problem_id] == undefined) RankItem.problem_submit_count[problem_id] = 0;
                            if(RankItem.problem_ignore_count[problem_id] == undefined) RankItem.problem_ignore_count[problem_id] = 0;
                            RankItem.problem_submit_count[problem_id] += solution.submit_count;
                            RankItem.problem_ignore_count[problem_id] += solution.ignore_count;
                            WeJudgeBoard.rankList[userRank] = RankItem;     // 写回
                            WeJudgeBoard.updateUserRankItem(RankItem, problem_id);      //更新项目
                            $viewItem.removeClass("board_highlight");
                            WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                            return;
                        }
                    }
                    setTimeout(function () {
                        $viewItem.removeClass("board_highlight");
                        // 如果循环走到这里，还没有被return，那只能说明一点，就是当前项目已经不会再有变化了，于是游标减1
                        WeJudgeBoard.cursor -= 1;
                        if (RankItem.rank != -1 &&  RankItem.rank <= WeJudgeBoard.award_rank  && !RankItem.donot_rank) {
                            WeJudgeBoard.viewTeamIdCard(RankItem.user_id, RankItem.rank, function () {
                                WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                            });
                        }else{
                            WeJudgeBoard.worker = setTimeout(WeJudgeBoard.rollRank, WeJudgeBoard.duration);
                        }
                    }, WeJudgeBoard.duration / 2);
                });
            }
        },
        viewTeamIdCard: function (user_id, rank, callback) {
            if(typeof callback != "function"){
                callback =  function () {}
            }
            var $idcard = $("#TeamIdCard");
            var $cont = $("#TeamIdCardContent");
            var $image = $("#TeamIdCardImg");
            var user = WeJudgeBoard.userList[user_id];
            var uname = user.nickname;
            if(user.sex == 0){
                uname = "<span style='color:red'>" + uname + "</span>";
            }
            $cont.html("<h1>第"+rank+"名</h1><h2>"+uname+" <small>("+user.username+")</small></h2>" +
                "<h3>"+user.realname+"</h3>");
            $image.attr("src", (user.headimg == null || user.headimg == "")? "/static/images/user_placeholder.png" :"/resource/headimg/" + user.headimg);
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
            var rank = 1;
            for(var i = 0; i < WeJudgeBoard.rankList.length; i++){
                var item = WeJudgeBoard.rankList[i];
                if(!item.donot_rank) {
                    item.rank = rank++;
                }else{
                    item.rank = -1;
                }
                $("#uitem_rank_" + item.user_id).text(item.rank == -1 ? "": item.rank);
            }
        },
        updateUserRankItem: function(item, problem) {
            var problems;
            if(problem == undefined){
                problems = WeJudgeBoard.problemList;
            }else{
                problems = [problem];
            }
            var user = WeJudgeBoard.userList[item.user_id];
            var uname = user.nickname
            if(user.sex == 0){
                uname = "<span style='color:red'>" + uname + "</span>";
            }
            $("#uitem_user_"+item.user_id).html(uname + " ("+user.username+")<br />" + user.realname);
            $("#uitem_solved_"+item.user_id).text(item.solved_problem.length);
            $("#uitem_time_"+item.user_id).text(parseInt(item.timeuse / 60));
            for(var i = 0 ; i < problems.length; i++){
                var pid = problems[i];
                var color;
                var text;
                if(item.problem_first_ac_time[pid] == undefined){
                    if (item.problem_submit_count[pid] != undefined && item.problem_submit_count[pid] > 0) {
                        color = "noac";
                        text = item.problem_submit_count[pid]
                    }else{
                        color = "";
                        text = "";
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
                    var myImage = canvas.toDataURL("image/png");
                    var img = document.getElementById("MoveItemImgBody");
                    img.src = myImage;
                    img.width = $("#board").width();
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
                    // 叶启权说，移动的时候直接飞上去就好了，不用聚焦。。。
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
        }
    };
    return WeJudgeBoard;
}

