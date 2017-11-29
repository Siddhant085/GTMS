$(document).ready(allocated);
function allocated(){
	data = {'status':'a'}
	$.ajax({
		url: "/load_proj_data",
		data:  JSON.stringify(data),
		type: "POST",
		contentType: 'application/json;charset=UTF-8',		
		success: load_allocated_proj,
		error: function(error) {
			console.log(error);
			$("#error").html(error.responseText)
		}
	});
}
function load_allocated_proj(data){
	loadProjectData(data, document.getElementById('allo_table'))
}
function waiting(){
	data = {'status':'w'}
	$.ajax({
		url: "/load_proj_data",
		data:  JSON.stringify(data),
		type: "POST",
		contentType: 'application/json;charset=UTF-8',		
		success: load_waiting_proj,
		error: function(error) {
			console.log(error);
			$("#error").html(error.responseText)
		}
	});
}
function load_waiting_proj(data){
	loadProjectData(data, document.getElementById('wait_table'))
}
function loadProjectData(data, tab){
	console.log(data)
	for(i=0; i<data.length; ++i){
		tr = document.createElement('tr')
		for (var j=0; j<7; ++j){
			td = document.createElement('td')
			a = document.createElement('a')
			a.href = "/project/title/"+data[i][0]
			a.appendChild(document.createTextNode(data[i][j]))
			td.appendChild(a)
			tr.appendChild(td)
		}
		
		tab.appendChild(tr)
	}
}

function search(){
	data1 = $("input[name='optradio']:checked").val()
	data2 = document.getElementById('str').value
	data = {'method':data1, 'text':data2}
	$.ajax({
		url: "/search_by",
		data:  JSON.stringify(data),
		type: "POST",
		contentType: 'application/json;charset=UTF-8',		
		success: update_success,
		error: function(error) {
			console.log(error);
			$("#error").html(error.responseText)
		}
	});
}

function update_success(text){
	// need to parse this text as json and accordingly update the search results in this function
	data = JSON.parse(text)
	
	res = document.getElementById('result')
	res.style.display = "block"
	d = document.getElementById('tab')
	for(var i=0; i<data.length; ++i){
		tr = document.createElement('tr')
		for (var j=0; j<7; ++j){
			td = document.createElement('td')
			td.appendChild(document.createTextNode(data[i][j]))
			tr.appendChild(td)
		}
		d.appendChild(tr)
	}
}

function add_project(){
	d1 = document.getElementById('tit').value
	d2 = document.getElementById('state').value
	d3 = document.getElementById('dist').value
	d4 = document.getElementById('cate').value
	d5 = document.getElementById('strt').value
	d6 = document.getElementById('end').value
	d7 = document.getElementById('desc').value
	data = {'title':d1, 'state':d2, 'district':d3, 'project_category':d4, 'bid_start_date':d5, 'bid_end_date':d6, 'project_desc':d7}
	$.ajax({
		url: "/addproject",
		data:  JSON.stringify(data),
		type: "POST",
		contentType: 'application/json;charset=UTF-8',		
		success: proj_added,
		error: function(error) {
			console.log(error);
			$("#error").html(error.responseText)
		}
	});	
}
function proj_added(data){
	alert("ADDED")
}