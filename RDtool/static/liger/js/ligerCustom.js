$(document).ready(function () {
    $.getJSON(
    	"/clusters",
        function (json) {
	        window['t'] = $("#tree1").ligerTree({
	               nodeDraggable: false,
	               data: json,
	               idFieldName: "id",
	               parentIDFieldName: "pid"
	            });
         });
         manager = $("#tree1").ligerGetTreeManager();
     

    
    $.getJSON("/loadInfo", function(data) {
       
        window.cmds= data.comments;
        $.each(data.comments, function(i, item) {
        	//[{u'GetNodeEvents': [u'Node ID', u'Tenant ID']}, {u'GetTenantLbSetting': [u'Tenant ID']}]
            $("#command").append(
            		"<option  >" + item.command + "</option>"
                 );             
        });
        });
	$('#runtest').click(function(d){
		
		d.preventDefault();
		alert("in");
		var anArray = ['one','two','three'];
		var trHtml = '<tr><td>add1</td><td><button onclick="deltr(this)">del</button></td></tr>'
			addTr("restable", trHtml);
	

	});
	$('#run').click(function(e) {
		
    	timeIndex = 0;
        e.preventDefault();
        
		setTime();
    	times = setInterval(setTime, 1000);
    	
    	var cluster = getDatas();
    	if(cluster.length == 0){alert("Please Select Cluster!!");clearInterval(times);return false};
    	var command=document.getElementById('command').value;
    	if(command == "Select command"){alert("Please Select Command !!");clearInterval(times);return false};
    	var  param ={};
    	var flag = 0;
    	console.log(param0);
    	$.each(param0, function(j,para) {
    			param[para] = $.trim(document.getElementById(para).value);	
    					if(param[para] == ""){
    						alert("Please input "+ para);
    						flag =1;
    						return false
    						};
    			});
    	
    	if(flag == 1){
    		clearInterval(times);    	
    		return false;
    	}
    	
    	var prompte=document.getElementById('history').value;
    	var json = {
    			"cluster": cluster,
    			"command": command,
    			"param": param,
    			"prompte":prompte
    		
    			}; 
    	
       	console.log(json);
       	
        $(this)
            .removeClass('btn-primary')
            .addClass('btn-danger disabled') // with *disabled* I'm sure that the button is not clickable
            .attr('disabled',"true")
            .text('WAIT');

        $("#restable>tbody").html("");
        $.get(yourApp.contaUrl,{'cmd':JSON.stringify(json)}, function(jsondata) {
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


function checkinput(){  
	var cluster = getDatas();
	var command=document.getElementById('command').value; 
   	if (command == "Select command"){
		alert("Please Select Command !!");
		return false;
	}else if(cluster.length == 0){
		alert("Please Select Cluster !!");
		return false;
	}else{
		return true;
	};  
         
}  
var getManager = (function () {
    var manager = null;
    return function doGet() {
   	       if (!manager) {
               manager = $("#tree1").ligerGetTreeManager();
           }
	return manager;
 }
   })();

function stoptime(times){
	 clearInterval(times);
     $('#run')
        .removeClass('btn-danger disabled')
        .addClass('btn-primary')
        .removeAttr("disabled")
        .text('Run');
	
	
}
function setparam(){
    	var sec = document.getElementById('command').value;
    	$("#param").html("");
    	$("#help").html("");
    	window.param0=[]
    	$.each(cmds, function(i, item) {
    		if(item.command == sec){
    			$("#help").append(" <label style='color:red;font-size:14px'>" + item.help + "</label>");
    			$.each(item.param, function(j,para) {
    				param0.push(para);
    				$("#param").append(
    						" <label class='control-label' style='font-size:14px'>" + para + "</label> <div class='controls'><input type='text' style='font-size:14px' placeholder='Type something…'  id='" + para + "' name='subdomain' value='' /></div><br \> "
    						
    						);
    				
    			});
    		}
    	});
    };

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


    
function getDatas(){
	 if(manager){
//		 alert(1);
	 }
	 var nodes =getManager().getChecked();
	 var text=[];
	 for(var i=0;i<nodes.length;i++){
		if(!nodes[i].data.bgroup) 
			text.push(nodes[i].data.ip);
	 }
	// alert(text.join(","));
	return text;
 }

 function addTr(tab1, trHtml){
	var $tr=$("#" + tab1 + ">tbody");
	//$tr.html("");
	//$("#restable>tbody").html("");
	$tr.append(trHtml);
};
