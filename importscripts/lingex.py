import re
import pprint

class IMTError(ValueError):
    pass

class IMTWordError(IMTError):
    pass

class IMTSentenceError(IMTError):
    pass

OUTERHTML_ =  u"""<head>  
  <title></title>
  <style type="text/css">
 
.item { 
    display: inline;
    float: left;
    margin-right: 2px;
    min-height:40px;
    border: 1px solid black;
} 

.label{
    background: white;
  }
  </style>
</head><body>%s</body></html>"""

OUTERXML_ =  u"""<?xml version="1.0" encoding="UTF-8"?>
%s"""

IMTSPLITTERS = re.compile('[-=~]')
  
class Item():
    """ A sentence, word or morpheme with translation, comment and subelements"""
    
    children = None
    parent = None
    label = ''
    translation = ''
    comment = ''
    pos = ''
    
    def __init__(self,children):
	self.children = children
	self.offspringjoiner = " "
	
    def __str__(self):
	return self.offspringjoiner.join([str(x) for x in self.children])
	
    def flatstring(self):
	return self.offspringjoiner.join([x.flatstring() for x in self.children])
		
    def getLeaves(self,nested = False):
	if nested:
	    return [(ch.getLeaves(nested = True)) for ch in children]
	return [ch.getLeaves() for ch in children]
	
    def newick(self): 
	return "(%s)%s"%(','.join([ch.newick() for ch in self.children]), self.label)
	
    def xml(self, outer= True): 
        childxml = '\n'.join([c.xml(outer=False) for c in self.children]) 
	innerxml = u"""<item>
 <label>{}</label>
  <children>
   {}
  </children>
  </item>""".format(self.label, childxml) 
	if not outer:
	    return innerxml
	return OUTERXML_%innerxml
	
    def html(self, outer=True, level=0): 
        childhtml = '\n'.join([c.html(outer=False, level=level+1) for c in self.children]) 
        pospart = ''
        if self.pos != '':
	    pospart = u"""  <div class="pos">
    <div><span>{}</span></div>
  </div> 
	    """.format(self.pos)
	translationpart = ''
	if self.translation != '':
	    translationpart = u""" <div class="translation">
    <span>{}</span></div>
 """.format(self.translation)

	innerhtml = u"""<div class="item xlevel{}"> 
 <div class="label">{}</div>
    <div class="children">
    {}
    </div>  
  {}
  {}
  </div>
  """.format(level,self.label, childhtml, pospart, translationpart) 
	if not outer:
	    return innerhtml
	return OUTERHTML_%innerhtml	
	
    def tupl(self): 
	if self.children != []:
	    return [self.label,self.translation,[c.tupl() for c in self.children]]
	return [self.label,self.translation,[]]
        #return "|".join([self.label, self.translation])
        
    def bb(self):
	return self.html(outer=False).replace('<','[').replace('>',']')  
	    

	
	
class Textoid(Item):
    """an item of roughly text length"""
    offspringjoiner = "\n"
	
class Paragraphoid(Item):
    """an item of roughly text length"""
    def __init__(self,s,children=False):
	self.label = s
	self.s = s
	if children:
	    self.children = children
	else:
	    self.children = [Utteranceoid(x) for x in s.split(" | ")]
	
    offspringjoiner = ". "
	
class Utteranceoid(Item):
    """an item of roughly utterance length"""
    def __init__(self,s,children=False, translation=' '):
	self.label = s
	self.s = s
	if children:
	    self.children = children
	else:
	    self.children = [Wordoid(x) for x in self.s.split()]
	self.translation = translation
    
    offspringjoiner = " "
    
    def insertIMT(self,imt):
	tokens = imt.split()
	if len(tokens) != len(self.children):
	    #print self.s
	    #print tokens
	    #print len(tokens), len(self.children)
	    #for x in self.children:
		#print repr(x.s)
	    print len(tokens),len(self.children)
	    raise IMTSentenceError
	for child, token in zip(self.children, tokens):
	    try:
		child.insertIMT(token)
	    except IMTWordError:
		pass
        
class Wordoid(Item):
    """an item of roughly word length"""
    offspringjoiner = ""
    
    def __init__(self,s,children=False, translation=' ', pos='POS'):
	self.label = s
	self.s = s
	if children:
	    self.children = children
	else:
	    self.children = [Morphemoid(x) for x in re.split("([=-])",self.s)][::2]
	self.joiners = [x for x in re.split("([=-])",self.s)][:1][::2]
	self.translation = translation
	self.pos = pos
	
    def __str__(self): 
	return self.s 
	
    def flatstring(self): 
	return self.offspringjoiner.join([x.label for x in self.children])
	
    def getLeaves(self,nested = False):
	if nested:
	    return((s))
	return self.s
	
    def insertIMT(self,word):
	morphemes = IMTSPLITTERS.split(word)
	if len(morphemes) != len(self.children):	    
	    raise IMTWordError     
	for child, token in zip(self.children, morphemes):
	    child.translation = token
	
	
    
class Morphemoid(Item):
    """an item of roughly morpheme length"""
    def __init__(self,s,translation=' '):
	self.label = s
	self.children = [] 
	self.translation = translation 
    def __str__(self): 
	return self.label
	
	
    def newick(self): 
	#return self.translation, self.label
	return  self.label
	
	
	  
    
    
class Morpheme:
    """ a morpheme"""
    
class Affix(Morpheme):
    """ an affix"""
    
class Clitic(Morpheme):
    """ a clitic"""
    
class PreX(Morpheme):
    """a left-attaching thing"""
    
class Prefix(PreX,Affix):
    """a left-attaching thing"""
    rightjoiner = "-"
    
class Preclitic(PreX,Clitic):
    """a left-attaching thing"""
    rightjoiner = "="
    
class PostX(Morpheme):
    """a left-attaching thing """
    leftjoiner = "-"
    
class Postfix(PostX,Affix):
    """a left-attaching thing """
    leftjoiner = "-"
    
class Postclitic(PostX,Clitic):
    """a left-attaching thing """
    leftjoiner = "-"

if __name__ == '__main__':
    t = "In meine-r Bade-wanne bin ich Kapitaen | das ist wunder-schoen"

    p = Paragraphoid(t)
    pprint.pprint(p.newick())

