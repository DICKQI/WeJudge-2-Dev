/**
 * RESTful API by LanceLRQ
 * ver: 0.1
 */

module.exports = function backend(options)
{
    var obj = Object.create(GRESTP_ENTITY);
    obj.options = options;
    obj.init();
    return obj;
};

function isValid(options) {
    return !!(!options || (options && typeof options === "object"));
}

var GRESTP_ENTITY = {

    init: function (){
        //检测用户传进来的参数是否合法
        if (!isValid(this.options))
            throw new ReferenceError("参数对象异常");
    },

    call: function(url){
        if((typeof this.options) !== 'object')
            throw new ReferenceError("参数对象异常");
        var config = $.extend({}, HTTP_OPTION_DEFAULT, this.options);
        if(typeof url === "string") config.url = url;
        var data = config.data;
        $.ajax({
            url : config.url,
            type: config.method,
            data: data,
            cache: false,
            traditional: true,
            dataType: config.responseType,
            success: function (rel, textStatus) {
                if(textStatus === "success"){
                    if(config.responseType==='json')
                        try {
                            if (rel.WeJudgeError === undefined) {
                                config.success(rel);
                            } else {
                                if (!rel.WeJudgeError) {
                                    config.success(rel);
                                } else {
                                    var res = config.error(rel, rel.errmsg);
                                    if (res !== false) {
                                        if (rel.errcode === 1010) {
                                            wejudge.global.login();
                                        } else if (rel.errcode === 3010) {
                                            wejudge.global.login('education');
                                        } else if (rel.errcode === 5010) {
                                            wejudge.global.login('contest');
                                        }
                                    }
                                }
                            }
                        }catch (ex){
                            config.error(null, "Restful API应答处理错误");
                            console.trace();
                            console.log("[RESTful]Restful API应答处理错误; 错误内容：" + textStatus);
                            console.log(ex);
                        }
                    else
                        config.success(rel);
                }else{
                    config.error(null, "请求时发生错误(" + textStatus + ")");
                    console.trace();
                    console.log("[RESTful]请求时发生错误; 错误内容：" + textStatus);
                }
            },
            error: function (xhr, err) {
                config.error(null, "请求时发生错误(" + err + ")");
                console.trace();
                console.log("[RESTful]请求时发生错误; 错误内容：" + err);
            }
        });
        var cnzz = (function (url) {
            return function () {
                if(!window._czc) return;
                try {
                    window._czc.push(["_trackPageview", url, window.location.href]);
                } catch (ex) {

                }
            }
        })(config.url);
        setTimeout(cnzz, 500);

    },

    upload: function (url) {
        if((typeof this.options) !== 'object')
            throw new ReferenceError("参数对象异常");
        if (!(window.File && window.FileReader && window.FileList && window.Blob)){
            return false;
        }
        var option = $.extend({}, UPLOAD_OPTION_DEFAULT, this.options);
        if(typeof url === "string") config.url = url;
        var xhr = new XMLHttpRequest();
        xhr.upload.addEventListener("progress", function (evt) {
            if (evt.lengthComputable) {
                var percentComplete = Math.round(evt.loaded * 100 / evt.total);
                option.progress(percentComplete, evt.loaded, evt.total);
            }
            else {
                option.progress(0, 0, 0);
            }
        }, false);
        xhr.addEventListener("load", function (evt) {
            if(option.responseType === 'json'){
                try {
                    var result = JSON.parse(evt.target.responseText);

                }catch(ex){
                    option.error("解析API响应文本错误(" + ex + ")" );
                    console.log("[RESTful]解析API响应文本错误; 错误内容：" + ex);
                }
                if (result.WeJudgeError === undefined) {
                    option.success(result);
                }else{
                    if(!result.WeJudgeError) {
                        option.success(result);
                    }else{
                        option.error(result.errmsg);
                    }
                }
            }else{
                option.success(evt.target.responseText);
            }

        }, false);
        xhr.addEventListener("error", function () {
            option.error();
        }, false);
        xhr.addEventListener("abort", function () {
            option.abort();
        }, false);
        xhr.open("POST", option.url);
        xhr.setRequestHeader("X-CSRFtoken", window.csrf_token);
        xhr.send(option.formdata);
        return xhr;
    },
    submit_form: function (forms) {
        this.options.data = $(forms).serialize();
        this.options.method = $(forms).attr('method');
        this.call();
    }
};

var HTTP_OPTION_DEFAULT = {
    csrf: "",
    url: '',                                //请求的url
    data: null,                             //请求的数据（QueryString）
    method: 'GET',                          //请求模式
    responseType: 'json',                   //设置jQuery的响应回调数据格式，默认为text，仅支持text和json的处理
    in_modal: false,                        //在modal框内发起的请求
    success:function(entity){},             //成功，然后返回请求体（或者解析好的json）
    error:function(entity, msg){}           //失败，msg 存在的话为HTTP错误的原因，否则为程序的错误
};
var UPLOAD_OPTION_DEFAULT = {
    url: '',                                        //请求的url
    formdata: "",                                   //上传的表单
    responseType: 'text',                           //设置jQuery的响应回调数据格式，默认为text，仅支持text和json的处理
    success:function(data){},                       //请求成功后执行，返回响应体
    error: function (msg) {},                       //请求失败，返回消息
    abort: function () {},                          //用户终止，返回消息
    progress: function (perc, loaded, total) {}     //上传进度
};

// Hook
if (!Object.create) {
    Object.create = function (o) {
        function F() {}
        F.prototype = o;
        return new F();
    };
}
