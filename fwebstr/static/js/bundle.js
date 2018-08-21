function parse_data(data){
	var stc = data['stc'];
	var chart_more = document.getElementById('chart_more');
	var chart_more_array = new Array();
	for(var key in stc){
		item = stc[key];
		if(item['type'] == 'TIME'){
			var html_str = "<font color='red'>" + item['str'] + "</font>";
			data['seg_text'] = data['seg_text'].replace(item['str'],html_str);
			chart_more_array[0] = "<font color='red'>时间</font>";
		}else if(item['type'] == 'NUM'){
			var html_str = "<font color='blue'>" + item['str'] + "</font>";
			data['seg_text'] = data['seg_text'].replace(item['str'],html_str);
			chart_more_array[1] = "<font color='blue'>数字</font>";
		}else if(item['type'] == "NP"){
			var html_str = "<font color='green'>" + item['str'] + "</font>";
			data['seg_text'] = data['seg_text'].replace(item['str'],html_str);
			chart_more_array[2] = "<font color='green'>地点名词</font>";
		}
	}
	chart_more.innerHTML = chart_more_array.join(" ");
	return data;
}

function  nlp_process(){
	var text = document.getElementById('text').value;
	var data = {'text':text};
	$.ajax({
		type: "POST",
		url: "nlp_process",
		data: JSON.stringify(data),
		dataType: "text",
		success: function(data){
			var json_data = JSON.parse(data).result;
			var chart = document.getElementById('chart');
			json_data = parse_data(json_data);
			chart.innerHTML = json_data['seg_text'];
			console.log(json_data);
		}
	});
}
