var tablename='';  var schoolid=''; var bxlx='';
function reportable(node)
{ $("#cctree").tree({
  url : 'reportmenu?pid=0&power=1&bxlx=0',
  onClick : function(node) {
    if(node.id<=6){ var node = $('#cctree').tree('getSelected');
      if ($('#cctree').tree('isLeaf', node.target)) {
	$.ajax({ url : 'reportmenu?pid=' + node.id + '&power=1&bxlx='+bxlx, type : 'POST', success : function(jsontree) { $('#cctree').tree('append', { parent : node.target, data:jsontree }) } }) } if (node.state === 'open') { $('#cctree').tree('collapse', node.target); }
      else { $('#cctree').tree('expand', node.target); }}
    else{ addTab('教基'+node.id, 'jj'+node.id+'?schoolid='+schoolid+'&table='+node.id+'&tablename='+node.text); } } });}
function bl(item){ var tree = new Object(); tree.id = item.id; tree.text = item.text; if(item.id.length==12){tree.state = 'closed'}; tree.checked = 'false'; tree.attributes ={levels:item.level,url:'www.baidu.com'}; return tree; };
function jsonbl(data){ var easyTree = []; $.each(data,function(index,item){ easyTree[index] = bl(item); }); return easyTree;}
$(function(){ $('#cc').combotree({ url:"/main/regiontree?pid="+{{request.user}}+"&levels="+ {{request.user.last_name}}, panelWidth: 'auto', panelMaxHeight: 350, onShowPanel: function () {  $(this).combobox('panel').width("auto"); var width = $(this).combobox('panel').width(); if (width > 600) { $(this).combobox('panel').width("600"); } else if (width < 300) { $(this).combobox('panel').width("300"); } else {$(this).combobox('panel').width(width + 20); } }, loadFilter:function(data){ return jsonbl(data); }, onBeforeExpand:function(node) { $('#cc').combotree("tree").tree("options").url = "/main/regiontree?pid=" + node.id + "&levels="+node.attributes.levels; }, onSelect:function(node,target){ var tree = $(this).tree; var isLeaf = tree('isLeaf', node.target); if (!isLeaf) { $(this).tree('expand', node.target); $('#cc').combotree('clear'); } else {schoolid=node.id;bxlx=node.attributes.levels;reportable(node); } } }); });

