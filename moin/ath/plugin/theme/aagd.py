# -*- coding: utf-8 -*-
"""
    MoinMoin - modern theme

    @copyright: 2003-2005 Nir Soffer, Thomas Waldmann
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase
from MoinMoin import wikiutil
from MoinMoin.Page import Page

class Theme(ThemeBase):

    name = "aagd"

    _ = lambda x: x     # We don't have gettext at this moment, so we fake it
 
    del _
    def header(self, d, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),
            
            """ <script src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
	 <div class="navbar navbar-inverse" role="navigation"> 
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="http://www.glottotopia.org/aagd">Alaskan Athabascan Grammar Database</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="http://www.glottotopia.org/solr/aagd/browse">Browse</a></li>
            <li><a href="http://www.glottotopia.org/aagd/About">About</a></li>
            <li><a href="http://www.glottotopia.org/aagd/Contact">Contact</a></li>
            <li><a href="http://www.glottotopia.org/aagd/Languages">Languages</a></li>
            <li><a href="http://www.glottotopia.org/aagd/Glossary">Glossary</a></li>
            <li><a href="http://www.glottotopia.org/aagd/Assumptions">Assumptions</a></li> 
            <li><a href="http://www.glottotopia.org/aagd/Help">Help</a></li>
            <li><a href="http://www.glottotopia.org/aagd/Search">Search</a></li>
          </ul>
        </div><!--/.nav-collapse --> 
    </div>
""",
            

            
            # Header
            u'<div id="header">',  
            #u'<h1 id="locationline">',
            #self.interwiki(d),
            #self.title_with_separators(d),
            #u'</h1>', 
                      
            #u'<hr id="pageline">',
            u'<div id="pageline"><hr style="display:none;"></div>',
            self.msg(d),
            u'</div>',

            """
<div class="container">  
    <div class="col-xs-12 col-sm-9">  
	<div > 
		<img src="http://www.glottotopia.org/moin_static197/aagd/img/beads.png" id="logo" /></a> 
		<div id="headerinfo">
		    <h1> AAGD </h1> 
		    <h3> Alaskan Athabascan Grammar Database </h3>
		    <div class="inputs"> """, 
	    self.searchpanel(d),  
	    """
		    </div>
		</div>     
	<div class="row">
	    <div class="pagination"> &nbsp;</div>
	
	""",    

            
            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),
	   
	    
        
            # Start of page
            
            ]
        return u'\n'.join(html)

    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            u'<h1 id="locationline">',
            self.title_with_separators(d),
            u'</h1>',
            self.msg(d),
            u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),
            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def footer(self, d, **keywords):
        """ Assemble wiki footer

        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        #page = d['page']
        html = [
            # End of page
            	    """
</div><!--/row--> <footer>
    <p>&copy; Glottotopia 2013-4</p>
</footer> 

    </div><!--/span--> 

    <div class="col-xs-6 col-sm-3 " >
	<div > 
	    <div class="navigators navigatorshigh">
		<h2> Recently visited </h2>
		<div class="navigatorbox">
		    <div>
	    """, 
		    self.quicklinksbar(d), 
		    
	    """
		    </div>  
		</div>  
	    <h2> Tools </h2>
	    <div class="navigatorbox navigatorboxhigh">
		    <div>
	    """,
		    self.editbar(d),
		    #self.navibarpanel(d), 
		    #self.addpagebarpanel(d),     
	    """
		    </div>  
		</div>  
	    <h2> User </h2>
	    <div class="navigatorbox navigatorboxhigh">
		    <div>
	    """,         
		    self.adduserbar(d),
		    
		"""
		    </div>  
		</div>  
	    </div>  
	</div>
	    </div>  
    
</div><!--/span--> 


<hr/> 
</div><!--/.container-->           
            """
            ]
        return u'\n'.join(html)
         

    def username(self, d):
        """ Assemble the username / userprefs link

        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """
        request = self.request
        _ = request.getText

        userlinks = []
        # Add username/homepage link for registered users. We don't care
        # if it exists, the user can create it.
        if request.user.valid and request.user.name:
            interwiki = wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = "%s @ %s" % (aliasname, interwiki[0])
            # link to (interwiki) user homepage
            homelink = (request.formatter.interwikilink(1, title=title, id="userhome", generated=True, *interwiki) +
                        request.formatter.text(name) +
                        request.formatter.interwikilink(0, title=title, id="userhome", *interwiki))
            userlinks.append(homelink)
            # link to userprefs action
            if 'userprefs' not in self.request.cfg.actions_excluded:
                userlinks.append(d['page'].link_to(request, text=_('Settings'),
                                               querystr={'action': 'userprefs'}, id='userprefs', rel='nofollow'))

        if request.user.valid:
            if request.user.auth_method in request.cfg.auth_can_logout:
                userlinks.append(d['page'].link_to(request, text=_('Logout'),
                                                   querystr={'action': 'logout', 'logout': 'logout'}, id='logout', rel='nofollow'))
        else:
            query = {'action': 'login'}
            # special direct-login link if the auth methods want no input
            if request.cfg.auth_login_inputs == ['special_no_input']:
                query['login'] = '1'
            if request.cfg.auth_have_login:
                userlinks.append(d['page'].link_to(request, text=_("Login"),
                                                   querystr=query, id='login', rel='nofollow'))
	
        userlinks_html=u'<li>'.join(userlinks)
        html = u'<ul id="userprofile">%s<ul>' % userlinks_html
        return html

    def getTrailLinks(self, d):
        """ Assemble page trail items

        @param d: parameter dictionary
        @rtype: unicode
        @return: linklist
        """
        request = self.request
        user = request.user 
        items = []
        if not user.valid or user.show_page_trail:
            trail = user.getTrail()
            if trail:
                items = []
                for pagename in trail:
                    try:
                        interwiki, page = wikiutil.split_interwiki(pagename)
                        if interwiki != request.cfg.interwikiname and interwiki != 'Self':
                            link = (self.request.formatter.interwikilink(True, interwiki, page) +
                                    self.shortenPagename(page) +
                                    self.request.formatter.interwikilink(False, interwiki, page))
                            items.append(link)
                            continue
                        else:
                            pagename = page
                    except ValueError:
                        pass
                    page = Page(request, pagename)		
                    if d['page_name']==pagename: #do not put a link to the page itself
			continue
                    title = page.split_title()
                    title = self.shortenPagename(title) 
                    items.append(title)
        return items

    def interwiki(self, d):
        """ Assemble the interwiki name display, linking to page_front_page

        @param d: parameter dictionary
        @rtype: string
        @return: interwiki html
        """
        if self.request.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or 'Self'
            link = page.link_to(self.request, text=text, rel='nofollow')
            html = u'<span id="interwiki">%s<span class="sep">: </span></span>' % link
        else:
            html = u''
        return html
        
        # Rick: Remember to customize this box by editing the edit_bar entry in your farmconfig/wikiconfig.py file!
# ## Rick This is a basic, no-frills (no hiding) panel
    
    def navibarpanel(self, d):
        """ Create page actions panel . 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted actions panel
        """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel"><h1>%s</h1>' % ( _("Tools")),
            self.navibar(d),
            u'</div>'
            ]
        return u''.join(html) 
        
    def addpagebarpanel(self, d):
        """ Create page actions panel . 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted actions panel
        """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel"><h1>%s</h1>' % ( _("Add page")),
            self.addpagebar(d),
            u'</div>'
            ]
        return u''.join(html) 
                
    def adduserbarpanel(self, d):
        """ Create userbar panel . 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted userbar panel
        """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel"><h1>%s</h1>' % ( _("Profile")),
            self.adduserbar(d),
            u'</div>'
            ]
        return u''.join(html) 
        
                   

        
# Rick: Borrowing code from Roger Haase's FixedLeft theme so that the searchbox buttons will wrap: 

    def searchpanel(self,d):
        """Create search panel.
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted search panel
        """
        _ = self.request.getText
        html = [
            #u'<div class="sidepanel"><h1>%s</h1>' % (_("Search Help")), 
	    self.searchform(d), 
            u'</div>',
            ]
        return u''.join(html)
       

    def addpagebar(self, d):
        """ Assemble the navibar

        @param d: parameter dictionary
        @rtype: unicode
        @return: addpagebar html
        """
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [ 
            u'<form class="searchform" method="get" action="%(baseurl)s/%(pagename_quoted)s">' % d,
            u'<div>',
            u'<ul>',
	    u'<li class="searchboxcontainer">',
	    u'<input type="text" name="target" class="searchinput">',
	    #u'<div class="searchbuttons">',
            u'<input type="hidden" name="action" value="goto">',
	    u'<input type="submit" value="Add page">',
            #u'</div>',
            u'</ul>',
            u'</div>',	    
	    u'</form>' ] # addapgebar items             

        # Assemble html
        items = u''.join(items)
        html = u''' 
		%s 
	''' % items
        return html

    def adduserbar(self,d):
        """Create search panel.
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted search panel
        """
        _ = self.request.getText
        html = [ 
            u'<ul>',
	    u'<li>',
	    self.username(d),
            u'</ul>' 
            ]
        return u''.join(html)

 
# Rick: Pasted in <div id="searchbuttons"> (don't forget the extra </div>) to break onto two lines.  Also removed the extra size="20" so that we can make it pretty.
    
    def searchform(self, d):
        """
        assemble HTML code for the search forms

        @param d: parameter dictionary
        @rtype: unicode
        @return: search form html
        """
        _ = self.request.getText
        form = self.request.form
        updates = {
            # Rick - commented out because we don't need it. We wrap this in the panel above: 
            #'search_label': _('Search:'),
            'search_value': wikiutil.escape(form.get('value', [''])[0], 1),
            'search_full_label': _('Documentation full'),
            'search_title_label': _('Documentation titles'),
            'baseurl': self.request.getScriptname(),
            'pagename_quoted': wikiutil.quoteWikinameURL(d['page'].page_name),
            }
        d.update(updates)
# Rick - paste this in below if you want a needless field label. 
# <label for="searchinput">%(search_label)s</label>
# Rick - I also whack the 'size' from input id because that belongs in CSS.
        html = u'''
	<form class="searchform" method="get" action="%(baseurl)s/%(pagename_quoted)s">
	<div>
	<input type="hidden" name="action" value="fullsearch">
	<input type="hidden" name="context" value="180">

	<input class="searchinput" type="text" size="" name="value" value="%(search_value)s" 
	    onfocus="searchFocus(this)" onblur="searchBlur(this)"
	    onkeyup="searchChange(this)" onchange="searchChange(this)" alt="this"> 
	    
	    <input id="titlesearch" name="titlesearch" type="submit"
	    value="%(search_title_label)s" alt="Search Titles">
	<input id="fullsearch" name="fullsearch" type="submit"
	    value="%(search_full_label)s" alt="Search Full Text">
	</div>
	</form>
	<script type="text/javascript">
	// Initialize search form
	// var f = document.getElementById('searchform');
	// f.getElementsByTagName('label')[0].style.display = 'none';
	var e = document.getElementById('searchinput');
	e.value = "";
	searchChange(e);
	searchBlur(e);
	</script>
	''' % d
        return html


# Rick:  Here we comment out the code that does the "linkto:" code because it's too easy to accidently click in our theme.
# Rick:  Use the WhatLinksToThis.py macro available on http://moinmo.in/MacroMarket
  
    def title_with_separators(self, d):
        """ Assemble the title using slashes, not <ul>

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        if d['title_text'] == d['page'].split_title():
            # just showing a page, no action
            segments = d['page_name'].split('/')
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            # Rick: commented out the below line:
            #link_query = {'action': 'fullsearch', 'context': '180', 'value': 'linkto:"%s"' % d['page_name'], }
            
            # Rick: We also delete 'querystr=link_query, title=link_title,' from this section:
            link = d['page'].link_to(self.request, link_text, css_class='backlink', rel='nofollow')
            if len(segments) <= 1:
                html = link
            else:
                content = []
                curpage = ''
                for s in segments[:-1]:
                    curpage += s
                    content.append(Page(self.request,
                                        curpage).link_to(self.request, s))
                    curpage += '/'
                path_html = u'<span class="sep"> / </span>'.join(content)
                # Rick: original: html = u'<span class="pagepath"> return to %s</span><span class="sep"> < </span>%s' % (path_html, link)
                html = u'<span class="pagepath">%s</span><span class="sep"> / </span>%s' % (path_html, link)
        else:
            html = wikiutil.escape(d['title_text'])
        return u'<span id="pagelocation">%s</span>' % html
        
# Rick:  We get to copy this in from __init__.py so that we can comment out the current page link.
    
    def navibar(self, d):
        """ Assemble the navibar

        @param d: parameter dictionary
        @rtype: unicode
        @return: navibar html
        """
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li>'
        current = d['page_name']

        # Process config navi_bar
        if request.cfg.navi_bar:
            for text in request.cfg.navi_bar:
                pagename, link = self.splitNavilink(text)
                if pagename == current:
                    cls = 'wikilink current'
                else:
                    cls = 'wikilink'
                items.append(item % (cls, link))
                found[pagename] = 1

        # Assemble html
        items = u''.join(items)
        html = u'''
		<ul id="navibar">
		%s
		</ul>
''' % items
        return html
        

    
    def quicklinksbar(self, d):
        """ Assemble the quicklinksbar

        @param d: parameter dictionary
        @rtype: unicode
        @return: quicklinksbar html
        """
        request = self.request
        found = {} # pages we found. prevent duplicates        
        items = [] # navibar items
        item = u'<li class="%s">%s</li>'
        current = d['page_name']         
	quicklinks = request.user.getQuickLinks() 
        quicklinkitems = []
        # Process quicklinks and trail
        if quicklinks:
            for text in quicklinks: 
			# Split text without localization, user knows what he wants
			pagename, link = self.splitNavilink(text, localize=0)
			if not pagename in found: 
			    quicklinkitems.append(item % ('userlink', link))
			    found[pagename] = 1				    
        traillinks = self.getTrailLinks(d)
        traillinkitems = []
        if traillinks:
            for text in traillinks: 
			# Split text without localization, user knows what he wants
			pagename, link = self.splitNavilink(text, localize=0)
			if not pagename in found:			    
			    traillinkitems.append(item % ('traillink', link))
			    found[pagename] = 1			      
        # Assemble html
        quicklinkitems = u''.join(quicklinkitems)
        traillinkitems = u''.join(traillinkitems)
        html = u'''
		<ul id="quicklinksbar">
		%s
		<li>&nbsp;
		%s
		</ul>
''' % (quicklinkitems, traillinkitems)
        return html
        

def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

