document.write("<script language=javascript src='/static/js/cardcheck.js'></script>");
$.extend($.fn.validatebox.defaults.rules, {    
  phoneNum: { //验证手机号   
    validator: function(value, param){ 
      return /^1[3-8]\d{9}$/.test(value);
    },    
    message: '请输入正确的手机号码。'   
  },
  telNum:{ //既验证手机号，又验证座机号
    validator: function(value, param){ 
      return /(^(0[0-9]{2,3}\-)?([2-9][0-9]{6,7})+(\-[0-9]{1,4})?$)|(^(()|(\d{3}\-))?(1[358]\d{9})$)/.test(value);
    },    
    message: '请输入正确的电话号码。' 
  },
  CNchar:{
    validator:function(value,param){
      return  /^[\u4e00-\u9fa5]{1,6}(·[\u4e00-\u9fa5]{1,6}){0,2}$/.test(value);
    },
    message:'请输入正确的汉字！'
  },
  idcheck:{
    validator:function(value,param){
      if (cardcheck(value)=== value){
        return value;
      }},
      message:'请输入正确的身份证号！' 
    }
  });
