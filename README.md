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
	cd [installation directory]
	bin\solr.cmd start -f -m 2g -p 8938
	
The application will then be available at localhost:8983

To adjust poort, hostname and other parameters, please refer to 

Users
=====

There are two default users
admin / fireweed
athabasca / fireweed


Roles
=====
aagd there are two roles, aagd-admin and aagd-user.

admin has role aagd-admin
athabasca has role aagd-user


User Management
===============

aagd supports assigning username and password via 

	org.eclipse.jetty.security.HashLoginService
	
to add a new user first get the password hashes

	cd [installation directory]\server
	java -cp lib\jetty-util-9.2.11.v20150529.jar org.eclipse.jetty.util.security.Password [username] [securePassword]
	
Select your prefered hash from the resulting output:
	
	s3cr3t
	OBF:1yta19bz1v8w1v9q19bz1ytc
	MD5:a4d80eac9ab26a4a2da04125bc2c096a
	CRYPT:li6YN5PVerMyI 
	
and add one line per user to the file name\[:ALGORYTHM:HASH]\[,ROLE1]\[,ROLE2]
	
	[installation directory]\server\etc\realm.properties
		
See also jetty doc http://www.eclipse.org/jetty/documentation/9.2.6.v20141205/configuring-security-authentication.html

Partial Update
==============

Instead of downloading the archive you can update the configuration using git. Be aware, that local changes will be overwritten

	cd /home/solr/aagdSolrPackage/server/solr/aagd
	git clone https://github.com/Glottotopia/aagd.git
	
	