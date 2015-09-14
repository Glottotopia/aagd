
// function modfield(id,field,value){
//     modtrans(id,value)
// }


function modtrans(id,value){
    field='translatedsentence'
//     alert(id)
//     alert(field)
//     alert(value)
    host = "/mod";  
    url = host+'/set/'+id+'/'+field+'/'+value ;
    $.ajax({
    dataType: "json",
    url: url, 
    success: function (o) { 
	    msg = o.msg
	    status = o.status  	    
	    if (status == 'success'){ 		
		$("#trs_"+id).replaceWith('<span class="translatedsentence" id="trs_'+id+'" style="background:#7f7;border:4px double green">'+value+'</span>')
	    }
	    if (status == 'failure'){ 
		$("#trs_"+id).attr('background','green')
	    }
	},
    });
}
 


function addfield(id,field,value){
    host = "/mod";  
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
		valueidspan = document.createElement('span'); 
		valueidspan.setAttribute('id',id+field+value)
		valueidspan.appendChild(document.createTextNode(value));
		valuespan.appendChild(valueidspan)
		
		select = document.createElement('select')
		o1=document.createElement('option')
		o1.appendChild(document.createTextNode('---'))
		o2=document.createElement('option')
		o2.appendChild(document.createTextNode('delete'))
		o3=document.createElement('option')
		o3.appendChild(document.createTextNode('exemplar'))
		 
		select.appendChild(o1)
		select.appendChild(o2)
// 		select.appendChild(o3)
		select.setAttribute('onChange','deletefield("'+id+'","'+field+'","'+value+'")')
		valuespan.appendChild(select)
		
// 		closerspan = document.createElement('span');		
// 		a = document.createElement('a');
// 		a.appendChild(document.createTextNode("X"))
// 		a.setAttribute('href','#');
// 		clickstring = "deletefield('"+id+"','"+field+"','"+value+"');" 
// 		a.setAttribute('onClick',clickstring);		
// 		closerspan.appendChild(a);
// 		valuespan.appendChild(closerspan);
		
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


function deletefield(id,field,value){
    host = "/mod";
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
		cid = "callbackmsg"+id  
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

function setFlag(id,value){
    host = "/mod";  
    url = host+'/flag/'+id+'/'+value;
    if (value==false){
	color='green';
    }
    if (value==true){
	color='red';
    } 
    $.ajax({
    dataType: "json",
    url: url, 
    success: function (o) {  
	    status = o.status  
	    if (status == 'success'){
		img = document.getElementById('flag'+id)
		parent = img.parentNode
		parent.removeChild(img)
		newimg = document.createElement('img')
		newimg.setAttribute('src','../img/'+color+'flag.png') 
		newimg.setAttribute('id','flag'+id) 
		newimg.setAttribute('onclick','setFlag("'+id+'",' +!value+')')  
		newimg.setAttribute('width','32px')  
		parent.appendChild(newimg)
	    } 
	    else{
		    alert(o.msg)
	    }
	},
    });
}



// ondblclick="$(this).replaceWith($('<form ><div><input type=\'text\' value=\' + this.innerHTML + '\'></input	><button type=\'submit\'>test</button></div>  </form>'));alert(123)"
