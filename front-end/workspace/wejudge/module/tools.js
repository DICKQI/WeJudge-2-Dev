/**
 * Created by lancelrq on 2017/4/7.
 */

var React = require("react");

module.exports = {
    gen_problem_index: gen_problem_index,
    rank_list_time: rank_list_time,
    wejudge_timer: wejudge_timer,
    wejudge_countdown_timer: wejudge_countdown_timer,
    format_datetime: format_datetime,
    get_arrangement_desc: get_arrangement_desc,
    LightenDarkenColor: LightenDarkenColor,
    bytesToSize,
    generateIcon
};

function gen_problem_index(val) {
    try {
        var v = parseInt(val);
        var outstr = "";
        while (v > 0) {
            if (v % 26 !== 0)
                outstr = String.fromCharCode(v % 26 + 64) + outstr;
            else
                outstr = "Z" + outstr;
            if(v % 26 === 0) v--;
            v /= 26;
            v = Math.floor(v);
        }
        return outstr;
    }catch(e) {
        return "NaN"
    }
}

function rank_list_time(timestamp) {
    try {
        timestamp = parseInt(timestamp);
        var hour = Math.floor(timestamp / 3600);
        var minute = Math.floor((timestamp % 3600) / 60);
        var seconds = Math.floor(timestamp % 60);
        return `${hour}:${minute}:${seconds}`
    }catch(e){
        return ""
    }
}

function format_datetime(sec) {
    var moment = require("moment");
    return moment(sec * 1000).format("YYYY-MM-DD HH:mm:ss")
}

function wejudge_timer(sec, container) {
    document.getElementById(container).innerHTML = format_datetime(sec);
    setTimeout(function () {
        wejudge_timer(sec+1, container)
    }, 1000);
}

function wejudge_countdown_timer(sec, container) {
    if (sec <= 0) return;
    var timestamp = parseInt(sec);
    var day = Math.floor(timestamp / 86400);
    var hour = Math.floor(timestamp % 86400 / 3600);
    var minute = Math.floor((timestamp % 3600) / 60);
    var seconds = Math.floor(timestamp % 60);
    document.getElementById(container).innerHTML = `${day}天${hour}小时${minute}分钟${seconds}秒`;

    setTimeout(function(){
        wejudge_countdown_timer(sec-1, container)
    }, 1000);

}

function get_arrangement_desc(arrangement){
    //排课信息通用格式化工具
    var oe = "";
    if(arrangement.odd_even === 1){
        oe = "【单周】"
    }else if(arrangement.odd_even === 2){
        oe = "【双周】"
    }
    var week_names = ["日", "一", "二", "三", "四", "五", "六", "日"];
    return `${oe}周${week_names[arrangement.day_of_week]} ${arrangement.start_section}-${arrangement.end_section}节 (${arrangement.start_week}-${arrangement.end_week}周)`
}
function LightenDarkenColor(col, amt) {

    var usePound = false;

    if (col[0] === "#") {
        col = col.slice(1);
        usePound = true;
    }

    var num = parseInt(col,16);

    var r = (num >> 16) + amt;

    if (r > 255) r = 255;
    else if  (r < 0) r = 0;

    var b = ((num >> 8) & 0x00FF) + amt;

    if (b > 255) b = 255;
    else if  (b < 0) b = 0;

    var g = (num & 0x0000FF) + amt;

    if (g > 255) g = 255;
    else if (g < 0) g = 0;

    return (usePound?"#":"") + (g | (b << 8) | (r << 16)).toString(16);

}

function bytesToSize(bytes) {
    if (bytes === 0) return '0 B';

    var k = 1024;

    sizes = ['B','KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    i = Math.floor(Math.log(bytes) / Math.log(k));

    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
    //toPrecision(3) 后面保留一位小数，如1.0GB                                                                                                                  //return (bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i];
}
function generateIcon(filename){
    var fn = filename.split('.');
    if(fn.length < 2) return <i className="file outline icon" />;
    var ext = fn[fn.length -1];
    switch (ext){
        case "zip":
        case "rar":
        case "7z":
        case "tar":
        case "gz":
            return <i className="file archive outline icon" />;
        case "mp3":
        case "wav":
        case "egg":
        case "mid":
        case "wma":
        case "acc":
        case "flac":
            return <i className="file audio outline icon" />;
        case "c":
        case "h":
        case "cpp":
        case "py":
        case "java":
        case "sh":
        case "html":
        case "js":
        case "css":
        case "php":
        case "rc":
        case "go":
        case "vb":
        case "cs":
            return <i className="file code outline icon" />;
        case "xls":
        case "xlsx":
            return <i className="file excel outline icon" />;
        case "png":
        case "gif":
        case "jpg":
        case "jpeg":
        case "tiff":
        case "bmp":
            return <i className="file image outline icon" />;
        case "pdf":
            return <i className="file pdf outline icon" />;
        case "doc":
        case "docx":
            return <i className="file word outline icon" />;
        case "ppt":
        case "pptx":
            return <i className="file powerpoint outline icon" />;
        case "txt":
            return <i className="file text outline icon" />;
        case "mp4":
        case "avi":
        case "rmvb":
        case "mov":
        case "mkv":
        case "wmv":
        case "3gp":
        case "rm":
        case "flv":
            return <i className="file video outline icon" />;
        case "in":
        case "out":
        case "outdata":
            return <i className="file text icon" />;
        default:
            return <i className="file outline icon" />
    }
}