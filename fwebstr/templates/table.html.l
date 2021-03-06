﻿<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{tablename}}</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">
<style>
/* input styles */
textarea, 

textarea {
	width: 370px;
	height: 200px;
}

/* fallback placeholder */
.placeholder {
	color: #bbb;
}
/* webkit placeholder */
::-webkit-input-placeholder {
	color: #bbb;
}
/* moz placeholder */
:-moz-placeholder {
	color: #bbb;
}

<style type="text/css">
	.black_overlay{
		display:none;
		position:absolute;
		top:0%;
		left:0%;
		width:100%;
		height:100%;
		background-color:black;
		z-index:1001;
		-moz-opacity:0.8;
		opacity:.80;
		filter:alpha(opacity=80);
	}
	.white_content{
		display:none;
		position:absolute;
		top:25%;
		left:25%;
		width:50%;
		height:60%;
		padding:16px;
		border:3px solid orange;
		background-color:white;
		z-index:1002;
		overflow:auto;
	}
</style>

</style>
</head>
<body>
<script src="{{ static_url('js/viz.js') }}"></script>
<script src="{{ static_url('js/ajax-funcs.js') }}"></script>
<script src="http://code.jquery.com/jquery-2.1.1.min.js" integrity="sha256-h0cGsrExGgcZtSZ/fRz4AwV+Nn6Urh/3v3jFRQ0w9dQ=" crossorigin="anonymous"></script>

<!--隐藏的 -->
<div id="white_content" display="none" class="white_content">
	<a href="javascript:void(0)" onclick="on_close()">Close</a>
	<form class="form" action="#">
		<p><textarea id="text1" readonly ></textarea></p>
		<p><textarea id="text2"></textarea></p>
		<p>
			<input name="删除" type="button" id="Button3" onclick="del_item()" value="删除" />
			<input name="提交" type="button" id="Button4" onclick="add_item()" value="添加" />
		</p>
	</form>
</div>
<div id="black_overlay" display="none" class="black_overlay"></div>

<script type="text/javascript">
	var param = {
		"tablename":"{{tablename}}"
	};
	onload("readtable",param,function(data){
		var dot = data.result.dot;
		var result = Viz(dot,{ engine: "dot" });
		console.log(result);
		document.body.innerHTML += result;
		var test = document.getElementsByTagName("text");
		for(i = 0;i < test.length;i++){
			var value = test[i].innerHTML;
			if (value == "child" || value == "self"){
				continue;
			}
			test[i].innerHTML = "<a href='javascript:void(0)' onclick='into_words(\"{{tablename}}\",\""+ value +"\")'>" + value + "</a>";
			console.log(test[i].innerHTML);
		}
	});
	function on_close(){
		document.getElementById('black_overlay').style.display='none';
		document.getElementById('white_content').style.display='none';
	}
	function mousePosition(ev){
		if(ev.pageX || ev.pageY){//firefox、chrome等浏览器
			return {x:ev.pageX,y:ev.pageY};
		}
		return {// IE浏览器
			x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,
			y:ev.clientY + document.body.scrollTop - document.body.clientTop
		}
	}
</script>
</body>
</html>
