function addwin(mytitle,urls)
{
  $('#mywindows').dialog({
    title: mytitle,
    width: 1024,
    height: 876,
    closed: false,
    cache: false,
    href:urls,
    maximizable:true,
    inline:false,
    modal:false
  });
}

function createwin(mytitle,urls)
{
  var str='title=yes,menubar=no,toolbar=no, status=no,scrollbars=yes';
  var newWin = window.open('','',str);
  newWin.document.write('<body scroll="no" style="margin: 0px;padding: 0px;border:0px;overflow:hidden;"><iframe style="margin: 0px;padding: 0px;border: 0px;width:100%;height:100%" src="' + urls + '"></iframe></body>');
  setTimeout(function(){newWin.document.title=mytitle;},100);
}

function createFrame(url) {
  var s = '<iframe scrolling="auto" frameborder="0"  src="' + url + '" style="width:100%;height:100%;"></iframe>';
  return s;
}
