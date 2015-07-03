import time
#import urllib2
#import requests
import subprocess
import os
#import cookielib, urllib2

class MetadataError(ValueError):
    pass

class MetadataRecord:
    def __init__(self, ID, params): 
	self.ID = ID 
	self.lg = params[0] 
	self.dialect = params[1] 
	self.speakers = params[2].split(';') 
	self.sources = params[3].split(';') 
	self.recordingname = params[4]  
	try:
	    self.recordingdate = time.strftime("%Y-%m-%e",time.strptime(params[5].strip(),"%d-%b-%y"))+"T12:00:00Z/DAY"#choosing noon for unknown time
	except ValueError: 
	    #self.recordingdate = time.strftime("%Y-%m-%e",time.strptime("01-Jan-70","%d-%b-%y"))+"T12:00:00Z/DAY"
	    self.recordingdate = False
	self.recordinglinguists = params[6].split(';') 
	self.anlalink = params[7] 
	self.editedbyspeaker = False
	if params[8].lower() == 'Y':
	    self.editedbyspeaker = True
	self.editedbylinguist = False
	if params[9].lower() == 'Y':
	    self.editedbylinguist = True 
	self.texttypes = params[10].split(';')
	self.rejectedbyspeaker = False
	if params[11].lower() == 'Y':
	    self.rejectedbyspeaker = True  
	    
    def toSOLRstring(self):	    
	singlevalues = """<field name="aagdID">{ID}</field>
<field name="lg">{lg}</field>
<field name="dialect">{dialect}</field>
<field name="recordingname">{recordingname}</field>
<field name="anlalink">{anlalink}</field>
<field name="editedbyspeaker">{editedbyspeaker}</field>
<field name="editedbylinguist">{editedbylinguist}</field>
<field name="rejectedbyspeaker">{rejectedbyspeaker}</field>""".format(**self.__dict__)

	if self.recordingdate:
	    singlevalues += """\n<field name="recordingdate">%s</field>"""%self.recordingdate

	speakers = '\n'.join(['<field name="speaker">%s</field>'%spkr for spkr in self.speakers])
	sources = '\n'.join(['<field name="source">%s</field>'%src for src in self.sources])
	recordinglinguists = '\n'.join(['<field name="recordinglinguist">%s</field>'%rl for rl in self.recordinglinguists])
	texttypes = '\n'.join(['<field name="texttype">%s</field>'%tt for tt in self.texttypes]) 
	s = ''.join((singlevalues,speakers,sources,recordinglinguists,texttypes)) 
	return s

class Metadata:
    def __init__(self,csvfile,url):
	self.chunks = {} 
	if csvfile != None:
	    lines = open(csvfile).readlines()[1:] #drop first line where the labels are  
	else:  
	    #syscall = "wget %s" % url #urllib2 has problems with cookies
	    #print syscall
	    subprocess.call(["wget", "-O" "metadatafile", url])
	    #cj = cookielib.CookieJar()
	    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	    #urllib2.install_opener(opener)
	    #f = urllib2.urlopen(url)
	    lines = open('metadatafile').readlines()[1:]
	    os.remove("metadatafile")

	print lines
	for line in lines:
	    fields = line.split('\t')
	    ID = fields[0]
	    self.chunks[ID] = MetadataRecord(ID,fields[1:])
	     
	
class Language:
    def __init__(self,name,iso,coords):
	self.name=name
	self.iso=iso
	self.coords=coords
	

