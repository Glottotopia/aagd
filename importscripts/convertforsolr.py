from xml.etree  import ElementTree as ET 
import glob

from athautils import EAF, Language, AthaSOLR, template, getAdditions


lgs = ( 
('Upper_Tanana',  'tau','63.1377,-142.5244',  'UT', 'graf', 'utterance','eaf'),
('Lower_Tanana',  'taa','65.1577, -149.3765', 'LT', 'graf', 'phrase', 'typecraft'),
('Koyukon',       'koy','64.8816,-157.7044',  'KOY','graf', 'phrase', 'typecraft'),
)

docs = []

for x in lgs: 
    lg, iso, coords, d, fmt,toplevelfilename,orig  = x 
    print lg
    if fmt == 'csv':
	for j,f in enumerate(glob.glob('%s/*csv'%d)):
	    for ii,line in enumerate(open(f).readlines()):   
		i, txt, trs, src = line.strip().decode('utf8').replace('&','&amp;').split('\t')
		lenchars = len(txt)
		vws = txt.split()
		lenws = len(vws)
		tws = trs.split()
		
		vernacularwords = u'\n'.join([u'<field name="vernacularword">%s</field>'%w.strip() for w in vws ] )
		translationwords = u'\n'.join([u'<field name="translatedword">%s</field>'%w.strip() for w in tws ] ) 
		additions =  u'\n'.join([u'<field name="%s">%s</field>' % a for a in getAdditions(trs) ] )   
		
		#ID = u'%s.%s.%s' % (iso,j,i)
		ID="%s-%s-%s"% (iso,hash(iso)%1000,ii) 
		
		name = u"%s-%s" % (src,i)
		t = template.format(ID=ID, 
			    txt=txt,
			    trs=trs,
			    src=src, 
			    vernacularwords=vernacularwords, 
			    translationwords=translationwords, 
			    additions=additions, 
			    lg=lg,
			    iso=iso,
			    coords=coords, 
			    lenws = lenws, 
			    lenchars=lenchars, 
			    imtwords='', 
			    glosses='', 
			    lingex='')  
		#t = template.format(ID=ID,name=name, txt=txt, trs=trs, src=src, vernacularwords=vernacularwords, translationwords=translationwords, additions=additions, lg=lg,iso=iso,coords=coords, lenws = lenws, lenchars=lenchars)
		docs.append((t,ID))

    if fmt == 'graf':   
	for i,f in enumerate(glob.glob('/home/snordhoff/Dropbox/data_for_import/graf/%s/*-%s.xml' % (d.lower(),toplevelfilename))):    
	    eaf = EAF(f, language=Language(lg, iso, coords), orig=orig)
	    eaf.parse(orig=orig) 
	    eaf.eaf2solr(orig=orig)  
	
	
    for (doc,ID) in docs:  
	out = open('./solr/%s.xml'%ID,'w') 
	out.write(doc.encode('utf8'))  
	out.close()