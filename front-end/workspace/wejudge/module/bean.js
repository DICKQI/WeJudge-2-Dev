/**
 * Created by lancelrq on 2017/6/14.
 */

module.exports = WeJudgeBeanFactory();

function WeJudgeBeanFactory() {
    var BeanFactory = function () {
        return new BeanFactory.fn.init();
    };
    BeanFactory.fn = BeanFactory.prototype = {
        beansList: {},
        init: function () {

        },
        register: function(bean_name, creator){
            if(!this.beansList.hasOwnProperty(bean_name)){
                this.beansList[bean_name] = creator();
            }else{
                console.log("WeJudgeBeanFactory: `" + bean_name + "` already exists.")
            }
        },
        getBean(bean_name){
            if(this.beansList.hasOwnProperty(bean_name)) {
                return this.beansList[bean_name];
            }else{
                console.log("WeJudgeBeanFactory: No object named `" + bean_name + "`.")
            }
        }
    };
    BeanFactory.fn.init.prototype = BeanFactory.fn;
    return BeanFactory();
}