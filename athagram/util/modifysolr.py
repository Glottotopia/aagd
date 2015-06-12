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

class WrongFileFormatError(Exception):
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
    ID = sanitize(ID) 
    address = "http://localhost:8983/solr/aagd/update?commit=true"
    data = [{"id":ID,"%s"%field:{"add":"%s"%value}}] 
    r = requests.post(address, data=json.dumps(data), headers={'content-type': 'application/json'})
    try:
	retval = json.loads(r.text)['responseHeader']['status']
    except:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'json error'}), content_type='application/json')
    if retval == 0:
	return Response(body=json.dumps({'status':'success','msg':u'Added %s:%s to %s' % (ID,field,value)} ), content_type='application/json') 
    if retval == 400:
	msg = json.loads(r.text)['error']['msg']
	return Response(body=json.dumps({'status':'failure',
					    'msg':msg}), content_type='application/json')
    return Response(body=json.dumps({'status':'failure',
				    'msg':u'unknown error: %s'%retval}), 
				    content_type='application/json')
	
   	     

def mod(request):  
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
					    'msg':msg}), content_type='application/json')
    return Response(body=json.dumps({'status':'failure',
				    'msg':u'unknown error: %s'%retval}), 
				    content_type='application/json')
	
   	 
    
def delete(request):    
    field = request.matchdict['field']
    value =  request.matchdict['value']
    ID =  request.matchdict['ID']
    ID = sanitize(ID) 
    getaddress = "http://localhost:8983/solr/aagd/get?id=%s"%ID
    r = requests.get(getaddress)
    doc = None
    try:
	doc = json.loads(r.text)['doc']
    except:
	pass
    try:
	values = doc[field]
    except KeyError:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'Field %s not present in %s'%(field,ID)
					}), content_type='application/json')
    if value not in values:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'Value %s not present in %s'%(value,ID)
					}), content_type='application/json')
    newvalues = [v for v in values if v != value]
    empty = False
    if len(newvalues) == 0:
	empty = True
    address = "http://localhost:8983/solr/aagd/update?commit=true"
    data = [{"id":ID,"%s"%field:{"set":newvalues}}] 
    
    r = requests.post(address, data=json.dumps(data), headers={'content-type': 'application/json'})
    try:
	retval = json.loads(r.text)['responseHeader']['status']
    except:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'json error'}), content_type='application/json')
    if retval == 0:
	return Response(body=json.dumps({'status':'success','msg':u'Deleted %s:%s from %s' % (field,value,ID), 'empty':empty} ), content_type='application/json') 
    if retval == 400:
	msg = json.loads(r.text)['error']['msg']
	return Response(body=json.dumps({'status':'failure',
					    'msg':msg}), content_type='application/json')
    return Response(body=json.dumps({'status':'failure',
				    'msg':u'unknown error: %s'%retval}), 
				    content_type='application/json')
    
    
   
def put(request):    
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
    

    lgs = {'tau':Language('Upper_Tanana',  'tau','63.1377,-142.5244'),
    'taa':Language('Lower_Tanana',  'taa','65.1577, -149.3765'),
    'koy':Language('Koyukon',       'koy','64.8816,-157.7044')
    }
    
    fn = request.POST['elanfile'].filename
    input_file = request.POST['elanfile'].file 
    lg = fn[:3].lower()
    try:
	eafpath = _transferfile(fn, input_file)
    except WrongFileFormatError as e:
	return Response(body=json.dumps({'status':'failure',
				'msg':u'wrong file format. Expected: eaf. Found:%s'%e.args[0]}), 
				content_type='application/json')
    
    parser  =  poioapi.io.elan.Parser(eafpath) 
    writer  =  poioapi.io.graf.Writer()
    try:
	converter  =  poioapi.io.graf.GrAFConverter(parser,  writer)
	converter.parse()
	converter.write("%s.hdr"%eafpath[:-4])
    except:
	return Response(body=json.dumps({'status':'failure',
				'msg':u'Unknown conversion error'}), 
				content_type='application/json')
	
    try:
	language = lgs[lg]
    except KeyError:
	return Response(body=json.dumps({'status':'failure',
				'msg':u'File name must begin with a valid ISO639-3 code. Code found:%s'%lg}), 
				content_type='application/json')
	
    athagraf = Athagraf(eafpath.replace('.eaf','-utterance.xml'), language,  metadatafile = '%s/metadata.csv'%lg)
    
    athagraf.parse() 
    jsondata, ids = athagraf.graf2json()   
    #print jsondata
	
    updateaddress = "http://localhost:8983/solr/aagd/update?commit=true" 
    
    r = requests.post(updateaddress, jsondata, headers={'content-type': 'application/json'})
    try:
	retval = json.loads(r.text)['responseHeader']['status']
    except:
	return Response(body=json.dumps({'status':'failure',
					'msg':u'json error'}), content_type='application/json')
    if retval == 0:
	return Response(body=json.dumps({'status':'success',
					'msg':u'uploaded %s with %i IDs' % (fn,len(ids)),
					'ids':sorted(ids)}), content_type='application/json') 
    if retval == 400:
	msg = json.loads(r.text)['error']['msg']
	return Response(body=json.dumps({'status':'failure',
					    'msg':msg}), content_type='application/json')
    return Response(body=json.dumps({'status':'failure',
				    'msg':u'unknown error: %s'%retval}), 
				    content_type='application/json')
    
    
    
    
 
	 

if __name__ == '__main__':
    config = Configurator()
    
    config.add_route('add', '/add/{ID}/{field}/{value}')
    #config.add_route('add', '/add')
    config.add_view(add, route_name='add')
    
    config.add_route('delete', '/delete/{ID}/{field}/{value}')
    config.add_view(delete, route_name='delete')
    
    config.add_route('put', '/put')
    config.add_view(put, route_name='put')
    
    
    app = config.make_wsgi_app() 
    server = make_server('0.0.0.0', 8086, app)
    server.serve_forever()
