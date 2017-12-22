/**
 * Created by lancelrq on 2017/3/14.
 */

module.exports = {
    truncatechars: function (data, len) {
        if(typeof data == "string"){
            var length = data.length;
            if(length > len){
                return data.substring(0, len) + "...";
            }else{
                return data
            }
        }else{
            return ""
        }
    }
};