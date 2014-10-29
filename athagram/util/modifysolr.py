from wsgiref.simple_server import make_server 
from pyramid.config import Configurator
from pyramid.response import Response
from xml.etree  import ElementTree as ET 
import os
import string
import json
#import subprocess
import requests

def sanitize(s):
    return ''.join([x for x in s if x in '-.'+string.ascii_letters+string.digits])
   
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
	return Response(body=json.dumps({'status':'success','msg':u'Added %s:%s to %s' % (field,value,ID)} ), content_type='application/json') 
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
    
    
    
    
    
 
	 

if __name__ == '__main__':
    config = Configurator()
    
    config.add_route('add', '/add/{ID}/{field}/{value}')
    #config.add_route('add', '/add')
    config.add_view(add, route_name='add')
    
    config.add_route('delete', '/delete/{ID}/{field}/{value}')
    config.add_view(delete, route_name='delete')
    
    
    app = config.make_wsgi_app() 
    server = make_server('0.0.0.0', 8086, app)
    server.serve_forever()
