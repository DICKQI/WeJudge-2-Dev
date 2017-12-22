/**
 * Created by lancelrq
 */

var handler = function (req, rep) {
    rep.write("WeJudge WebSocket Boardcast Service");
    rep.end();
};

var app = require('http').createServer(handler);
var io = require('socket.io')(app);

app.listen(8081);


io.of("contest").on('connection', function (socket) {
    socket.emit('notice', { content: '这个是公告测试' });
});