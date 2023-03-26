function changTheme(themeName) {
  var $easyuiTheme = $('#easyuiTheme');
  href = '/static/easyui/themes/' + themeName + '/easyui.css';
  $easyuiTheme.attr('href', href);
  var $iframe = $('iframe');
  if ($iframe.length > 0) {
    for (var i = 0; i < $iframe.length; i++) {
      var ifr = $iframe[i];
      $(ifr).contents().find('#easyuiTheme').attr('href', href)
    }
  }
  $.cookie('themeName', themeName, {
    expires: 7
  })
};
$(document).ready(function() {
  $(document).bind("contextmenu", function(e) {
    return false
  })
});
function setCookie(name, value) {
  var Days = 1; //此 cookie 将被保存 1 天
  var exp = new Date(); //new Date("December 31, 9998");
  exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
  document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}
function getCookie(name) {
  var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
  if (arr != null) return unescape(arr[2]);
  return null;
}

