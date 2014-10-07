
from xml.etree  import ElementTree as ET 

class GrAFtree:
    def __init__(self,f): 
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
	for edge in self.edges: 
	    from_ = edge.attrib['from']
	    to_ = edge.attrib['to'] 
	    try:
		self.edged[from_].append(to_ )
	    except KeyError:
		self.edged[from_] = [to_] 
	self.dominatednodesd = {}
