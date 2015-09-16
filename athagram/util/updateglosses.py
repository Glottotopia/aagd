import re
import glob
import requests
import json

UPPERCASE = re.compile('^[A-Z0-9\.]+$')

for f in  glob.glob('/root/solrimport/*'):
    ID = f.split('/')[-1][:-4] 
    
    r = requests.get('http://localhost:8983/solr/athagram/get?id=%s'%ID,  headers={'content-type': 'application/json'})
    doc = None
    try:
	doc = json.loads(r.text)['doc']
	glosses = doc['gloss']
    except KeyError: 
	continue 
    grammaticalglosses = [g for g in glosses if UPPERCASE.match(g)]
    lexicalglosses = [g for g in glosses if not UPPERCASE.match(g)] 
	
    address = "http://localhost:8983/solr/athagram/update?commit=true"
    data = [{"id":ID,
	    "lexicalgloss" :{"set":lexicalglosses}, 
	    "grammaticalgloss" :{"set":grammaticalglosses} 
	    }] 
    print data
    r = requests.post(address, data=json.dumps(data), headers={'content-type': 'application/json'})
	