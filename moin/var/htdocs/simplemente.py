# -*- coding: iso-8859-1 -*-
"""
    MoinMoin Simplemente theme

    XXX ToDo    
    Provide translations for:
    * _('Recently viewed pages')
    * _('Jump directly to the page content')
    * _('to the edit and actions menu')
    * _('to the navigation and search menu')
    * _('to the recently viewed pages')
    * _('or to the personalization menu')
    * _('Jump to the main navigation')
    * _('to the top of the page')
    * _('Your are here:')
    * _('Main navigation')
    * _('Page content')
    * _('Edit and actions menu')
    * _('Personalization menu')
    * _('Navigation menu')
    * _('Search')
    * _('Search Titles')
    * _('Search Full Text')
    * _('Accesskeys')
    * _('Available accesskeys on this page:')
    * _('(opens in new window)'
    * _('Footer')
    * _('Message')
    * _('Jump directly to the input field')

    XXX ToDo
    Check the skip links in editorheader according to your edit-conflict-policy.

    For a detailed explanation of theme usage see:
    http://moinmoin.wikiwikiweb.de/ThemeMarket/SimpleMente

    Simplemente theme
    @copyright: 2007 by Eduardo Mercovich and Oliver Siemoneit
    @license: GNU GPL, see COPYING for details.
    
"""

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.theme import ThemeBase

class Theme(ThemeBase):

    name = "simplemente"

    ##
    ## Sidepanels
    ##    

    def wikipanel(self, d):
        """ Create wiki panel """
        _ = self.request.getText
        dummy = self.getImageURI('1-pix.png')
        html = [
            u'<div class="sidepanel">',
            # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
            u'<div style="width:0%;height:0px;">',
            u'<a name="nav" id="nav" title="%s">' % _('Navigation menu'),
            u'<img src="%s" width="0" height="0" alt="">' % dummy,
            u'</a>',
            u'</div>',
            u'<h1 class="screenreader_info">%s</h1>' % _('Navigation menu'),
            self.navibar(d),
            self.searchform(d),
            u'</div>',
            ]
        return u'\n'.join(html)
    
    def pagepanel(self, d):
        """ Create page panel """
        _ = self.request.getText
        dummy = self.getImageURI('1-pix.png')
        if self.shouldShowEditbar(d['page']):
            html = [
                u'<div class="bottompanel">',
                # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
                u'<div style="width:0%;height:0px;">',
                u'<a name="edit" id="edit" title="%s">' % _('Edit and actions menu'),
                u'<img src="%s" width="0" height="0" alt="">' % dummy,
                u'</a>',
                u'</div>',
                u'<h1 class="screenreader_info">%s</h1>' % _('Edit and actions menu'),
                self.editbar(d),
                u'</div>',
                ]
            return u'\n'.join(html)
        return ''   
        
    def userpanel(self, d):
        """ Create user panel """
        _ = self.request.getText
        dummy = self.getImageURI('1-pix.png')
        html = [
            u'<div class="sidepanel">',
            # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
            u'<div style="width:0%;height:0px;">',
            u'<a name="user" id="user" title="%s">' % _('Personalization menu'),
            u'<img src="%s" width="0" height="0" alt="">' % dummy,
            u'</a>',
            u'</div>',
            u'<h1 class="screenreader_info">%s</h1>' % _('Personalization menu'),
            self.username(d),
            u'</div>',
            ]
        return u'\n'.join(html)

    def trailpanel(self, d):
        """ Create trail panel """
        _ = self.request.getText
        dummy = self.getImageURI('1-pix.png')
        html = ''
        trail = self.trail(d)
        if trail:
            html = [
                u'<div class="sidepanel">',
                # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
                u'<div style="width:0%;height:0px;">',
                u'<a name="trail" id="trail" title="%s">' % _('Recently viewed pages'),
                u'<img src="%s" width="0" height="0" alt="">' % dummy,
                u'</a>',
                u'</div>',
                u'<h1>%s</h1>' % _('Recently viewed pages'),
                trail,
                u'</div>',
                ]
        return u'\n'.join(html)

    ##
    ## Header and footer stuff
    ##    

    def header(self, d):
        """
        Assemble page header
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText
        dummy = self.getImageURI('1-pix.png')

        html = [
            u'<div id="container_content">',
            # Page
            self.startPage(),

            # Custom html above header
            self.emit_custom_html(self.cfg.page_header1),

            u'<div id="header">',
            # Hidden meta-navigation
            # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
            u'<div style="width:0%;height:0px;">',
            u'<a name="metanav" id="metanav" title="%s">' % _('Main navigation>'),
            u'<img src="%s" width="0" height="0" alt="">' % dummy,
            u'</a>',
            u'</div>',			
            # Skip links
            u'<div class="help">',
            u'<ul>',
            u'<li><a href="#page_content">%s</a></li>' % _('Jump directly to the page content'),
            u'<li><a href="#edit">%s</a></li>' % _('to the edit and actions menu'),
            u'<li><a href="#nav">%s</a></li>' % _('to the navigation and search menu'),
            self.trailSkipLink(d),
            u'<li><a href="#user">%s</a></li>' % _('or to the personalization menu'),
            u'</ul>',
            u'</div>',
            # Location line
            u'<div id=locationline>',
            # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
            u'<div style="width:0%;height:0px;">',
            u'<a name="page_content" id="page_content" title="%s">' % _('Page content'),
            u'<img src="%s" width="0" height="0" alt="">' % dummy,
            u'</a>',
            u'</div>',
            self.msg(d),
            u'<h1 class="screenreader_info">%s </h1>' % _('Your are here:'),
            self.title(d),
            u'<h1 class="screenreader_info">%s </h1>' % _('Page content'),
            u'</div>',
            u'</div>',

            # Custom html below header (not recomended!)
            self.emit_custom_html(self.cfg.page_header2),
	    ]
        return u'\n'.join(html)
    
    def editorheader(self, d):
        """
        Assemble page header for editor

        XXX ToDo: Check skip links according to your wiki settings, i.e. if editlock is turned on, enable the
                  the skip link "jump directly to the input field".
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText
        dummy = self.getImageURI('1-pix.png')

        html = [
            u'<div id="container_content">',
            # Page
            self.startPage(),

            # Custom html above header
            self.emit_custom_html(self.cfg.page_header1),

            u'<div id="header">',
            # Hidden meta-navigation
            # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
            u'<div style="width:0%;height:0px;">',
            u'<a name="metanav" id="metanav" title="%s">' % _('Main navigation>'),
            u'<img src="%s" width="0" height="0" alt="">' % dummy,
            u'</a>',
            u'</div>',			
            # Skip links
            u'<div class="help">',
            u'<ul>',
            # Turning on this feature depends on your wiki's edit-conflict-policy (see HelpOnEditLocks)
            # If 'lock' is enabled it's good to activate the 'jump to the input field'.
            # If 'warning' or 'none' is enabled users must read the messagebox to know about potential conflicts.
            # In this case it is better to turn this link of.
            #u'''<li><a href="#" onclick="document.forms[0].elements['savetext'].focus();">%s</a></li>''' % _('Jump directly to the input field'),
            # If 'Jump to the input field' is activated better turn this link of..
            u'<li><a href="#page_content">%s</a></li>' % _('Jump directly to the page content'),
            u'<li><a href="#nav">%s</a></li>' % _('to the navigation and search menu'),
            self.trailSkipLink(d),
            u'<li><a href="#user">%s</a></li>' % _('or to the personalization menu'),
            u'</ul>',
            u'</div>',
            # Location line
            u'<div id=locationline>',
            # Sucking IE anchor bug, see http://juicystudio.com/article/ie-keyboard-navigation.php
            u'<div style="width:0%;height:0px;">',
            u'<a name="page_content" id="page_content" title="%s">' % _('Page content'),
            u'<img src="%s" width="0" height="0" alt="">' % dummy,
            u'</a>',
            u'</div>',
            self.msg(d),
            u'<h1 class="screenreader_info">%s </h1>' % _('Your are here:'),
            self.title(d),
            u'</div>',
            u'</div>',

            # Custom html below header (not recomended!)
            self.emit_custom_html(self.cfg.page_header2),
            ]
        return u'\n'.join(html)

    def footer(self, d, **keywords):
        """ Assemble page footer
        
        @param d: parameter dictionary
        @keywords: not used currently
        @rtype: string
        @return: page footer html
        """
        _ = self.request.getText
        page = d['page']
        html = [

            # Page end
            self.pageinfo(page),
            u'<div class="help">',
            u'<ul>',
            u'<li><a href="#metanav">%s</a></li>' % _('Jump to the main navigation'),
            u'<li><a href="#page_content">%s</a></li>' % _('to the top of the page'),
            u'</ul>',
            u'</div>',
            self.pagepanel(d),
            self.endPage(),
            u'</div>',
                       
            # Sidebars
            u'<div id="sidebar">',
            self.wikipanel(d),
            self.userpanel(d),
            self.trailpanel(d),
            u'</div>',
            # Again some hidden extra navigation. We place it outside the sidebars and the footer
            # to prevent rendering bugs of IE
            u'<div class="help">',
            u'<ul>',
            u'<li><a href="#metanav">%s</a></li>' % _('Jump to the main navigation'),
            u'<li><a href="#page_content">%s</a></li>' % _('to the top of the page'),
            u'</ul>',
            u'</div>',

            # Real footer stuff
            u'<div id="container_footer">',
            u'<div id="footer">',
            u'<h1 class="screenreader_info">%s</h1>' % _('Footer'),
            # Use page_footer1 to state contact information, privacy policy, terms of use, disclaimer..
            self.emit_custom_html(self.cfg.page_footer1),
            self.credits(d),
            self.showversion(d, **keywords),
            # Use page_footer2 for more customization
            self.emit_custom_html(self.cfg.page_footer2),
            self.showaccesskeys(d),
            u'</div>',
            u'</div>',
            ]
        return u'\n'.join(html)

    ##
    ## Helper functions and overwritten standard behaviour of theme/_init_.py
    ##


    # Changed standard set of style sheets for screen view
    stylesheets = (
        # media         basename
        ('all',         'common'),
        ('screen',      'screen'),
        ('print',       'print_ext'),
        ('projection',  'projection'),
        )


    def title(self, d):
        """ Assemble breadcrumbs

        Changed: - ImmutablePage added to the end of page name if page is not writeable
                 - Virtual page of an action causes a new crumb and is appended to the
                   end (i.e. to the underlying current wikipage)
        
        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        content = []
        curpage = ''
        segments = d['page_name'].split('/')
        for s in segments[:-1]:
            curpage += s
            if curpage == s:
                content.append("%s" % Page(self.request, curpage).link_to(self.request, s))
            else:
                content.append(" / %s" % Page(self.request, curpage).link_to(self.request, s))
            curpage += '/'

        link_text = segments[-1]
        # Check whether an action has created a virtual page. No backlinking in this case.
        if d['title_text'] == d['page_name']: 
            link_title = _('Click to do a full-text search for this title')
            link_query = {
                'action': 'fullsearch',
                'value': 'linkto:"%s"' % d['page_name'],
                'context': '180', }
            link = d['page'].link_to(self.request, link_text, querystr=link_query, title=link_title, css_class='backlink', rel='nofollow')
        else:
            curpage += link_text
            link = Page(self.request, curpage).link_to(self.request, link_text)

        # Show interwiki?
        if self.cfg.interwikiname and self.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or 'Self'
            interwiki = page.link_to(self.request, text=text, rel='nofollow')
            content.insert(1, '%s : ' % interwiki)

        if len(segments) > 1:
            content.append(' / %s' % link)
        else:
            content.append('%s' % link)
            
        # Check whether page ist writeable. If not: add a note on that
        if not (d['page'].isWritable() and self.request.user.may.write(d['page'].page_name)):
            content.append(' (%s)' % _('Immutable Page', formatted=False))

        # Check whether an action has created a virtual page e.g. "Diff for..". Add this virtual page to the end of the breadcrumb navigation.
        if d['title_text'] != d['page_name']: 
            content.append(' / %s' % wikiutil.escape(d['title_text']))

        html = '''
<p id="pagelocation">
%s
</p>
''' % "".join(content)
        return html


    def externalScript(self, name):
        """ Format external script html

        Changed: Check on Moin version for backwards compatibility
                 Use changed common.js of simplemente theme instead of
                 common/js/common.js
        """
        # Check for version: prefix for the static stuff has been changed in Moin1.6
        if self.cfg.url_prefix: # prior Moin1.6
            src = '%s/simplemente/js/%s.js' % (self.cfg.url_prefix, name)
        else:                   # we are on Moin1.6
            src = '%s/simplemente/js/%s.js' % (self.cfg.url_prefix_static, name)

        return '<script type="text/javascript" src="%s"></script>' % src


    def headscript(self, d):
        """ Return html head script with common functions

        Changed: Added GoogleAnalytics support and support for customizable accesskeys

        @param d: parameter dictionary
        @rtype: unicode
        @return: script for html head
        """
        # Don't add script for print view
        # Try..except for backwards compatibility of Moin versions only
        try:
            if self.request.action == 'print':
                return u''
        except:
            if self.request.form.get('action', [''])[0] == 'print':
                return u''

        # Searchbox stuff
        _ = self.request.getText
        script = u"""
<script type="text/javascript">
<!--
var search_hint = "%(search_hint)s";
//-->
</script>
""" % { 'search_hint': _('Search', formatted=False), }
        
        # GoogleAnalytics stuff
        if hasattr(self.request.cfg, 'google_analytics_account_number'):
            account_number = self.request.cfg.google_analytics_account_number
            script += u"""
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript"></script>
<script type="text/javascript">
<!--
_uacct = "%(account_number)s";
urchinTracker();
//-->
</script>""" % { 'account_number': account_number, }

        # Accesskey customization
        user = self.request.user
        content = ''
        if user.valid and user.name: 
            homewiki, homepage = wikiutil.getInterwikiHomePage(self.request)
            # We don't support interwiki homepages at the moment.
            # In the long run better move accesskey customization to the userprefs menu instead
            # of using an attached file 'shortcuts.js" to the user's homepage.
            # This will solve most security, perfomance and interwiki homepage problems
            if homewiki == 'Self':
                from MoinMoin.action import AttachFile
                import os
                pagename, filename = AttachFile.absoluteName('shortcuts.js', homepage)
                fname = wikiutil.taintfilename(filename)
                fpath = AttachFile.getFilename(self.request, pagename, fname)
                base, ext = os.path.splitext(filename)
                try:
                    # Try to get the user's shortcut list
                    content = file(fpath, 'r').read()
                    content = wikiutil.decodeUnknownInput(content)
                    # Escape malicious code
## Turned off due to i18n problems with regex checking
##                    paras = []
##                    try:
##                        paras = content.split(',')
##                    except:
##                        paras[0] = content
##                    import re
##                    pattern1 = re.compile('^"(name|id)\#[-_a-zA-Z0-9]+\=[a-zA-Z0-9]+"$')
##                    pattern2 = re.compile('^"(name|id)\#[-_a-zA-Z0-9]+\=[a-zA-Z0-9]+\![ -_a-zA-Z0-9]+"$')
##                    for para in paras:
##                        fail1 = fail2 = False
##                        if re.search(pattern1, para.strip()) == None:
##                            fail1 = True
##                        if re.search(pattern2, para.strip()) == None:
##                            fail2 = True
##                        if fail1 and fail2:
##                            content = ''
##                            break
                    
                    content = content.replace(')', '')
                    content = content.replace(';', '')

                except:
                    # User hasn't specified a shortcut list
                    pass

        if not content: 
            # If there is no user shortcut list: Do we have some global shortcut lists
            # set in wikiconfig.py?
            lang_keydefaults = 'accesskey_defaults_%s' % self.request.lang
            # Check whether there is a shortcut list fitting to the request.lang object
            if hasattr(self.request.cfg, lang_keydefaults):
                content = getattr(self.request.cfg, lang_keydefaults)
            # Otherwise check if 'accesskey_defaults' is set
            elif hasattr(self.request.cfg, 'accesskey_defaults'):
                content = self.request.cfg.accesskey_defaults
                
        script += u"""
<script type="text/javascript">
<!--
var shortcut_list = new Array (%(shortcut_list)s);
//-->
</script>
""" % { 'shortcut_list': content,}

        return script
    
    def html_stylesheets(self, d):
        """ Assemble html head stylesheet links
        
        Just here so that in prior 1.6Moin version simplemente also renders correctly on IE
        """
        link = '<link rel="stylesheet" type="text/css" charset="%s" media="%s" href="%s">'

        # Check mode
        if d.get('print_mode'):
            media = d.get('media', 'print')
            stylesheets = getattr(self, 'stylesheets_' + media)
        else:
            stylesheets = self.stylesheets
        usercss = self.request.user.valid and self.request.user.css_url

        # Create stylesheets links
        html = []

        # Try..except for backwards compatibility of Moin versions only
        try:
            prefix = self.cfg.url_prefix_static
        except:
            prefix = self.cfg.url_prefix
            
        csshref = '%s/%s/css' % (prefix, self.name)
        for media, basename in stylesheets:
            href = '%s/%s.css' % (csshref, basename)
            html.append(link % (self.stylesheetsCharset, media, href))

            # Don't add user css url if it matches one of ours
            if usercss and usercss == href:
                usercss = None

        # admin configurable additional css (farm or wiki level)
        for media, csshref in self.request.cfg.stylesheets:
            html.append(link % (self.stylesheetsCharset, media, csshref))


        # tribute to the most sucking browser: MS IE6

        # Try..except for backwards compatibility of Moin versions only
        try:
            if self.cfg.hacks.get('ie7', False) and self.request.action != 'edit':
                # using FCKeditor and IE7 at the same time makes nices crashes in IE
                html.append("""
<!-- compliance patch for microsoft browsers -->
<!--[if lt IE 7]>
   <script src="%s/common/ie7/ie7-standard-p.js" type="text/javascript"></script>
<![endif]-->
""" % prefix)
        except:
            if self.cfg.hacks.get('ie7', False) and self.request.form.get('action', [''])[0] != 'edit':
                html.append("""
<!-- compliance patch for microsoft browsers -->
<!--[if lt IE 7]>
   <script src="%s/common/ie7/ie7-standard-p.js" type="text/javascript"></script>
<![endif]-->
""" % prefix)


        csshref = '%s/%s/css/msie.css' % (prefix, self.name)
        html.append("""
<!-- css only for MSIE browsers -->
<!--[if IE]>
   %s
<![endif]-->
""" % link % (self.stylesheetsCharset, 'all', csshref))

        # Add user css url (assuming that user css uses same charset)
        if usercss and usercss.lower() != "none":
            html.append(link % (self.stylesheetsCharset, 'all', usercss))

        return '\n'.join(html)

    def editbar(self, d):
        """ Assemble the editbar.

        Changed: If special editbar configs are found in wikiconfig.py, build customized
                 editbar according to the requested language. Otherwise use Moin's
                 default editbar.
                
        @param d: parameter dictionary
        @rtype: unicode
        @return: iconbar html
        """
        _ = self.request.getText
        page = d['page']
        if not self.shouldShowEditbar(page):
            return ''

        html = self._cache.get('editbar')
        if html is None:
            action_defaults = 'simplemente_editbaritems_%s' % self.request.lang
            action_defaults_ext = 'simplemente_editbaritems_ext_%s' % self.request.lang
            # Check whether there are editbar setting fitting to the request.lang object
            if hasattr(self.request.cfg, action_defaults):
                actions = getattr(self.request.cfg, action_defaults)
                html = u'<ul class="simplemente_editbar">%s</ul>\n' % self.assembleEditbarItems(d, actions)
                if hasattr(self.request.cfg, action_defaults_ext):
                    actions_ext = getattr(self.request.cfg, action_defaults_ext)
                    html += u'''<span class="screenreader_info">%s</span>
<ul class="simplemente_editbar_ext">%s</ul>\n''' % ( _('More actions:'), self.assembleEditbarItems(d, actions_ext))
            # Otherwise check if we have some language independent defaults
            elif hasattr(self.request.cfg, 'simplemente_editbaritems'):
                actions = self.request.cfg.simplemente_editbaritems
                html = u'<ul class="simplemente_editbar">%s</ul>\n' % self.assembleEditbarItems(d, actions)
                if hasattr(self.request.cfg, 'simplemente_editbaritems_ext'):
                    actions_ext = self.request.cfg.simplemente_editbaritems_ext
                    html += u'''<span class="screenreader_info">%s</span>
<ul class="simplemente_editbar_ext">%s</ul>\n''' % ( _('More actions:'), self.assembleEditbarItems(d, actions_ext))
            # No? Use Moin's default editbar then
            else:
                items = ''.join(['<li>%s</li>' % item
                                 for item in self.editbarItems(page) if item])
                html = u'<ul class="editbar">%s</ul>\n' % items

            self._cache['editbar'] = html

        return html

    def assembleEditbarItems(self, d, items):
        """ Assemble Simplemente editbar items.

        New helper function.

        If the name of the menuitem is either "Quicklink" or "Subscribe", use the default Moin
        menu item to have the toggle functionality

        Raw action is by default opend now in a new window. Reason: There are no navigtional
        elements in the raw view which renders the page for an unexperienced user unusable.
               
        @param d: parameter dictionary
        @param actions_dict: customized editbar items dictionary
        @rtype: unicode
        @return: editbar items html
        """
        _ =  self.request.getText
        page = d['page']
        html = ''
        for item in items:
            key, value = item
            if key == 'Subscribe':
                link = self.subscribeLink(page)
            elif key == 'Quicklink':
                link = self.quicklinkLink(page)
            elif value == 'raw':
                 link = page.link_to(self.request, text=key,
                                     querystr={'action': value}, id=key, name=key,
                                    rel='nofollow', target='_blank')
            else:
                link = page.link_to(self.request, text=key,
                                    querystr={'action': value}, id=key, name=key, rel='nofollow')
            if link and value == 'raw':
                html += '<li>%s<span class="screenreader_info">%s</span></li>' % (link, _('(opens in new window)'))
            elif link:
                html += '<li>%s</li>' % link

        return html


    def editorLink(self, page):
        """ Return a link to the editor 
        
        Changed: name attrib changed for accesskeys
                 name attrib for textedit remains unchanged, i.e. is always
                 set to 'texteditlink'
                 [and "guieditlink' for the guieditor (see common.js)]
        """
        if not (page.isWritable() and
                self.request.user.may.write(page.page_name)):
            return self.disabledEdit()

        _ = self.request.getText
        querystr = {'action': 'edit'}

        guiworks = self.guiworks(page)
        if self.showBothEditLinks() and guiworks:
            text = _('Edit (Text)', formatted=False)
            querystr['editor'] = 'text'
            attrs = {'name': 'texteditlink', 'rel': 'nofollow', }
        else:
            text = _('Edit', formatted=False)
            if guiworks:
                # 'textonly' will be upgraded dynamically to 'guipossible' by JS
                querystr['editor'] = 'textonly'
                attrs = {'name': 'texeditlink', 'rel': 'nofollow', }
            else:
                querystr['editor'] = 'text'
                attrs = {'name': 'texteditlink', 'rel': 'nofollow', }

        return page.link_to(self.request, text=text, querystr=querystr, **attrs)


    def infoLink(self, page):
        """ Return link to page information

        Changed: name attrib added for accesskeys
        """
        _ = self.request.getText
        return page.link_to(self.request,
                            text=_('Info', formatted=False),
                            querystr={'action': 'info'}, id='info', name='info',
                            rel='nofollow')

    def subscribeLink(self, page):
        """ Return subscribe/unsubscribe link to valid users

        Changed: name attrib added for accesskeys
        
        @rtype: unicode
        @return: subscribe or unsubscribe link
        """
        if not (self.cfg.mail_enabled and self.request.user.valid):
            return ''

        _ = self.request.getText
        # Try..except for backwards compatibility of Moin versions only
        try:
            from MoinMoin.version import release_short
            if self.request.user.isSubscribedTo([page.page_name]):
                action, text = 'unsubscribe', _("Unsubscribe", formatted=False)
            else:
                action, text = 'subscribe', _("Subscribe", formatted=False)
                return page.link_to(self.request, text=text, querystr={'action': action}, css_class='nbsubscribe', name='subscribe', rel='nofollow')
        except:
            if self.request.user.isSubscribedTo([page.page_name]):
                text = _("Unsubscribe", formatted=False)
            else:
                text = _("Subscribe", formatted=False)
            return page.link_to(self.request, text=text, querystr={'action': 'subscribe'},
                                id='subscribe', name='subscribe', rel='nofollow')

    def quicklinkLink(self, page):
        """ Return add/remove quicklink link

        Changed: name attrib added for accesskeys
        
        @rtype: unicode
        @return: link to add or remove a quicklink
        """
        if not self.request.user.valid:
            return ''
   
        _ = self.request.getText
        # Try..except for backwards compatibility of Moin versions only
        try:
            if self.request.user.isQuickLinkedTo([page.page_name]):
                action, text = 'quickunlink', _("Remove Link", formatted=False)
            else:
                action, text = 'quicklink', _("Add Link", formatted=False)
            return page.link_to(self.request, text=text, querystr={'action': action}, css_class='nbquicklink', name='quicklink', rel='nofollow')
        except:
            if self.request.user.isQuickLinkedTo([page.page_name]):
                text = _("Remove Link", formatted=False)
            else:
                text = _("Add Link", formatted=False)
            return page.link_to(self.request, text=text, querystr={'action': 'quicklink'},
                                id='quicklink', name='quicklink', rel='nofollow')


    def attachmentsLink(self, page):
        """ Return link to page attachments

        Changed: name and title attrib added for accesskeys
        """
        _ = self.request.getText
        return page.link_to(self.request,
                            text=_('Attachments', formatted=False),
                            querystr={'action': 'AttachFile'}, id='attachments',
                            name='attachments', rel='nofollow')

    def splitNavilink(self, text, localize=1):
        """ Split navibar links into pagename, link to page

        Changed: name attrib added for accesskeys
        """
        request = self.request

        # Handle [pagename title] or [url title] formats
        if text.startswith('[') and text.endswith(']'):
            try:
                pagename, title = text[1:-1].strip().split(' ', 1)
                title = title.strip()
                localize = 0
            except (ValueError, TypeError):
                # Just use the text as is.
                pagename = title = text

        # Handle regular pagename like "FrontPage"
        else:
            # Use localized pages for the current user
            if localize:
                # Try..except for backwards compatibility of Moin versions only
                try:
                    page = wikiutil.getSysPage(request, text)
                except:
                    page = wikiutil.getLocalizedPage(request, text)
            else:
                page = Page(request, text)
            pagename = page.page_name
            # Try..except for backwards compatibility of Moin versions only
            try: 
                title = page.split_title()
            except:
                title = page.split_title(request)
            title = self.shortenPagename(title)
            link = page.link_to(request, title, name=title)


        from MoinMoin import config
        for scheme in config.url_schemas:
            if pagename.startswith(scheme):
                title = wikiutil.escape(title)
                link = self.request.formatter.url(1, pagename, name=title) + \
                       self.request.formatter.text(title) +\
                       self.request.formatter.url(0)
                return pagename, link

        # remove wiki: url prefix
        if pagename.startswith("wiki:"):
            pagename = pagename[5:]

        # try handling interwiki links
        try:
            interwiki, page = pagename.split(':', 1)
            thiswiki = request.cfg.interwikiname
            if interwiki == thiswiki:
                pagename = page
                title = page
            else:
                return (pagename,
                        self.request.formatter.interwikilink(True, interwiki, page, name=page) +
                        page +
                        self.request.formatter.interwikilink(False, interwiki, page)
                        )

        except ValueError:
            pass

        pagename = request.normalizePagename(pagename)
        link = Page(request, pagename).link_to(request, title, name=title)

        return pagename, link

    def trail(self, d):
        """ Assemble page trail
        
        Changed: name attrib added for accesskeys
        """
        request = self.request
        user = request.user
        html = ''
        if user.valid and user.show_page_trail:
            trail = user.getTrail()
            if trail:
                items = []
                i = -1
                for pagename in trail:
                    i = i + 1
                    trail_number = "trail%02d" % i
                    try:
                        interwiki, page = pagename.split(":", 1)
                        if request.cfg.interwikiname != interwiki:
                            link = (self.request.formatter.interwikilink(True, interwiki, page, name=trail_number) +
                                    self.shortenPagename(page) +
                                    self.request.formatter.interwikilink(False, interwiki, page))
                            items.append('<li>%s</li>' % link)
                            continue
                        else:
                            pagename = page

                    except ValueError:
                        pass
                    page = Page(request, pagename)
                    # Try..except for backwards compatibility of Moin versions only
                    try:
                        title = page.split_title()
                    except:
                        title = page.split_title(request)
                    title = self.shortenPagename(title)
                    link = page.link_to(request, title, name=trail_number)
                    items.append('<li>%s</li>' % link)
                html = '''
<ul id="pagetrail">
%s
</ul>''' % ''.join(items)
        return html

    def logo(self):
        """ Assemble logo with link to front page

        Changed: * we don't need a div wrapper for the textlogo
                 * append text "FrontPage" to the logo string
        
        @rtype: unicode
        @return: logo html
        """
        _ = self.request.getText
        html = u''
        if self.cfg.logo_string:
            page = wikiutil.getFrontPage(self.request)
            logo_string = self.cfg.logo_string
            logo_append = '<span class="screenreader_info"> %s</span>' % _('FrontPage', formatted=False) 
            logo_string = logo_string + logo_append
            # Try..except for backwards compatibility of Moin versions only
            try:
                logo = page.link_to_raw(self.request, logo_string)
            except:
                pagename = wikiutil.getFrontPage(self.request).page_name
                pagename = wikiutil.quoteWikinameURL(pagename)
                logo = wikiutil.link_tag(self.request, pagename, logo_string)
            html = u'%s' % logo
        return html

    def msg(self, d):
        """ Assemble the msg display

        Changed: Added hidden h1 heading for better navigation with screenreaders
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: msg display html
        """
        _ = self.request.getText
        msg = d['msg']
        if not msg:
            return u''

        if isinstance(msg, (str, unicode)):
            # Render simple strings with a close link
            close = d['page'].link_to(self.request, text=_('Clear message'))
            html = u'<p>%s</p>\n<div class="buttons">%s</div>\n' % (msg, close)
        else:
            # msg is a widget
            html = msg.render()

        return u'<div id="message">\n<h1 class="screenreader_info">%s</h1>\n%s\n</div>\n' % (_('Message'), html)

    def navibar(self, d):
        """ Assemble the navibar

        Changed: * textlogo added as first entry of the navibar
                 * name attrib added for accesskeys
        """
        request = self.request
        _ = request.getText
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li>'
        current = d['page_name']

        # Add textlogo as first entry
        items.append(item % ('wikilink', self.logo()))
        found[wikiutil.getFrontPage(self.request).page_name] = 1
        found[_('FrontPage', formatted=False)] = 1

        # Process config navi_bar, eliminating dublicate to the FrontPage
        if request.cfg.navi_bar:
            for text in request.cfg.navi_bar:
                pagename, link = self.splitNavilink(text)
                if not pagename in found:
                    if pagename == current:
                        cls = 'wikilink current'
                    else:
                        cls = 'wikilink'
                    items.append(item % (cls, link))
                    found[pagename] = 1

        # Add user links to wiki links, eliminating duplicates.
        userlinks = request.user.getQuickLinks()
        for text in userlinks:
            # Split text without localization, user knows what he wants
            pagename, link = self.splitNavilink(text, localize=0)
            if not pagename in found:
                if pagename == current:
                    cls = 'userlink current'
                else:
                    cls = 'userlink'
                items.append(item % (cls, link))
                found[pagename] = 1

        # Add current page at end
        if not current in found:
            # Try..except for backwards compatibility of Moin versions only
            try:
                title = d['page'].split_title()
            except:
                title = d['page'].split_title(request)
            title = self.shortenPagename(title)
            link = d['page'].link_to(request, title, name="navbar_current_page")
            cls = 'current'
            items.append(item % (cls, link))

        # Assemble html
        items = u''.join(items)
        html = u'''
<ul id="navibar">
%s
</ul>
''' % items
        return html

    def searchform(self, d):
        """ assemble HTML code for the search forms

        Changed: linebreak added for Simplemente. Searchbox formatting now done by
                 css
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: search form html
        """
        _ = self.request.getText
        form = self.request.form
        updates = {
            'search_label': _('Search:'),
            'search_alt': _('Search'),
            'search_titles_alt': _('Search Titles'),
            'search_full_alt': _('Search Full Text'),
            'search_value': wikiutil.escape(form.get('value', [''])[0], 1),
            'search_full_label': _('Text', formatted=False),
            'search_title_label': _('Titles', formatted=False),
            }
        d.update(updates)

        html = u'''
<form id="searchform" method="get" action="">
<div>
<input type="hidden" name="action" value="fullsearch">
<input type="hidden" name="context" value="180">
<label for="searchinput">%(search_label)s</label>
<input id="searchinput" type="text" name="value" value="%(search_value)s" size="20"
    onfocus="searchFocus(this)" onblur="searchBlur(this)"
    onkeyup="searchChange(this)" onchange="searchChange(this)" alt="%(search_alt)s">
<br> 
<input id="titlesearch" name="titlesearch" type="submit"
    value="%(search_title_label)s" alt="%(search_titles_alt)s">
<input id="fullsearch" name="fullsearch" type="submit"
    value="%(search_full_label)s" alt="%(search_full_alt)s">
</div>
</form>
<script type="text/javascript">
<!--// Initialize search form
var f = document.getElementById('searchform');
f.getElementsByTagName('label')[0].style.display = 'none';
var e = document.getElementById('searchinput');
searchChange(e);
searchBlur(e);
//-->
</script>
''' % d
        return html

    def credits(self, d, **keywords):
        """ Create credits html from credits list
        
        Changed: If no credits are set, the default Moin credits are disabled and replaced by
                 a Creative Common License hint for the wiki content.
        """
        # Try..except for backwards compatibility of Moin versions only
        try:
            from MoinMoin.config.multiconfig import DefaultConfig
        except:
            from MoinMoin.multiconfig import DefaultConfig

        page_credits = self.cfg.page_credits
        cc_img = self.getImageURI('cc-wiki.png')
        page = wikiutil.getFrontPage(self.request)
        # Try..except for backwards compatibility of Moin versions only
        try:
            cc_src = page.link_to_raw(self.request, self.request.cfg.sitename)
        except:
            pagename = wikiutil.getFrontPage(self.request).page_name
            pagename = wikiutil.quoteWikinameURL(pagename)
            cc_src = wikiutil.link_tag(self.request, pagename, self.request.cfg.sitename)
         
        _credits = u'''<div id="creditos">
<!--Creative Commons License-->
%s is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share Alike 3.0  License</a> 
<br>
<img alt="Creative Commons License" style="border-width: 0" src="%s"/>.
<!--/Creative Commons License-->
</div>
<!--
<rdf:RDF xmlns="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
<Work rdf:about="">
    <license rdf:resource="http://creativecommons.org/licenses/by-sa/3.0/" />
</Work>
<License rdf:about="http://creativecommons.org/licenses/by-sa/3.0/">
    <permits rdf:resource="http://web.resource.org/cc/Reproduction"/>
    <permits rdf:resource="http://web.resource.org/cc/Distribution"/>
    <requires rdf:resource="http://web.resource.org/cc/Notice"/>
    <requires rdf:resource="http://web.resource.org/cc/Attribution"/>
    <permits rdf:resource="http://web.resource.org/cc/DerivativeWorks"/>
    <requires rdf:resource="http://web.resource.org/cc/ShareAlike"/>
</License>
</rdf:RDF> -->''' % (cc_src, cc_img)

        if self.cfg.page_credits != DefaultConfig.page_credits:
            # Admin has set in wikiconfig.py new credits. Disable simplemente credits.
            _credits = ''
        else:
            # Admin hasn't set new credits. Throw away the default credits and display simplemente credits only.
            page_credits = []
        
        if isinstance(page_credits, (list, tuple)):
            if page_credits != []:
                items = ['<li>%s</li>' % i for i in page_credits]
                html = '<ul id="credits">\n%s\n</ul>%s\n' % (''.join(items), _credits)
            else:
                html = _credits
        else:
            # Old config using string, output as is
            html = page_credits + _credits
        return html

    def showaccesskeys(self, d):
        """ Create accesskey html

        New helper function.

        If you put a <div id="accesskeys></div> somewhere in the page (e.g. by setting in wikiconfig.py
        "page_footer2 = u'<div id="accesskeys"></div>'"), the javascript function responsible for
        accesskeys augmentation of the page will add here a list of available shortcuts for the current
        page. 
        
        However since we want to have also some translated text before this list, we have to do it here so as to be
        able to use the built-in getText.

        @param d: parameter dictionary
        @rtype: unicode
        @return: accesskey list html
        """
        _ = self.request.getText
        html = ''
        show_keys = False
        if hasattr(self.request.cfg, 'show_accesskeys'):
            show_keys = self.request.cfg.show_accesskeys
        if show_keys:
            html = u'<div id="accesskeys"><h1 class="screenreader_info">%s</h1>%s</div>' % (_('Accesskeys'),_('Available accesskeys on this page:'))
        return html

    def trailSkipLink(self, d):
        """ Assemble HTML code for the "page trail" - skip link

        New helper function.

        Look whether we have a trail. If yes: build the skip link for it and
        return it.

        @param d: parameter dictionary
        @rtype: unicode
        @return: skip link html
        """
        _ = self.request.getText
        user = self.request.user
        html = ''
        if user.valid and user.show_page_trail:
            html = u'<li class="help"><a href="#trail">%s</a></li>' % _('to the recently viewed pages'),
        return u'\n'.join(html)

    def getImageURI(self, image):
        """ Get the URI of an image in the theme's img folder

        New helper function.

        @param image: name of image e.g. 'test.png'
        @rtype: unicode
        @return: image URI
        """
        if self.cfg.url_prefix:
            uri = u'%s/simplemente/img/%s' % (self.cfg.url_prefix, image)
        else:
            uri = u'%s/simplemente/img/%s' % (self.cfg.url_prefix_static, image)
        return uri

    ##
    ## Theme main-entry
    ##    

def execute(request):
    """
    Generate and return a theme object
        
    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

