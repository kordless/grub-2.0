#!/usr/bin/python3

# get token from gcp tag
import httplib2
http = httplib2.Http()
url = 'http://metadata.google.internal/computeMetadata/v1/instance/tags'
headers = {'Metadata-Flavor': 'Google'}
response, content = http.request(url, 'GET', headers=headers)
evalcontent = eval(content)
for item in evalcontent:
	if 'token' in item:
		key,token = item.split('-')

# run it
import os

user = sys.argv[1]
os.system("/usr/bin/htpasswd -b -c /etc/nginx/htpasswd %s %s" % (user, token))

