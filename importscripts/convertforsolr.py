import sys
from athautils import EAF, Language, AthaSOLR, template, getAdditions

lgs = {'tau':Language('Upper_Tanana',  'tau','63.1377,-142.5244'),
	'taa':Language('Lower_Tanana',  'taa','65.1577, -149.3765'),
	'koy':Language('Koyukon',       'koy','64.8816,-157.7044')
	}
	
f = sys.argv[1]
lg = lgs[sys.argv[2]]
metadatafile = sys.argv[3]
 
eaf = EAF(f, lg,  metadatafile = metadatafile)
eaf.parse() 
eaf.eaf2solr()  
	 