<!doctype html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <style type="text/css">
        body{
            font-size: 12px;
        }
        @page {
            margin: 10mm 8mm 8mm 10mm;
            size: A4;
        }
    </style>
    <title>WeJudge 比赛打印服务</title>
</head>
<body>
    <h3>{{ contest.title }}</h3>
    <p>队伍名称：{{ printer_item.author.username }} {{ printer_item.author.nickname }} </p>
    <p>提交时间：{{ printer_item.create_time }}</p>
    <p>打印标题：{{ printer_item.title }}</p>
    <hr>
    <pre>{{ printer_item.content }}</pre>
    <script>
        window.print();
    </script>
</body>
</html>