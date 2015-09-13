//
// MoinMoin commonly used JavaScript functions
//
// Changed: 
// * added function addAccessKeys(), addAccessKeyDescription()
// * added function addAccessKeys() to load()
// * provided name attrib for guiEdit link
//
// Copyrights:
// addAccessKeys(), addAccessKeyDescription() copyright 2007 by Oliver Siemoneit
// license: GNU GPL, see COPYING for details. 	


window.onload = function() {
    document.getElementById('Exemplars	').onclick = alert(123);
};




// We keep here the state of the search box
searchIsDisabled = false;

function searchChange(e) {
    // Update search buttons status according to search box content.
    // Ignore empty or whitespace search term.
    var value = e.value.replace(/\s+/, '');
    if (value == '' || searchIsDisabled) { 
        searchSetDisabled(true);
    } else {
        searchSetDisabled(false);
    }
}

function searchSetDisabled(flag) {
    // Enable or disable search
    document.getElementById('fullsearch').disabled = flag;
    document.getElementById('titlesearch').disabled = flag;
}

function searchFocus(e) {
    // Update search input content on focus
    if (e.value == search_hint) {
        e.value = '';
        e.className = '';
        searchIsDisabled = false;
    }
}

function searchBlur(e) {
    // Update search input content on blur
    if (e.value == '') {
        e.value = search_hint;
        e.className = 'disabled';
        searchIsDisabled = true;
    }
}

function actionsMenuInit(title) {
    // Initialize action menu
    for (i = 0; i < document.forms.length; i++) {
        var form = document.forms[i];
        if (form.className == 'actionsmenu') {
            // Check if this form needs update
            var div = form.getElementsByTagName('div')[0];
            var label = div.getElementsByTagName('label')[0];
            if (label) {
                // This is the first time: remove label and do buton.
                div.removeChild(label);
                var dobutton = div.getElementsByTagName('input')[0];
                div.removeChild(dobutton);
                // and add menu title
                var select = div.getElementsByTagName('select')[0];
                var item = document.createElement('option');
                item.appendChild(document.createTextNode(title));
                item.value = 'show';
                select.insertBefore(item, select.options[0]);
                select.selectedIndex = 0;
            }
        }
    }
}

// use this instead of assigning to window.onload directly:
function addLoadEvent(func) {
  // alert("addLoadEvent " + func)
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    }
  }
}

function can_use_gui_editor() {
    var sAgent = navigator.userAgent.toLowerCase() ;

    // Internet Explorer
    if ( sAgent.indexOf("msie") != -1 && sAgent.indexOf("mac") == -1 && sAgent.indexOf("opera") == -1 )
    {   
        var sBrowserVersion = navigator.appVersion.match(/MSIE (.\..)/)[1] ;
        return ( sBrowserVersion >= 5.5 ) ;
    }
    
    // Gecko
    if ( navigator.product == "Gecko" && navigator.productSub >= 20030210 )
        return true ;

    // Opera
    if ( this.EnableOpera )
    {   
        var aMatch = sAgent.match( /^opera\/(\d+\.\d+)/ ) ;
        if ( aMatch && aMatch[1] >= 9.0 )
            return true ;
    }
    
    // Safari
    if ( this.EnableSafari && sAgent.indexOf( 'safari' ) != -1 )
        return ( sAgent.match( /safari\/(\d+)/ )[1] >= 312 ) ;  // Build must be at least 312 (1.3)

    return false ;

}


function update_edit_links() {
    // Update editlink according if if the browser is compatible
    if (can_use_gui_editor() == false){
        //alert("update_edit_links: can't use gui editor");
        return;
    }
    var editlinks = document.getElementsByName("editlink");
    for (i = 0; i < editlinks.length; i++) {
        var link = editlinks[i];
        href = link.href.replace('editor=textonly','editor=guipossible');
        link.href = href;
        //alert("update_edit_links: modified to guipossible");
    }
}


function add_gui_editor_links() {
    // Add gui editor link after the text editor link
    
    // If the variable is not set or browser is not compatible, exit
    try {gui_editor_link_href}
    catch (e) {
        //alert("add_gui_editor_links: gui_editor_link_href not here");
        return
    }
    if (can_use_gui_editor() == false){
        //alert("add_gui_editor_links: can't use gui_editor");
        return;
    }
    var all = document.getElementsByName('texteditlink');
    for (i = 0; i < all.length; i++) {
        var textEditorLink = all[i];
        // Create a list item with a link
        var guiEditorLink = document.createElement('a');
        guiEditorLink.href = gui_editor_link_href;
	  guiEditorLink.name = 'guieditlink'; 
        var text = document.createTextNode(gui_editor_link_text);
        guiEditorLink.appendChild(text);
        var listItem = document.createElement('li')
        listItem.appendChild(guiEditorLink);
        // Insert in the editbar
        var editbar = textEditorLink.parentNode.parentNode
        var nextListItem = textEditorLink.parentNode.nextSibling;
        editbar.insertBefore(listItem, nextListItem);
        //alert("add_gui_editor_links: added gui editor link");
    }
}
 

function show_switch2gui() {
    // Show switch to gui editor link if the browser is compatible
    if (can_use_gui_editor() == false) return;
    
    var switch2gui = document.getElementById('switch2gui')
    if (switch2gui) {
        switch2gui.style.display = 'inline';
    }
}

function toggleComments() {
    // Toggle visibility of every div with class == *comment*
    var all = document.getElementsByTagName('*');
    for (i = 0; i < all.length; i++){
        el = all[i];
        if ( el.className.indexOf('comment') >= 0 ){
            if ( el.style.display != 'none' ) {
                el.style.display = 'none';
            } else {
                el.style.display = '';
            }
        }
    }
}

function addAccessKeys(){
    // Add 'accesskey=".."' attribute to the elments specified in var shortcut_list 
    for (i=0; i < shortcut_list.length; i++){
        // Split up the values which are stored like this:
        // Variant 1: (elementtype[name/id])#(elementname)=(accesskey)
        // Variant 2: (elementtype[name/id])#(elementname)=(accesskey)!(descriptiontext)
        var short1 = shortcut_list[i].split("#");
        var short2 = short1[1].split("=");
        var short3 = short2[1].split("!");
        var type = short1[0];
        var name = short2[0];
        var key = short3[0];
        if (short3.length > 1) {
            var desc = short3[1];
        }
        else {
            var desc = ""
        }
        //alert("type: " + type + " name: " + name + " key: " + key + " desc:" + desc);

        // Add keys
        if (type == "id") {
            var element = document.getElementById(name);
            if (element != null) {
                //alert("OK!!!!!!!!!! name:" + name + " element:" + element)
                var ak = document.createAttribute("accesskey");
                ak.nodeValue = key;
                element.setAttributeNode(ak);
                addAccessKeyDescription(document.getElementById('accesskeys'), key, name, desc);
            }
            else {
                //alert("ERROR!!!!!! type:" + type + " name:" + name +" not found")
            }
        }
        else {
            var elements = document.getElementsByName(name);
            for (j=0; j < elements.length; j++) {
                if (elements[j] != null) {
                    //alert("OK!!!!! name:" + name + " elements[" + j + "]:" + elements[j])
                    var ak = document.createAttribute("accesskey");
                    ak.nodeValue = key;
                    elements[j].setAttributeNode(ak);
                    addAccessKeyDescription(document.getElementById('accesskeys'), key, name, desc);
                }
                else {
                    //alert("ERROR!!!!!!!! type:" + type + " name:" + name +" not found")
                }
            }
        }
    }
}

function addAccessKeyDescription(div, key, name, desc){
    // If there is a 'div id="accesskeys"' in the page, add a list of available shortcuts so users get a clue
    // which keys to hit for a certain action
    if (div != null) {
        //alert("div is there");
        key_list = document.getElementById('accesskey_list');
        if (key_list == null) {
            key_list = document.createElement("ul");
            div.appendChild(key_list);
            var id = document.createAttribute("id");
            id.nodeValue = "accesskey_list";
            key_list.setAttributeNode(id);
            //alert("Created ul keylist");
        }
        if (desc == ""){
            var text = document.createTextNode(key + " = " + name)
        }
        else {
            var text = document.createTextNode(key + " = " + desc)
        }
        key_list.appendChild(document.createElement("li")).appendChild(text);
    }
    else {
        //alert("No div");
    }
}

function load() {
    // Do not name this "onload", it does not work with IE :-)
    // TODO: create separate onload for each type of view and set the
    // correct function name in the html. 
    // e.g <body onlod='editor_onload()'>
    
    // Page view stuff
    update_edit_links();
    add_gui_editor_links();
    
    // Editor stuff
    show_switch2gui();

    addAccessKeys();
}


function before_unload(evt) {
    // TODO: Better to set this in the editor html, as it does not make
    // sense elsehwere.
    // confirmleaving is available when editing
    try {return confirmleaving();}
    catch (e) {}
}

// Initialize after loading the page
addLoadEvent(load)

// Catch before unloading the page
window.onbeforeunload = before_unload

