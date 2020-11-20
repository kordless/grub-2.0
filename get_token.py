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

config = """
%s
""" % token

print(config)
