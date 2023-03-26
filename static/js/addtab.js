function createFrame(url) {
  var s = '<iframe scrolling="auto" frameborder="0"  src="' + url + '" style="width:100%;height:100%;"></iframe>';
  return s;
}

function addTab(title, url) {
  if ($('#tabs').tabs('exists', title))
{$('#tabs').tabs('select', title);
    var currTab = $('#tabs').tabs('getSelected');
    var url = $(currTab.panel('options').content).attr('src');
    if (url != undefined && currTab.panel('options').title != 'Home')
  {
      $('#tabs').tabs('update', { tab: currTab, options: { content: creaeFrame(url) } })
    }
  }
  else
{ var content = createFrame(url);
    $('#tabs').tabs('add', { title: title, content: content, closable: true });
  }
  tabClose(); }

function tabClose() {
  $(".tabs-inner").dblclick(function() {
    var subtitle = $(this).children(".tabs-closable").text();
    $('#tabs').tabs('close', subtitle);
  })
  $(".tabs-inner").bind('contextmenu', function(e) {
    $('#mm').menu('show', {
      left: e.pageX,
      top: e.pageY
    });
    var subtitle = $(this).children(".tabs-closable").text();
    $('#mm').data("currtab", subtitle);
    $('#tabs').tabs('select', subtitle);
    return false;
  });
}

function tabCloseEven() {
  $('#mm-tabupdate').click(function() {
    var currTab = $('#tabs').tabs('getSelected');
    var url = $(currTab.panel('options').content).attr('src');
    if (url != undefined && currTab.panel('options').title != 'Home') {
      $('#tabs').tabs('update', {
        tab: currTab,
        options: {
          content: createFrame(url)
        }
      })
    }
  })
  $('#mm-tabclose').click(function() {
    var currtab_title = $('#mm').data("currtab");
    $('#tabs').tabs('close', currtab_title);
  });
  $('#mm-tabcloseall').click(function() {
    $('.tabs-inner span').each(function(i, n) {
      var t = $(n).text();
      if(t != '主页') {
        $('#tabs').tabs('close', t);
      }
    });
  });
  $('#mm-tabcloseother').click(function() {
    var prevall = $('.tabs-selected').prevAll();
    var nextall = $('.tabs-selected').nextAll();
    if (prevall.length > 0) {
      prevall.each(function(i, n) {
        var t =  $(n).text();
        if (t != '主页' ) {
          $('#tabs').tabs('close', t);
        }
      });
    }
    if (nextall.length > 0) {
      nextall.each(function(i, n) {
        var t = $(n).text();
        if (t != '主页') {
          $('#tabs').tabs('close', t);
        }
      });
    }
    return false;
  });
  $('#mm-tabcloseright').click(function() {
    var nextall = $('.tabs-selected').nextAll();
    if (nextall.length == 0) { alert('后边没有啦!!!'); return false; }
    nextall.each(function(i, n) { var t =  $(n).text(); $('#tabs').tabs('close', t); }); return false;
  });
  $('#mm-tabcloseleft').click(function() {
    var prevall = $('.tabs-selected').prevAll();
    if (prevall.length == 0) { alert('到头了，前边没有啦!!!'); return false; }
    prevall.each(function(i, n) { var t =  $(n).text(); $('#tabs').tabs('close', t); }); return false; });
  $("#mm-exit").click(function() {
    $('#mm').menu('hide');
  });
}
