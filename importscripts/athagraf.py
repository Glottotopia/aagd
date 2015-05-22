import re 
import lingex

import random
import pprint 
from athahelpers import Metadata
from graftree import GrAFtree
from athasolr import AthaSOLR

IMTSPLITTERS = re.compile('[-=;:\.]')

class Athagraf:    
    athasolr = None
    
    def __init__(self, utterancefile, language = None, metadatafile=None):
	self.utterancefile = utterancefile  
	self.barefile = self.utterancefile.replace('-utterance.xml','')
	#self.IDfile = self.utterancefile.replace('-utterance','-default-ldt')
	#self.IDfile = self.utterancefile.replace('-utterance','-comment') 
	self.IDfile = self.utterancefile.replace('-utterance','-ID')
	self.IUfile = utterancefile.replace('-utterance','-Intonation_unit')
	self.wordsfile = utterancefile.replace('-utterance','-words')
	self.posfile = utterancefile.replace('-utterance','-pos')
	self.wordtranslationfile = utterancefile.replace('-utterance','-word_translation')
	self.morphemesfile = utterancefile.replace('-utterance','-morphemes')
	self.IMTfile = utterancefile.replace('-utterance','-IMT')
	self.POSfile = utterancefile.replace('-utterance','-POS')
	self.UTfile = utterancefile.replace('-utterance','-utterance_translation')
	self.language = language 
	self.metadata = Metadata(metadatafile)
	        
    #def __init__(self, utterancefile, language = None, orig='eaf', metadatafile=None):
	#if orig=='eaf':
	    #self.utterancefile = utterancefile  
	    #self.barefile = self.utterancefile.replace('-utterance.xml','')
	    #self.IUfile = utterancefile.replace('-utterance','-Intonation_unit')
	    #self.wordsfile = utterancefile.replace('-utterance','-words')
	    #self.posfile = utterancefile.replace('-utterance','-pos')
	    #self.wordtranslationfile = utterancefile.replace('-utterance','-word_translation')
	    #self.morphemesfile = utterancefile.replace('-utterance','-morphemes')
	    #self.IMTfile = utterancefile.replace('-utterance','-IMT')
	    #self.POSfile = utterancefile.replace('-utterance','-POS')
	    #self.UTfile = utterancefile.replace('-utterance','-utterance_translation')
	##if orig=='typecraft':
	    ##self.utterancefile = utterancefile   
	    ##self.barefile = self.utterancefile.replace('-utterance.xml','')
	    ##self.wordsfile = utterancefile.replace('-phrase','-word')
	    ##self.posfile = utterancefile.replace('-phrase','-pos')
	    ##self.wordtranslationfile = None
	    ##self.morphemesfile = utterancefile.replace('-phrase','-morpheme')
	    ##self.IMTfile = utterancefile.replace('-phrase','-gloss')
	    ##self.UTfile = utterancefile.replace('-phrase','-translation') 
	#self.language = language 
	#self.orig = 'eaf' 
	#self.metadata = Metadata(metadatafile)  
    
    def parse(self):	
	self.id_tree = GrAFtree(self.IDfile) 
	self.ut_tree = GrAFtree(self.UTfile)
	self.u_tree = GrAFtree(self.utterancefile) 
	self.iu_tree = GrAFtree(self.IUfile)
	self.w_tree = GrAFtree(self.wordsfile)  
	self.wt_tree = GrAFtree(self.wordtranslationfile)
	self.m_tree = GrAFtree(self.morphemesfile)
	self.imt_tree = GrAFtree(self.IMTfile)	 
	self.pos_tree = GrAFtree(self.POSfile)
	self.edgeclosure() 
	
	
    def edgeclosure(self):  
	def addToClosureDic(u, uppers, h, level):
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
		     

	self.u_tree.edgeclosured = {}  
	self.u_tree.edgeclosured['iu'] = {} 
	self.u_tree.edgeclosured['w'] = {}  
	self.u_tree.edgeclosured['w2wt'] = {}  
	self.u_tree.edgeclosured['m'] = {}  
	self.u_tree.edgeclosured['imt'] = {}  
	#l = [('iu','w'),('w','wt'),('w','m'),('m','imt')] 
	utterances = self.iu_tree.edged 		     
	 
	hierarchy = [(self.w_tree,'w'),(self.m_tree,'m'),(self.imt_tree,'imt')]
	for utterance in utterances:  
	    addToClosureDic(utterance,tuple(self.iu_tree.edged[utterance]) ,hierarchy,0)   
		
	#pprint.pprint(self.u_tree.edgeclosured['imt'])
	 
	
    def getPOS(self,n): 
	try:
	    i = self.pos_tree.edged[n][0] 
	    result =  self.pos_tree.textd[i] 
	    return result
	except KeyError:
	    #print "no POS for", n
	    return '~'
	
    def getPOSlist(self,topnode):
	return list(set([self.getPOS(word) 
		    for iunode in self.iu_tree.edged[topnode]
			for word  in  self.w_tree.edged[iunode]]))
				    
    def computeLingex(self,topnode):
	try:
	    u = lingex.Utteranceoid(self.getText(topnode),
		translation = self.getTranslation(topnode),
		children = [lingex.Utteranceoid(self.iu_tree.textd[iunode],
			    children =  [lingex.Wordoid(self.w_tree.textd[wnode], 
				translation = self.wt_tree.textd[self.wt_tree.edged[wnode][0]],
				pos = self.getPOS(wnode),
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
	except KeyError:
	    print "incomplete example\n\t%s"% self.getText(topnode)
	    return lingex.Item([])
	    
	 
    def getText(self,node):
	try:
	    return self.u_tree.textd[node]	
	except KeyError:
	    print "could not retrieve text for node", node
	    return "[missing text]"
	
    def getTranslation(self,node):
	return self.ut_tree.textd[self.ut_tree.edged[node][0]]
	
    #def getIMTWords(self,node): 
	#result = []
	#if node in self.u_tree.edgeclosured['imt']: 
	    #result = [ self.imt_tree.textd[x]  for x in self.u_tree.edgeclosured['imt'][node]  ]  
		
	#result =  ' '.join(result).replace('- ','-').replace(' -', '-')
	#return result	
	
    def getIMTGlosses(self,node):  
	tmp = {} 
	if node in self.u_tree.edgeclosured['imt']:  
	    tokens = [ self.imt_tree.textd[x]  for x in self.u_tree.edgeclosured['imt'][node]  ]
	    for token in tokens:
		for imt in  IMTSPLITTERS.split(token):
		    if imt.strip() != '':
			tmp[imt.strip()] = True 
	return tmp.keys()
	 	 
    
    def getID(self,topnode):
	#print topnode 
	IDid = self.id_tree.edged[topnode][0]
	#print IDid
	ID = self.id_tree.textd[IDid]
	#print ID
	return ID
	##print d
	#n = None
	#for k in d:
	    #if d[k][0]==topnode:
		#n = k
		##print n
		#break  
	#result = None 
	#print self.id_tree.edged
	#print self.id_tree.textd
	#result = self.id_tree.textd[n] 
	##print repr(result)
	#return result       
	
    def getID2(self,topnode):
	print topnode   
	n = None
	d = self.id_tree.edged
	print d 
	for k in d:
	    if d[k][0]==topnode:
		n = k
		print n
		break  
	result = None 
	#print self.id_tree.edged
	#print self.id_tree.textd
	result = self.id_tree.textd[n] 
	#print repr(result)
	return result   
	
    #def getID(self,topnode):
	#print topnode
	#d = self.id_tree.edged	
	#pprint.pprint(d)
	#try:
	    #n = d[topnode] 
	    #result = self.id_tree.textd[n[0]]
	#except KeyError:
	    #print "utterance %s has no ID" % topnode
	#return "-1"
	
    def graf2json(self): 
	topnodes = self.ut_tree.edged.keys() 
	#print topnodes
	for topnode in topnodes:
	    #print topnode
	    try:
		ID = self.getID(topnode)	    
	    except KeyError: 
		print "no ID\n\t%s" % self.getText(topnode)
		#ID = "rnd"+str(random.randint(1000000,9999999))
		continue	
	    if ID == '':
		print "no ID\n\t%s" % self.getText(topnode)
		#ID = "rnd"+str(random.randint(1000000,9999999))
		continue	
		
	    athasolr = AthaSOLR(ID, topnode, self) 
	    return athasolr.json()
	
    def graf2solr(self):   
	topnodes = self.ut_tree.edged.keys() 
	#print topnodes
	for topnode in topnodes:
	    #print topnode
	    try:
		ID = self.getID(topnode)	    
	    except KeyError: 
		print "no ID\n\t%s" % self.getText(topnode)
		#ID = "rnd"+str(random.randint(1000000,9999999))
		continue	
	    if ID == '':
		print "no ID\n\t%s" % self.getText(topnode)
		#ID = "rnd"+str(random.randint(1000000,9999999))
		continue	
		
	    athasolr = AthaSOLR(ID, topnode, self) 
	    athasolr.formattemplate()
	    athasolr.write() 


