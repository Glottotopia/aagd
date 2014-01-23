
function addfield(id,field,value){
    host = "http://www.glottotopia.org/athagram/mod";  
    url = host+'/add/'+id+'/'+field+'/'+value ;
    $.ajax({
    dataType: "json",
    url: url, 
    success: function (o) { 
	    msg = o.msg
	    status = o.status  
	    
	    if (status == 'success'){
		tagcontainer = document.getElementById('tagcontainer'+id)
		div = document.createElement('div');
		div.setAttribute('class','tag');
		fieldspan = document.createElement('span');
		fieldspan.setAttribute('class','field');
		fieldspan.appendChild(document.createTextNode(field));
		valuespan = document.createElement('span');
		valuespan.setAttribute('class','value');
		valuespan.setAttribute('id',id+field+value)
		valuespan.appendChild(document.createTextNode(value));
		closerspan = document.createElement('span');
		a = document.createElement('a');
		a.appendChild(document.createTextNode("X"))
		a.setAttribute('href','#');
		clickstring = "deletefield('"+id+"','"+field+"','"+value+"');" 
		a.setAttribute('onClick',clickstring);
		closerspan.appendChild(a);
		valuespan.appendChild(closerspan);
		div.appendChild(fieldspan);
		div.appendChild(valuespan);
		tagcontainer.appendChild(div) 
	    }
	    if (status == 'failure'){
		cid = "callbackmsg"+id  
		document.getElementById(cid).innerHTML = msg
		document.getElementById(cid).setAttribute("class",status+ " callbackmsg")
		document.getElementById(cid).setAttribute("style",'')	
		$('#'+cid) 
	    }
	},
    });
}

// function addfield(id,field,value){
//     var callbacks = { 
// 	success : function (o) {
// 	    var msg;  
// 	    try {
// 		r = YAHOO.lang.JSON.parse(o.responseText);
// 		msg = r.msg
// 		status = r.status
// 	    }
// 	    catch (x) {
// 		alert("JSON Parse failed!");
// 		return;
// 	    }  
// 	    cid = "callbackmsg"+id 
// 	    if (status == 'success'){
// 		tagcontainer = document.getElementById('tagcontainer'+id)
// 		div = document.createElement('div');
// 		div.setAttribute('class','tag');
// 		fieldspan = document.createElement('span');
// 		fieldspan.setAttribute('class','field');
// 		fieldspan.appendChild(document.createTextNode(field));
// 		valuespan = document.createElement('span');
// 		valuespan.setAttribute('class','value');
// 		valuespan.setAttribute('id',id+field+value)
// 		valuespan.appendChild(document.createTextNode(value));
// 		closerspan = document.createElement('span');
// 		a = document.createElement('a');
// 		a.appendChild(document.createTextNode("X"))
// 		a.setAttribute('href','#');
// 		clickstring = "deletefield('"+id+"','"+field+"','"+value+"');" 
// 		a.setAttribute('onClick',clickstring);
// 		closerspan.appendChild(a);
// 		valuespan.appendChild(closerspan);
// 		div.appendChild(fieldspan);
// 		div.appendChild(valuespan);
// 		tagcontainer.appendChild(div) 
// 	    }
// 	    if (status == 'failure'){
// 		document.getElementById(cid).innerHTML = msg
// 		document.getElementById(cid).setAttribute("class",status+ " callbackmsg")
// 		document.getElementById(cid).setAttribute("style",'')	
// 		$('#'+cid).fadeOut(2500)
// 	    }
// 	},
// 	failure : function(o){
// 	    alert("connection error")
// 	}
//     };
//     // Make the call to the server for JSON data 
//     host = "http://www.glottotopia.org/athagram/mod";  
//     address = host+'/add/'+id+'/'+field+'/'+value 
//     YAHOO.util.Connect.asyncRequest('GET', address, callbacks);
// }
//  
function deletefield(id,field,value){
    host = "http://www.glottotopia.org/athagram/mod";  
    url = host+'/delete/'+id+'/'+field+'/'+value ;
    
    $.ajax({
    dataType: "json",
    url: url, 
    success: function (o) { 
	    msg = o.msg
	    status = o.status  
	    empty = o.empty
	    if (status == 'success'){
		hit = document.getElementById(id+field+value)
		if (empty){
		    hit.parentNode.parentNode.parentNode.removeChild(hit.parentNode.parentNode)
		}
		else{
		     hit.parentNode.removeChild(hit)
		}
	    }
	    if (status == 'failure'){
		document.getElementById(cid).innerHTML = msg
		document.getElementById(cid).setAttribute("class",status+ " callbackmsg")
		document.getElementById(cid).setAttribute("style",'')	
	    }
	},
    });
}

function hidealltagbags(){
     $('div[class="tagbag"]').hide('fast')
     $('div[class="tagbag"]').parent().attr('style','')
}

function toggleFacets(id){    
    $( "#"+ id ).toggle('fast') 
}

function toggleBox(id){
    $("#"+id).toggle('fast')
}



