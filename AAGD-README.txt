About
=====
AAGD in read-only mode. 
Needs java 7 
Current Solr Version : 5.3

Installation
============
Unpack the Zip-Archive to a directory of your choice.


Usage 
=====
Run 
	cd [installation directoy]
	bin\solr.cmd start -f -m 2g -p 8938
	
The application will then be available at localhost:8983

To adjust poort, hostname and other parameters, please refer to 


Partial Update
==============

Instead of downloading the archive you can update the configuration using git. Be aware, that local changes will be overwritten

	cd [installation directory]
	git clone https://github.com/Glottotopia/aagd.git
	
