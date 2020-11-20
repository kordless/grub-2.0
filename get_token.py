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
user www-data;
worker_processes auto;
pid /run/nginx.pid;
events {
        worker_connections 768;
        # multi_accept on;
}
http {
        server {
                listen  8389;
                location / {
                        auth_basic "solr";
                        auth_basic_user_file /etc/nginx/htpasswd
                        proxy_pass http://localhost:8983/;
                }
        }
}
""" % token

f = open("/etc/nginx/nginx.conf", "w")
f.write(config)
