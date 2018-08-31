function onload(action,param,cb) {

	console.log("start onload data......");
	$.ajax({
		async:false,
		url: 'http://10.10.1.126:28089/' + action,
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
		url: 'http://10.10.1.126:28089/getitem',
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
		url: 'http://10.10.1.126:28089/delitem',
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
		url: 'http://10.10.1.126:28089/additem',
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
