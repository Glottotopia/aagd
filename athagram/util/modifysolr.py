from wsgiref.simple_server import make_server 
from pyramid.config import Configurator
from pyramid.response import Response
from xml.etree  import ElementTree as ET 
import os
import string
import json
#import subprocess
import requests
 
from athagraf import Athagraf
from athahelpers import Language
import poioapi
from poioapi.io import typecraft, elan
import uuid 

import pprint


LGS = {'tau':Language('Upper_Tanana',  'tau','63.1377,-142.5244'),
'taa':Language('Lower_Tanana',  'taa','65.1577, -149.3765'),
'koy':Language('Koyukon',       'koy','64.8816,-157.7044')
}

METADATAURLS = {
    'tau':'https://www.dropbox.com/sh/be37fv36h53qm6k/AABJjgZTjbJHjNDWBRTqoteea/taumetadata.csv',
    'taa':'',
    'koy':'',
}
    
class IntegrityError(Exception):
    pass

class WrongFileFormatError(Exception):
    pass

class JSONError(Exception):
    pass

class DeprecationError(Exception):
    pass


def sanitize(s):
    return ''.join([x for x in s if x in '-_.'+string.ascii_letters+string.digits])
   
def updateSOLR(f):
    cmd = 'bash {postpath} {f}'.format(postpath='/usr/local/share/solr-atha/example/exampledocs/post.sh',f=f)
    print cmd
    os.system(cmd)
    

def add(request):  
    field = request.matchdict['field']
    value =  request.matchdict['value']
    ID =  request.matchdict['ID'] 
    doc = getDoc(ID) 
    print ID 
    print doc 
    print doc.get(field)
      
    
    
    try:
	doc[field].append(value) 
	doc[field] = list(set(doc[field]))
    except KeyError:
	doc[field] = [value]
    try:	
	result =  _copydoc(doc)
    except JSONError:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'JSONError'}), content_type='application/json')
    print result
    olduuid, newuuid, empty, deprecated = result
    return Response(body=json.dumps({'status':'success','msg':'added %s to %s (%s;%s)' %(value, field, olduuid, newuuid), 'empty':empty,'deprecated':deprecated} ), content_type='application/json')     
    
    
def delete(request):    
    field = request.matchdict['field']
    value =  request.matchdict['value']
    ID =  request.matchdict['ID']
    doc = getDoc(ID)
    try: 
	values = doc[field]
    except KeyError:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'Field %s not present in %s'%(field,ID)
					}), content_type='application/json')
    #updates of doc fields is handled here. Versioning is handled by _copydoc
    newvalues = list(set([v for v in values if v != value]))
    empty = False
    if len(newvalues) == 0:
	empty = True	
	del doc[field]
    else:
	doc[field] = newvalues 
    try:
	#result =  _copydoc(doc,'deleted %s from %s' % (value, field), empty=empty)
	result =  _copydoc(doc,empty=empty)
    except JSONError:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'JSONError'}), content_type='application/json')
    except DeprecationError:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'DeprecationError'}), content_type='application/json')
	
    olduuid, newuuid, empty, deprecated = result
    return Response(body=json.dumps({'status':'success','msg':'deleted %s form %s (%s;%s)' %(value, field, olduuid, newuuid), 'empty':empty,'deprecated':deprecated} ), content_type='application/json')     


	
   	     
def _copydoc(doc,empty=False):      
    olduuid  = doc.get("id") # better use getID(uuidlatest true)
    newuuid = str(uuid.uuid4())
    doc["version"] += 1
    print  doc["version"]
    doc["id"] = newuuid
    doc["latest"] = True
    doc["author_s"] = None
    doc["_version_"] = 0
    address  = "http://localhost:8983/solr/aagd/update?commit=true"
   
    data = {'add':{'doc':doc}}  
    print 1
    r = requests.post(address, data=json.dumps(data), headers={'content-type': 'application/json'})
    print 3
    try:
	retval = json.loads(r.text)['responseHeader']['status']
    except:
	raise JSONError 
    print retval
    if retval == 0:	
	deprecated = False
	print olduuid
	if olduuid != None: 
	    _deprecate(olduuid)
	    deprecated = True 
	return olduuid, newuuid, empty, deprecated
	#return Response(body=json.dumps({'status':'success','msg':'%s (%s;%s)' %(successmsg, olduuid, newuuid), 'empty':empty,'deprecated':deprecated} ), content_type='application/json') 
    if retval == 400:
	print json.loads(r.text)
	raise JSONError
    print json.loads(r.text)
    raise
    
    
	
def _deprecate(uuid):  
    """deprecates a doc when a modification is made and an updated copy is available"""
    
    print 5
    address = "http://localhost:8983/solr/aagd/update?commit=true"
    data = [{"id":uuid,"latest":{"set":False}}] 
    print data
    r = requests.post(address, data=json.dumps(data), headers={'content-type': 'application/json'})
    retval = json.loads(r.text)['responseHeader']['status']
    print json.loads(r.text)    
    if retval == 400:
	print json.loads(r.text)
	raise DeprecationError 
    if retval !=0:
	print json.loads(r.text)
	raise
    

def getDoc(ID): 
    ID = sanitize(ID) 
    getaddress = "http://localhost:8983/solr/aagd/query?q=athaid:%s+AND+latest:true"%ID
					    
					    
    print getaddress     
    r = requests.get(getaddress) 
    docs = json.loads(r.text)['response']['docs']
    if len(docs)==0:
	doc = None
    if len(docs)>1:
	print getaddress
	raise IntegrityError
    return docs[0]
    
   
def _transferfile(inputfn,input_file):  
    filetype = inputfn.split('.')[-1]
    if filetype != 'eaf':
	raise WrongFileFormatError(filetype)
    tmpdir = '%s'%uuid.uuid4() 
    os.mkdir(os.path.join('/tmp',tmpdir)) 
    file_path = os.path.join('/tmp',tmpdir,inputfn)
    # We first write to a temporary file to prevent incomplete files from
    # being used.
    temp_file_path = file_path + '~'
    output_file = open(temp_file_path, 'wb')
    # Finally write the data to a temporary file
    input_file.seek(0)
    while True:
	data = input_file.read(2<<16)
	if not data:
	    break
	output_file.write(data)          
    output_file.close()
    # Now that we know the file has been fully saved to disk move it into place.
    os.rename(temp_file_path, file_path) 
    return file_path
    
def convert(path):
    parser  =  poioapi.io.elan.Parser(path) 
    writer  =  poioapi.io.graf.Writer()
    converter  =  poioapi.io.graf.GrAFConverter(parser,  writer)
    converter.parse()
    converter.write("%s.hdr"%eafpath[:-4])
    
    
def put(request):     
    fn = request.POST['elanfile'].filename
    input_file = request.POST['elanfile'].file 
    lg = fn[:3].lower()
    try:
	language = LGS[lg]
    except KeyError:
	return Response(body=json.dumps({'status':'failure',
				'msg':u'File name must begin with a valid ISO639-3 code. Code found:%s'%lg}), 
				content_type='application/json')
    try:
	eafpath = _transferfile(fn, input_file)
    except WrongFileFormatError as e:
	return Response(body=json.dumps({'status':'failure',
				'msg':u'wrong file format. Expected: eaf. Found:%s'%e.args[0]}), 
				content_type='application/json')     
    try:
	convert(eafpath)
    except:
	return Response(body=json.dumps({'status':'failure',
				'msg':u'Unknown POIO conversion error'}), 
				content_type='application/json')
    try:	    
	athagraf = Athagraf(eafpath.replace('.eaf','-utterance.xml'), language,  metadataurl = METADATAURLS[lg])    
	athagraf.parse() 
	jsondata, ids = athagraf.graf2json()  
    except:
	return Response(body=json.dumps({'status':'failure',
				'msg':u'Unknown SOLR conversion error'}), 
				content_type='application/json')
	
    retvals = []
    for j in jsondata:
	try:
	    retvals.append((j['ID'],_copydoc(j)))
	except JSONError:
	    retvals.append((j['ID'],'error'))
	    
    retvals = [(j['ID'],_copydoc(j)) for j in jsondata]
    print retvals
    return Response(body=json.dumps({'status':'success',
				    'retvals':retvals}), 
				    content_type='application/json')
    
    


def set_(request):  
    #there is currently no way of checking whether the field to be changed should be allowed to be changed!!
    field = request.matchdict['field']
    value =  request.matchdict['value']
    ID =  request.matchdict['ID']
    ID = sanitize(ID) 
    address = "http://localhost:8983/solr/aagd/update?commit=true"
    data = [{"id":ID,"%s"%field:{"set":"%s"%value}}] 
    r = requests.post(address, data=json.dumps(data), headers={'content-type': 'application/json'})
    try:
	retval = json.loads(r.text)['responseHeader']['status']
    except:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'json error'}), content_type='application/json')
    if retval == 0:
	return Response(body=json.dumps({'status':'success','msg':u'Changed %s:%s to %s' % (ID,field,value)} ), content_type='application/json') 
    if retval == 400:
	msg = json.loads(r.text)['error']['msg']
	return Response(body=json.dumps({'status':'failure',
					    'msg':msg+data}), content_type='application/json')
    return Response(body=json.dumps({'status':'failure',
				    'msg':u'unknown error: %s'%retval}), 
				    content_type='application/json')    
    
 
	 

if __name__ == '__main__':
    config = Configurator()
    config.add_route('put', '/put')
    config.add_route('add', '/mod/add/{ID}/{field}/{value}')
    config.add_view(add, route_name='add')
    
    config.add_route('set_', '/mod/set/{ID}/{field}/{value}')
    config.add_view(set_, route_name='set_')
    
    config.add_route('delete', '/mod/delete/{ID}/{field}/{value}')
    config.add_view(delete, route_name='delete')
    
    app = config.make_wsgi_app() 
    server = make_server('0.0.0.0', 8086, app)
    server.serve_forever()
