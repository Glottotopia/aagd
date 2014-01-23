

import re
from xml.etree  import ElementTree as ET 
import lingex

import pprint

IMTSPLITTERS = re.compile('[-=;:\.]')

class Language:
    def __init__(self,name,iso,coords):
	self.name=name
	self.iso=iso
	self.coords=coords

class EAF:    
    athasolar = None
    
    def __init__(self,utterancefile, language = None):
	self.utterancefile = utterancefile  
	self.IUfile = utterancefile.replace('-utterance','-Intonation_unit')
	self.wordsfile = utterancefile.replace('-utterance','-words')
	self.posfile = utterancefile.replace('-utterance','-pos')
	self.wordtranslationfile = utterancefile.replace('-utterance','-word_translation')
	self.morphemesfile = utterancefile.replace('-utterance','-morphemes')
	self.IMTfile = utterancefile.replace('-utterance','-IMT')
	self.UTfile = utterancefile.replace('-utterance','-utterance_translation')
	self.language = language
	        
    def __init__(self,utterancefile, language = None, orig='eaf'):
	if orig=='eaf':
	    self.utterancefile = utterancefile  
	    self.IUfile = utterancefile.replace('-utterance','-Intonation_unit')
	    self.wordsfile = utterancefile.replace('-utterance','-words')
	    self.posfile = utterancefile.replace('-utterance','-pos')
	    self.wordtranslationfile = utterancefile.replace('-utterance','-word_translation')
	    self.morphemesfile = utterancefile.replace('-utterance','-morphemes')
	    self.IMTfile = utterancefile.replace('-utterance','-IMT')
	    self.UTfile = utterancefile.replace('-utterance','-utterance_translation')
	if orig=='typecraft':
	    self.utterancefile = utterancefile   
	    self.wordsfile = utterancefile.replace('-phrase','-word')
	    self.posfile = utterancefile.replace('-phrase','-pos')
	    self.wordtranslationfile = None
	    self.morphemesfile = utterancefile.replace('-phrase','-morpheme')
	    self.IMTfile = utterancefile.replace('-phrase','-gloss')
	    self.UTfile = utterancefile.replace('-phrase','-translation') 
	self.language = language 
	self.orig = orig
	    
    def parse(self, orig='eaf'):	
	self.ut_tree = GrAFtree(self.UTfile)
	self.u_tree = GrAFtree(self.utterancefile)
	if orig=='eaf':
	    self.iu_tree = GrAFtree(self.IUfile)
	self.w_tree = GrAFtree(self.wordsfile)
	self.pos_tree = GrAFtree(self.posfile)
	if orig=='eaf':
	    self.wt_tree = GrAFtree(self.wordtranslationfile)
	self.m_tree = GrAFtree(self.morphemesfile)
	self.imt_tree = GrAFtree(self.IMTfile)
	self.edgeclosure(orig=orig) 
	
	
    def edgeclosure(self,orig='eaf'):  
	self.u_tree.edgeclosured = {} 
	if orig=='eaf':
	    self.u_tree.edgeclosured['iu'] = {} 
	self.u_tree.edgeclosured['w'] = {}  
	self.u_tree.edgeclosured['m'] = {}  
	self.u_tree.edgeclosured['imt'] = {}  
	#l = [('iu','w'),('w','wt'),('w','m'),('m','imt')]
	if orig=='eaf':
	    utterances = self.iu_tree.edged
	if orig == 'typecraft':
	    utterances = self.w_tree.edged
	
		
	
	def addToClosureDic(u,uppers,h, level):
	    if h == []:
		return
	    lowertree, lowerstring = h[0]
	    h = h[1:] 
	    for upper in uppers:  
		#print level*' ', upper, lowerstring
		if upper in lowertree.edged:
		    lowers = tuple(lowertree.edged[upper])  
		    #print lowers
		    try: 
			for l in lowers:
			    self.u_tree.edgeclosured[lowerstring][u].append(l)
		    except KeyError: 
			self.u_tree.edgeclosured[lowerstring][u] = list(lowers) 
		    addToClosureDic(u, lowers, h, level+1) 
		     
	
	hierarchy = [(self.m_tree,'m'),(self.imt_tree,'imt')]
	if orig == 'eaf':
	    hierarchy = [(self.w_tree,'w'),(self.m_tree,'m'),(self.imt_tree,'imt')]
	for utterance in utterances: 
	    if orig=='eaf':
		addToClosureDic(utterance,tuple(self.iu_tree.edged[utterance]) ,hierarchy,0)  
	    if orig =='typecraft':
		addToClosureDic(utterance,tuple(self.w_tree.edged[utterance]) ,hierarchy,0)  
		
	#pprint.pprint(self.u_tree.edgeclosured['imt'])
	 
				    
				    
    def computeLingex(self,topnode,orig):
	if orig == 'eaf':
	    u = lingex.Utteranceoid(self.getText(topnode),
		children = [lingex.Utteranceoid(self.iu_tree.textd[iunode],
			    children =  [lingex.Wordoid(self.w_tree.textd[wnode],
				children =  [lingex.Morphemoid(self.m_tree.textd[mnode],
						    translation = self.imt_tree.textd.get(self.imt_tree.edged.get(mnode,[''])[0])
						    ) 					     
					    for mnode 
					    in self.m_tree.edged.get(wnode,[])
					    ],
					)
					for wnode 
					in self.w_tree.edged[iunode]
					]
			    ) 
			    for iunode 
			    in self.iu_tree.edged[topnode]
			    ]
		)
	    return u 
	if orig=='typecraft':	   
	    toptext = self.getText(topnode)
	    u = lingex.Utteranceoid(toptext,
		    children = [lingex.Utteranceoid(toptext,
				children =  [lingex.Wordoid(self.w_tree.textd[wnode],
				    children =  [lingex.Morphemoid(self.m_tree.textd[mnode],
							translation = self.m_tree.meaningd[mnode]
							) 					     
						for mnode 
						in self.m_tree.edged.get(wnode,[])
						],
					    )
					    for wnode 
					    in self.w_tree.edged[topnode]
					    ]
				)  
				]
		    )
	    return u 
	    
	
	
    def getDominationDictionary_(self, upper, lower):
	d  = {}
	for x in upper.textd: 
	    for y in lower.edged: 
		if x == y:   
		    edges = lower.edged[x]
		    for edge in edges:
			try:
			    trs = lower.textd[edge]  
			    d[x].append(trs)
			except KeyError: 
			    d[x] = [trs]	 
	return d
	
    def getText(self,node):
	return self.u_tree.textd[node]	
	
    def getTranslation(self,node):
	return self.ut_tree.textd[self.ut_tree.edged[node][0]]
	
    #def getIMTWords(self,node): 
	#result = []
	#if node in self.u_tree.edgeclosured['imt']: 
	    #result = [ self.imt_tree.textd[x]  for x in self.u_tree.edgeclosured['imt'][node]  ]  
		
	#result =  ' '.join(result).replace('- ','-').replace(' -', '-')
	#return result	
	
    def getIMTGlosses(self,node): 
	#print self.u_tree.edgeclosured['imt']
	tmp = {} 
	if node in self.u_tree.edgeclosured['imt']:  
	    tokens = [ self.imt_tree.textd[x]  for x in self.u_tree.edgeclosured['imt'][node]  ]
	    for token in tokens:
		for imt in  IMTSPLITTERS.split(token):
		    if imt.strip() != '':
			tmp[imt.strip()] = True 
	return tmp.keys()
	 	
	
    #def eaf2solr(language=None, offset=0):
    def eaf2solr(self,orig='eaf'):   
	d = self.getDominationDictionary_(self.u_tree,self.ut_tree)
	#print d
	l = [ (self.u_tree.textd[x], d[x][0]) for x in d ] #there is only one translation per utterance, so we can directly access it at [0]
	topnodes = self.ut_tree.edged.keys() 
	for i,topnode in enumerate(topnodes):  
	    athasolar = AthaSOLR(i, 
				    topnode,
				    self )
	    athasolar.formattemplate()
	    athasolar.write() 

class GrAFtree:
    def __init__(self,f):
	print f
	self.textd = {} 
	self.edged = {}
	self.meaningd = {}
	self.edgeclosured = {}
	self.f = f
	try:
	    self.tree = ET.parse(f)
	except IOError:
	    self.tree = None
	    return
	self.root = self.tree.getroot()
	self.anchors = self.root.findall('.//{http://www.xces.org/ns/GrAF/1.0/}a')
	self.edges = self.root.findall('.//{http://www.xces.org/ns/GrAF/1.0/}edge') 
	for a in self.anchors:
	    ref = a.attrib['ref']
	    try:
		text = a.find('.//{http://www.xces.org/ns/GrAF/1.0/}f[@name="annotation_value"]').text 
	    except AttributeError:
		text = ''
	    self.textd[ref] = text 
	    try:
		meaning = a.find('.//{http://www.xces.org/ns/GrAF/1.0/}f[@name="meaning"]').text 
	    except AttributeError:
		meaning = None
	    self.meaningd[ref] = meaning 
	    #print ref, text
	    #try:
		#text = t.find('.//*/*').text
	    #except AttributeError:
		#text = '' 
	for edge in self.edges:
	    from_ = edge.attrib['from']
	    to_ = edge.attrib['to'] 
	    try:
		self.edged[from_].append(to_ )
	    except KeyError:
		self.edged[from_] = [to_]
		
	self.dominatednodesd = {}

	    
class AthaSOLR:
    def __init__(self,ID,topnode,eaf):
	self.topnode=topnode
	self.language = eaf.language 
	self.src=eaf.utterancefile 
	self.ID="%s-%s-%s"% (self.language.iso,hash(self.src)%1000,ID) 
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
	self.mn()
	try: 
	    self.lingex = eaf.computeLingex(topnode,eaf.orig) 
	except KeyError:
	    self.lingex = lingex.Item([])
	
    def removePunctuation(self,w):
	ps = '()[]{},.:;!?"'
	for p in ps:
	    w = w.replace(p,'')
	return w

    def mn(self):
	self.vernacularwords = u'\n'.join([u'<field name="vernacularword">%s</field>'%self.removePunctuation(w.strip())  for w in self.vernacularwords ] )  
	self.translationwords = u'\n'.join([u'<field name="translatedword">%s</field>'%self.removePunctuation(w.strip())  for w in self.translatedwords ] ) 
	
    def getIMTString(self,imts):
	return u'\n'.join([u'<field name="gloss">%s</field>'%w.strip() for w in self.imtglosses ] )  
	
    def write(self):
	out = open('solr/%s.xml'%self.ID,'w')
	out.write(self.outstring.encode('utf8'))
	out.close()
	
	
    translation = ''
    docs = []
    

    def formattemplate(self):  
	test = getAdditions(self.translation) 
	#test = []
	additions =  u'\n'.join([u'<field name="%s">%s</field>' % a for a in test ] )   
	#ID = '%s.%s.%s' % (iso,j,i)
	name = u"%s-%s" % (self.src.encode('utf8'),self.ID) 
	self.outstring = template.format(ID=self.ID, 
			    txt=self.txt,
			    trs=self.translation,
			    src=self.src, 
			    vernacularwords=self.vernacularwords, 
			    translationwords=self.translationwords, 
			    additions=additions, 
			    lg=self.language.name.replace(' ','_'),
			    iso=self.language.iso,
			    coords=self.language.coords, 
			    lenws = self.lenwords, 
			    lenchars=self.lenchars, 
			    #imtwords=self.imtwords, 
			    glosses=self.getIMTString(self.imtglosses),
			    lingex=self.lingex.bb())   
			    
			    
template = u"""<add><doc>
<field name="id">{ID}</field>  
<field name="name">{txt}</field> 
<field name="language">{lg}</field> 
<field name="iso639-3">{iso}</field> 
<field name="vernacularsentence">{txt}</field>  
<field name="translatedsentence">{trs}</field>
<field name="author">{src}</field>
<!-- Join --> 
{vernacularwords} 
{translationwords} 
{additions} 
{glosses}
<field name="lingex">{lingex}</field>  
<field name="location">{coords}</field>  
<field name="words">{lenws}</field>  
<field name="chars">{lenchars}</field>  
</doc></add>"""

def getAdditions(trs):
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
    terminatives = ('ends', 'ended', 'stops', 'stop', 'stopped')
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
	for e in evids: 
	    if e == t:
		additions.append(('evidentiality','other'))
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
	
    