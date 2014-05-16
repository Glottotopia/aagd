import sys
from athautils import EAF, Language, AthaSOLR, template, getAdditions

lgs = {'ut':Language('Upper_Tanana',  'tau','63.1377,-142.5244'),
	'lt':Language('Lower_Tanana',  'taa','65.1577, -149.3765'),
	'koy':Language('Koyukon',       'koy','64.8816,-157.7044')
	}
	
f = sys.argv[1]
lg = lgs[sys.argv[2]]

orig='eaf'
eaf = EAF(f, lg, orig=orig)
eaf.parse(orig=orig) 
eaf.eaf2solr(orig=orig)  
	 