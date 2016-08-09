$(document).ready(function () {

	$('#run').click(function(e) {
		
    	timeIndex = 0;
        e.preventDefault();
        
		setTime();
    	times = setInterval(setTime, 1000);
    	var pingname=document.getElementById('pingname').value;
    		pingname = $.trim(pingname)
    	if(pingname.length == 0){alert("Please input hostname or ip address !!");clearInterval(times);return false};
    	if(pingname.split(" ").length > 1 || pingname.split(".").length <3 || pingname.split(".").length > 4){alert("hostname or ip address Error!!");clearInterval(times);return false};
    	var pingn = document.getElementById('pingn').value;
    		pingn = $.trim(pingn)
    		pingn = parseInt(pingn)
    	if (isNaN(pingn)){
    		alert("Please input the ping times. !!");
    		clearInterval(times);
    		return false
    	}else if (pingn > 50){
    		alert("Please input the num le 50 !!");
    		clearInterval(times);
    		return false
    	};
    	var port = document.getElementById('port').value;
		port = $.trim(port)
		port = parseInt(port)
		if (isNaN(port)){
			alert("Please input the ping Port. !!");
			clearInterval(times);
			return false
		}else if (port > 65535){
			alert("Please input the num le 65535 !!");
			clearInterval(times);
			return false
		};
    	var prompte=document.getElementById('history').value;
    	var json = {
    			"pingname": pingname,
    			"pingn": pingn,
    			"port": port,
    			"prompte":prompte
    		
    			}; 
    	
       	console.log(json);
       	
        $(this)
            .removeClass('btn-primary')
            .addClass('btn-danger disabled') // with *disabled* I'm sure that the button is not clickable
            .attr('disabled',"true")
            .text('WAIT');

        $("#restable>tbody").html("");
        $.get("/runping/",{'cmd':JSON.stringify(json)}, function(jsondata) {
       
        	 console.log(jsondata);
		     var jsonObj = JSON.parse(jsondata);
             var le = jsonObj.length;
             var newhash;
             if (le == 2 ){
                // request hash data
            	newhash=jsonObj[1];
    			var d=0;
    			for (var i = 0; i < jsonObj[0].length; i++){
    				var confirm_s = "cmd: " + jsonObj[0][i]["cmd"] + "\n";
    					confirm_s += "Status: " + jsonObj[0][i]["status"] + "\n";
    					confirm_s += "Datetime: " + jsonObj[0][i]["time"] + "\n";
    					confirm_s += "Do you wan used the histroy?\n";
    				if (prompte == "Prompte"){
    					var  con = confirm(confirm_s);
    				}else{
    					var con =true;
    				};
    				
    				var   h= jsonObj[0][i]["hash"];
    				if (con){
    					if (jsonObj[0][i]["status"] == "success"){
    						var trHtml='<tr class="success">'
    						
    					}else if (jsonObj[0][i]["status"] == "failed"){
    						var trHtml='<tr class="danger">'
    						
    					}else {
    						var trHtml='<tr class="warning">'
    					};
    					
                 		trHtml +="<td >" + d ;
             			trHtml += "</td><td>" + jsonObj[0][i]["cmd"];
             			trHtml += "</td><td ><a target='_blank' href='http://waps-20/getresult2/?hash=" + h + "'>" + h;
             			trHtml += "</a></td><td >" + jsonObj[0][i]["status"];
             			trHtml +="</td></tr>";
             			addTr("restable", trHtml);
    				}else{
    					newhash.push(h);
    				}
    			}
				var  url="/getresult/";
				console.log(newhash);
				if (newhash.length > 0 ){
					$.get("/submit/",{'hash':JSON.stringify(newhash)}, function(res0){
						if (res0 =="ok"){
						for (var i = 0; i < newhash.length; i++){
								$.get(url,{'hash':newhash[i]}, function(res) {
									console.log(res);
									d = d +1;
									var jsonObj2 = JSON.parse(res);
									
									if (jsonObj2.status == "success"){
										var trHtml='<tr class="success">'
										
									}else if (jsonObj2.status == "failed"){
										var trHtml='<tr class="danger">'
										
									}else {
										var trHtml='<tr class="warning">'
									};
									
				             		trHtml +="<td >" + d ;
				         			trHtml += "</td><td>" + jsonObj2.cmd;
				         			trHtml += "</td><td ><a target='_blank' href='http://waps-20/getresult2/?hash=" + jsonObj2.hash + "'>" + jsonObj2.hash;
				         			trHtml += "</a></td><td >" + jsonObj2.status;
				         			trHtml +="</td></tr>";
				         			addTr("restable", trHtml);
									//alert(status);
									if(d == newhash.length){
										 alert("Run Done!");
										 stoptime(times);
										 
									};
								});
						}; // for end
						}else{
							var s = "ERROR:  " + res0;
							 alert(s);
							 stoptime(times);
						};
					}); 
					/*
					
					*/
				}else{
					 alert("Run Done!");
					 stoptime(times);
				}
			 }else{
				var i =0
				var sub_cmd = jsonObj[i];
          		var trHtml="<tr align='center'><td >" + i ;
     			trHtml += "</td><td >" + sub_cmd.cmd;
     			trHtml += "</td><td >" + sub_cmd.hash;
     			trHtml += "</td><td >" + "Not Run";
     			trHtml += "</td><td >" + jsonObj[1];
     			trHtml +="</td></tr>"; 
     			addTr("restable", trHtml);
			    alert("Run Error!");
			    stoptime(times);
			    
			 };
        });
        
       
             //window.location.href ="/fcclient/";
             //parent.window.location.reload(true);               


        
	}); //click end
	


});



function stoptime(times){
	 clearInterval(times);
     $('#run')
        .removeClass('btn-danger disabled')
        .addClass('btn-primary')
        .removeAttr("disabled")
        .text('Run');
	
	
}


//define my self
var yourApp = {
        contaUrl: "/runcommand/"
    };
timeIndex = 0;
function setTime(){
 
    	var hour = parseInt(timeIndex / 3600);   
    	var minutes = parseInt((timeIndex % 3600) / 60); 
    	var seconds = parseInt(timeIndex % 60);    
    	hour = hour < 10 ? "0" + hour : hour;
    	minutes = minutes < 10 ? "0" + minutes : minutes;
    	seconds = seconds < 10 ? "0" + seconds : seconds;
    	$("#showTime").val(hour + ":" + minutes + ":" + seconds);
    	timeIndex++;
};

function addTr(tab1, trHtml){
	var $tr=$("#" + tab1 + ">tbody");
	$tr.append(trHtml);
};