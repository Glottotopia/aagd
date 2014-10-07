import sys
from athagraf import Athagraf
from athahelpers import Language

lgs = {'tau':Language('Upper_Tanana',  'tau','63.1377,-142.5244'),
	'taa':Language('Lower_Tanana',  'taa','65.1577, -149.3765'),
	'koy':Language('Koyukon',       'koy','64.8816,-157.7044')
	}
	
f = sys.argv[1]
lg = lgs[sys.argv[2]]
metadatafile = sys.argv[3]
 
athagraf = Athagraf(f, lg,  metadatafile = metadatafile)
athagraf.parse() 
athagraf.graf2solr()  
	 