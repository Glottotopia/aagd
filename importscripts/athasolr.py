import re
from xml.sax.saxutils import escape
import xmltodict
import json

class AthaSOLR:
    """An object holding all information we need for SOLR import"""
    def __init__(self,ID,topnode,eaf):
	self.topnode=topnode
	self.language = eaf.language 
	self.metadata = eaf.metadata
	self.src = eaf.barefile  
	self.ID=ID 
	if ID in (None,''):
	    raise ValueError
	#
	self.txt=eaf.getText(topnode)
	self.lenchars = len(self.txt)
	self.vernacularwords = self.txt.split() 
	self.lenwords = len(self.vernacularwords)
	#
	self.translation=eaf.getTranslation(topnode)
	self.translatedwords=set([self.removePunctuation(x) for x in self.translation.split()])
	#
	#self.imtwords=eaf.getIMTWords(topnode)
	self.imtglosses=eaf.getIMTGlosses(topnode)
	self.grammaticalglosses=[x for x in self.imtglosses if re.search('[A-Z]{2}', x)]
	self.lexicalglosses=[x for x in self.imtglosses if x not in self.grammaticalglosses]
	self.mn() 
	self.lingex = eaf.computeLingex(topnode) 
	self.partsofspeech = eaf.getPOSlist(topnode)
	
    def removePunctuation(self,w):
	ps = '()[]{},.:;!?"'
	for p in ps:
	    w = w.replace(p,'')
	return w

    def mn(self):
	self.vernacularwords = u'\n'.join([u'<field name="vernacularword">%s</field>'%escape(self.removePunctuation(w.strip()))  for w in self.vernacularwords ] )  
	self.translationwords = u'\n'.join([u'<field name="translatedword">%s</field>'%escape(self.removePunctuation(w.strip()))  for w in self.translatedwords ] ) 
	
    def getIMTString(self,imts):
	return u'\n'.join([u'<field name="gloss">%s</field>'%w.strip() for w in self.imtglosses ] )  
	
    def getPOSString(self,poss):
	return u'\n'.join([u'<field name="pos">%s</field>'%w.strip() for w in self.partsofspeech ] )  
	
    def getLexicalGlossString(self,imts):
	return u'\n'.join([u'<field name="lexicalgloss">%s</field>'%w.strip() for w in self.lexicalglosses ] )  
	
    def getGrammaticalGlossString(self,imts):
	return u'\n'.join([u'<field name="grammaticalgloss">%s</field>'%w.strip() for w in self.grammaticalglosses ] )  
	
    def write(self):
	out = open('solr/%s.xml'%self.ID,'w')
	out.write(self.outstring.encode('utf8'))
	out.close()
	
    def forjson(self):
	return {"id":self.ID,
	    "name":{self.ID},
	    "vernacularsentence":{escape(self.txt)},
	    "translatedsentence":{escape(self.translation)},
	    "author":{escape(self.src)}, 
	    #"vernacularwords":{self.vernacularwords}, 
	    #"translationwords":{self.translationwords}, 
	    #"additions":{additions}, 
	    "language":{self.language.name.replace(' ','_')},
	    "iso639-3":{self.language.iso},
	    "location":{self.language.coords}, 
	    "words":{ self.lenwords}, 
	    "chars":{self.lenchars}, 
	    #"pos ":{ self.getPOSString(self.partsofspeech)},
	    #"glosses":{self.getIMTString(self.imtglosses)},
	    #"grammaticalglosses":{self.getGrammaticalGlossString(self.grammaticalglosses)},
	    #"lexicalglosses":{self.getLexicalGlossString(self.lexicalglosses)},
	    #"metadatastring":{ metadatastring},
	    "lingex":{self.lingex.bb()},
	    "version":{0}
	    } 
	
	
    translation = ''
    docs = []
     
	

    def formattemplate(self):   
	test = self.getAdditions(self.translation)  
	#test = []
	additions =  u'\n'.join([u'<field name="%s">%s</field>' % a for a in test ] )    
	name = u"%s-%s" % (self.src.encode('utf8'),self.ID) 
	metadatastring = None
	try:
	    #print self.ID
	    #print self.metadata.chunks[self.ID]
	    metadatastring = self.metadata.chunks[self.ID].toSOLRstring()
	except KeyError:
	    print "no metadata\n\t%s" % self.ID
	self.outstring = self.template.format(ID=self.ID, 
			    txt=escape(self.txt),
			    trs=escape(self.translation),
			    src=escape(self.src), 
			    vernacularwords=self.vernacularwords, 
			    translationwords=self.translationwords, 
			    additions=additions, 
			    lg=self.language.name.replace(' ','_'),
			    iso=self.language.iso,
			    coords=self.language.coords, 
			    lenws = self.lenwords, 
			    lenchars=self.lenchars, 
			    #imtwords=self.imtwords, 
			    pos = self.getPOSString(self.partsofspeech),
			    glosses=self.getIMTString(self.imtglosses),
			    grammaticalglosses=self.getGrammaticalGlossString(self.grammaticalglosses),
			    lexicalglosses=self.getLexicalGlossString(self.lexicalglosses),
			    metadatastring= metadatastring,
			    lingex=self.lingex.bb())   
			    
			
    template = u"""<add><doc>
    <field name="id">{ID}</field>  
    <field name="name">{txt}</field> 
    <field name="language">{lg}</field> 
    <field name="iso639-3">{iso}</field> 
    <field name="vernacularsentence">{txt}</field>  
    <field name="translatedsentence">{trs}</field>
    <field name="author">{src}</field>
    {metadatastring} 
    <!-- Join --> 
    {vernacularwords} 
    {translationwords} 
    {additions} 
    {glosses}
    {grammaticalglosses}
    {lexicalglosses}
    {pos}
    <field name="lingex">{lingex}</field>  
    <field name="location">{coords}</field>  
    <field name="words">{lenws}</field>  
    <field name="chars">{lenchars}</field>   
    </doc></add>"""

    def getAdditions(self,trs):
	return []
	trs = trs.lower()
	complexity = False
	negations = ('no', 'none', 'not', 'never', 'nowhere', 'nothing', "don't", "does't", "did't", "won't", "would't", "hasn't", "haven't", "hadn't", "neither" , "nor")
	locations = ('at','where', 'between', 'above', 'below', 'front', 'top', 'bottom', 'side', 'nowhere')
	cmtinstrs = ('with',)
	temproles = ('when','always','never', 'then')
	srcroles = ('from',)
	pathroles = ('along',)
	past_references = ('ago','yesterday')
	present_references = ('now','today')
	future_references = ('tomorrow','will', "won't", 'future')
	poss_preds = ('has a ', 'have a ', 'has an ', 'have an ')
	poss_attrs = (' my ', ' your ', ' his ', ' our ', ' their ', "'s")
	sap1 = ('I', 'me', 'my','myself', 'we', 'us', 'our', 'ours', 'ourselves') #no mine bcs of gold mine
	sap2 = ('you', 'your', 'yours', 'yourself', 'yourselves')
	ors = ('or',)
	ands = ('and',)
	nors = ('neither',)
	tnexs = ('until', 'before', 'after', 'during', 'already', 'still', 'yet') 
	cnexs = ('because',)
	fnexs = ('in order to',)
	dqs = ('two','three','four','five','six','seven','eight','nine','ten','eleven', 'twelve', 'dozen', 'twenty', 'hundred', 'thousand', 'million')
	idqs = ('some', 'many', 'several', 'every', 'all')
	uqs = ('every', 'all', 'always')
	nqs = ('nowhere', 'never', 'no one', 'none')
	uqs_combined = ('every',)
	comparatives = ('better', 'more')
	superlatives = ('most','best')
	sufficientives = ('enough',)
	abundantives = ('too much',)
	evids = ('apparently',)
	proximals =  ('here', 'this', 'these')
	distals =  ('those',) # no that or there bcs of polysemy
	presentationals = ('there are', 'there is', 'there was', 'there were')
	conditions = ('if', 'unless')
	embeddings = ('whether',)
	manners = ('how',)
	reflexives = ('myself','yourself','himself','herself','ourselves','yourselves','themselves')
	reciprocals = ('each other',)
	inceptives = ('begin', 'began', 'begun', 'begins', 'beginning', 'start', 'started', 'starting', 'starts')
	terminatives = ('ends', 'ended'	, 'stops', 'stop', 'stopped')
	repetitives = ('again', )
	modals = ('want','wants','need','needs','must','can','might','may','could', 'should')
	additions = []
	
	
	if trs.strip().endswith('?'):
	    additions.append(('speech_acts','question'))
	if trs.strip().endswith('!'): # or txt.strip().endswith('!'):
	    additions.append(('speech_acts','command'))
	#if txt[1].lower() != txt[1]:
	    #print txt
	    #additions.append(('noun','proper_noun'))	
	# multi word expressions
	for poss in poss_preds:
	    if poss in trs:
		additions.append(('posssession','predicative'))
		break
	#for a in abundantives:
	    #if a in trs:
		#additions.append(('grade','abundant'))
		#break	    
	#for p in presentationals: 
	    #if p in trs:
		#additions.append(('focus','thetic'))
		#break	    
	#for fnex in fnexs:
	    #if fnex in trs: 
		#additions.append(('nexus','final'))
		#complexity = "complex"
		#break
	#for r in reciprocals: 
	    #if r in trs:
		#additions.append(('orientation','reciprocal')) 
	#for uq in uqs_combined:
	    #if uq in trs:
		#additions.append(('quantification','totality'))
	#for nq in nqs:
	    #if nq in trs:
		#additions.append(('quantification','zero'))
		#break
	# one word expressions
	for t in trs.split():
	    t = t.replace(',','').replace('.', '').replace('?','').replace('!','')
	    #for neg in negations:
		#if neg == t:
		    #additions.append(('negation','negative'))
		    #break
	    #for sap in sap1:
		#if sap == t:
		    #additions.append(('participant','speaker'))
		    #break
	    #for sap in sap2:
		#if sap == t:
		    #additions.append(('participant','addressee'))
		    #break
	    for poss in poss_attrs:
		if poss == t:
		    additions.append(('posssession','attributive'))
		    break
	    for loc in locations:
		if loc == t: 
		    additions.append(('participant_roles','location'))	
	    for pr in past_references :
		if pr == t: 
		    additions.append(('time','past'))
	    for pr in present_references :
		if pr == t: 
		    additions.append(('time','present'))
	    for fr in future_references :
		if fr == t:  
		    additions.append(('time','future'))
	    for o in ors :
		if o == t:  
		    additions.append(('coordination','OR'))
	    for a in ands :
		if a == t:  
		    additions.append(('coordination','AND'))
	    for tnex in tnexs :
		if tnex == t:  
		    additions.append(('coordination','temporal'))
		    complexity = "complex"
	    #for cnex in cnexs :
		#if cnex == t:  
		    #additions.append(('nexus','causal'))	
		    #complexity = "complex"
	    for x in nors :
		if x == t:  
		    additions.append(('coordination','NOR'))	
	    for cmtinstr in cmtinstrs: 
		if cmtinstr == t:
		    additions.append(('participant_roles','instrumental'))
		    additions.append(('participant_roles','comitative'))
	    for tr in temproles: 
		if tr == t:
		    additions.append(('participant_roles','time')) 
	    for src in srcroles: 
		if src == t:
		    additions.append(('participant_roles','source')) 
	    for p in pathroles: 
		if p == t:
		    additions.append(('participant_roles','path')) 
	    #for dq in dqs: 
		#if dq == t:
		    #additions.append(('quantity','definite'))
	    #for idq in idqs: 
		#if idq == t:
		    #additions.append(('quantity','indefinite'))
	    #for uq in uqs: 
		#if uq == t:
		    #additions.append(('quantity','totality'))
	    for c in comparatives: 
		if c == t:
		    additions.append(('comparison','comparison'))
	    for s in superlatives: 
		if s == t:
		    additions.append(('comparison','superlative'))
	    #for s in sufficientives: 
		#if s == t:
		    #additions.append(('grade','sufficient'))
	    #for e in evids: 
		#if e == t:
		    #additions.append(('evidentiality','other'))
	    #for p in proximals: 
		#if p == t:
		    #additions.append(('distance','proximals'))
	    #for d in distals: 
		#if d == t:
		    #additions.append(('distance','distal'))
	    for c in conditions: 
		if c == t:
		    additions.append(('participant_roles','condition')) 
		    complexity = 'complex'
	    for m in manners: 
		if m == t:
		    additions.append(('participant_roles','manner')) 
	    #for r in reflexives:  
		#if r == t: 
		    #additions.append(('orientation','reflexive'))  
	    for i in inceptives:  
		if i == t: 
		    additions.append(('phase','beginning'))  
	    for te in terminatives:  
		if te == t: 
		    additions.append(('phase','end'))  
	    #for r in repetitives:  
		#if r == t: 
		    #additions.append(('quantification2','iterative'))  
	    for m in modals:  
		if m == t: 
		    additions.append(('modality','modality'))  
	    for e in embeddings: 
		if e == t: 
		    complexity = 'complex'
		    
	if complexity:
	    additions.append(('sentence_type','complex')) 
	return additions
	    

    