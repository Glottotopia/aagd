
#Changes to normal setup:
 - underlay folder is in `./etc`, as it will never change
 - the full server is in `./local`
 - since we already have content, this is included in the install, in this case in /var/wiki/ath
 - `htdocs` are in `./var`
 - the FCKEditor is included. We only allow write access to people we personally know, so security risks are few

#Install:
 - load `mod_wsgi` in Apache
 - edit `./local/moin/wiki/server/moin.wsgi`
 - add the following line to apache config:
  -  `WSGIScriptAlias /aagd $WHATEVERTHEPATHIS/local/moin/wiki/server/moin.wsgi`
 - edit `./etc/wikiconfig.py`




