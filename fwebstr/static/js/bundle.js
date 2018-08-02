function parse_data(data){
	var TimeParse = data['TimeParse'];
	var str = TimeParse['strs'].join('');
	var html_str = "<font color='red'>" + str + "</font>";
	data['seg_text'] = data['seg_text'].replace(str,html_str);
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
