<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ contest.title }}</title>
    <link rel="stylesheet" href="/static/assets/semantic/semantic.min.css">
    <style type="text/css">
    table{
        background: #34495e;
        color: #fff;
        font-size:16px;
    }
    table > thead > tr > td {
        background: #2c3e50 !important;
        border: 1px solid #000 !important;
        color: #fff !important;
        text-align: center !important;
        font-weight: bold;
        font-size: 18px;
    }
    td {
        background: #2c3e50 !important;
        vertical-align: middle !important;
        text-align: center ;
        border: 1px solid #000 !important;
        height: 60px;
        color: #fff !important;
    }
    .board_highlight td {
        background: #3498db  !important;
    }
    td.proc{
        background: #f1c40f !important;
    }
    td.proc.animated{
        animation: proc_animation;
        animation-duration: 100ms;
        animation-iteration-count: infinite;
        animation-direction: alternate;
    }
    @keyframes proc_animation {
        from{
            background: #f1c40f;
        }
        to{
            background: #2c3e50;
        }
    }
    td.ac {
        background: #2ecc71  !important;
    }
    td.noac{
        background: #e74c3c !important;
    }
    td.first_blood{
        background: #008800 !important;
    }
    #procbar{
        background: #f00;
        height: 4px;
        position: fixed;
        top:0;
    }
    #TeamIdCard{
        display: none;
        position: fixed;
        top: 50%;
        left: 50%;
        width: 640px;
        height: 300px;
        margin-left: -300px;
        margin-top: -150px;
        border: 1px solid #2c3e50;
        background: #fff;
        clear: both;
    }
    #TeamIdCardImgLayout{
        width: 280px;
        height:2980px;
        float:left;
        text-align: center;
        line-height:298px;
    }
    #TeamIdCardContent{
        padding: 25px;
        width: 300px;
        height:249px;
        float:left;
    }

    </style>
</head>
<body>
    <div class="header_container" align="center" style="padding: 10px;">
        <h1>{{ contest.title }}</h1>
    </div>
    <div id="main_container">

    </div>
    <script type="text/javascript" src="/static/assets/wejudge/app.js?v2.0.20170422.2"></script>
    <script type="text/javascript" src="/static/assets/html2canvas.min.js"></script>
    <script type="text/javascript" src="/static/assets/jquery.scrollTo.min.js"></script>
    <script type="text/javascript">
        $(function () {
           wejudge.contest.contest.showContestRankBoard(
               'main_container',
               {
                   rank_board: "{% url 'api.contest.rank.board' contest.id %}"
                   //rank_board: "/static/temp.json"
               }
           )
        });
    </script>
</body>
</html>