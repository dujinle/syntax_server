function onload(action,param,cb) {

	console.log("start onload data......");
	$.ajax({
		async:false,
		url: '/' + action,
		type:"post",
		data:JSON.stringify(param),
		dataType:"text",
		success:function(data){
			obj = JSON.parse(data);
			cb(obj);
		},
		error:function(data){
			console.log(data);
		}
	});
}

function get_table(table_name,key){
	onload("readtable",{"tablename":table_name,"header_name":key},function(data){

		var dot = data.result.dot;
		var keys = data.result.keys;
		//var image = Viz(dot, { format: "png-image-element" });
		var result = Viz(dot,{engine:"dot"});
		var canvasOne = document.getElementById("canvasOne");
		var table_info = document.getElementById("table_info");
		var table_list = document.getElementById("table_list");
		var graph = document.getElementById("graph");
		document.removeEventListener('DOMMouseScroll',scrollFunc);
		document.removeEventListener("load", windowLoadHandler);
		window.onmousewheel=document.onmousewheel=null;
		var table_list_html = "<li class=\"header\">数据头</li>";
		for(var i = 0;i < keys.length;i++){
			var item = keys[i];
			table_list_html = table_list_html + "<li><a href=\"javascript:void(0)\" onclick=\"get_table('" + table_name + "','" + item + "')\">" + item + "</a></li>"
		}
		table_list.innerHTML = table_list_html;
		table_info.style.display = "";
		canvasOne.style.display = "none";
		graph.innerHTML = result;
	});
}

function into_words(tablename,words){
	var ev = window.event;
	var mousePos = mousePosition(ev);
	console.log(mousePos);
	$('#white_content').css( { position : 'absolute', top : mousePos.y, left : mousePos.x } ).show();
	$('#black_overlay').show();
	var param = {
		tablename:tablename,
		words:words.split(':')[0]
	};
	console.log(JSON.stringify(param));
	var obj = null;
	$.ajax({
		async:false,
		url: '/getitem',
		type:"post",
		data:JSON.stringify(param),
		dataType:"text",
		success:function(data){
			console.log(data);
			obj = JSON.parse(data);
		},
		error:function(data){
			console.log(data);
		}
	});
	if(!! obj.result){
		document.getElementById('text1').value = JSON.stringify(obj.result,null,2);
	}
}
function del_item(){
	var tablename = document.title;
	console.log("del item start......" + tablename);
	var pa = JSON.parse(document.getElementById('text1').value);
	var pa_json = null;
	for(item in pa){
		pa_json = pa[item];
	}
	var param = {
		"tablename":tablename,
		"word":pa_json.str
	};
	console.log(JSON.stringify(param));
	var obj = null;
	$.ajax({
		async:false,
		url: 'delitem',
		type:"post",
		data:JSON.stringify(param),
		dataType:"text",
		success:function(data){
			console.log(data);
			on_close();
		},
		error:function(data){
			console.log(data);
		}
	});
}
function add_item(){
	var tablename = document.title;
	console.log("add item start......" + tablename);
	var pa = JSON.parse(document.getElementById('text1').value);
	var pa_json = null;
	for(item in pa){
		pa_json = pa[item];
	}
	var text2 = JSON.parse(document.getElementById('text2').value)
	var param = {
		"tablename":tablename,
		"parent":pa_json.str,
		"item":text2
	};
	console.log(JSON.stringify(param));
	var obj = null;
	$.ajax({
		async:false,
		url: 'additem',
		type:"post",
		data:JSON.stringify(param),
		dataType:"text",
		success:function(data){
			console.log(data);
			on_close();
		},
		error:function(data){
			console.log(data);
		}
	});
}
