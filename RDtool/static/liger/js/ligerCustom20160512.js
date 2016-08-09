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
       // $("#info").html("");//清空info内容
        cmds= data.comments;
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
    	var json = {
    			"cluster": ["Bjbprdapp01"],
    			"command": "GetTenantEvents",
    			"param": {"name":"test"},
    			}; 
		$.each(anArray, function(k,v) {
			var s = "key:" + k +"   value:"+v;
			alert(s);
	        $.get(yourApp.contaUrl,{'cmd':JSON.stringify(json)}, function(json) {
	             alert(s + "I have finished counting");
	        });  
		});
			
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
    	var flag = false;
    	$.each(cmds, function(i, item) {
    		if(item.command == command){
    			$.each(item.param, function(j,para) {
    					param[para] = document.getElementById(para).value;
    					
    					if(param[para] == ""){
    						alert("Please input "+ para);
    						flag=true;
    						return false
    						};
    			});
    		}
    	});
    	if(flag){clearInterval(times);return false}
    	var json = {
    			"cluster": cluster,
    			"command": command,
    			"param": param
    			}; 
    	
       	console.log(json);
       	
        $(this)
            .removeClass('btn-primary')
            .addClass('btn-danger disabled') // with *disabled* I'm sure that the button is not clickable
            .attr('disabled',"true")
            .text('WAIT');

        $.get(yourApp.contaUrl,{'cmd':JSON.stringify(json)}, function(json) {
        	 clearInterval(times);
		     $('#run')
		        .removeClass('btn-danger disabled')
	            .addClass('btn-primary')
	            .removeAttr("disabled")
	            .text('Run');

             alert("I have finished counting");
             alert(json);
             
             //window.location.href ="/fcclient/";
             //parent.window.location.reload(true);               


        });
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
function setparam(){
    	var sec = document.getElementById('command').value;
    	$("#param").html("");
    	$("#help").html("");
    	$.each(cmds, function(i, item) {
    		if(item.command == sec){
    			$("#help").append(" <label style='color:red;'>" + item.help + "</label>");
    			$.each(item.param, function(j,para) {
    				$("#param").append(
    						" <label >" + para + "</label> <input type='text' placeholder='Type something…'  id='" + para + "' name='subdomain' value='' /><br> "
    						
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

