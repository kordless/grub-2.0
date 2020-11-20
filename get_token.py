#!/usr/bin/python3

# get the token from gcp tag on instance
import httplib2
http = httplib2.Http()
url = 'http://metadata.google.internal/computeMetadata/v1/instance/tags'
headers = {'Metadata-Flavor': 'Google'}
response, content = http.request(url, 'GET', headers=headers)
evalcontent = eval(content)
for item in evalcontent:
	if 'token' in item:
		key,token = item.split('-')

token = "solr"
config = 
"""
{
"authentication":{ 
   "blockUnknown": true, 
   "class":"solr.BasicAuthPlugin",
   "credentials":{"%s":"IV0EHq1OnNrj6gvRCwvFwTrZ1+z1oBbnQdiVC3otuq0= Ndd7LKvVBAaZIF0QAVi1ekCfAJXr1GGfLtRUXhgrF8c="}, 
   "realm":"purelands", 
   "forwardCredentials": false 
}
""" % token

f = open("security.json")
f.write(config)
