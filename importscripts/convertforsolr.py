import sys
from athagraf import Athagraf
from athahelpers import Language

lgs = {'tau':Language('Upper_Tanana',  'tau','63.1377,-142.5244'),
	'taa':Language('Lower_Tanana',  'taa','65.1577, -149.3765'),
	'koy':Language('Koyukon',       'koy','64.8816,-157.7044')
	}
	
f = sys.argv[1]
lg = f.split('/')[0]
metadatafile = '/'.join((lg,'metadata.csv')) 
 
athagraf = Athagraf(f, lgs[lg],  metadatafile = metadatafile)
athagraf.parse() 
athagraf.graf2solr()  
#print athagraf.graf2json()	 