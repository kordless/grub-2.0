import datetime
import logging
import os
import re

import requests
import urllib
import json

from flask import Flask, render_template, request, abort

# app up
app = Flask(__name__)

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


@app.route('/g', methods=['POST'])
def grub():
	try:
		request_token = request.args.get('token')
	except:
		request_token = ""

	if request_token == token:
		print("we're good")
	else:
		abort(404, description="resource not found")

	# build document
	document = {}
	
	response = make_response(
		render_template(
			'grub.json',
			json = json.dumps({"result": "success", "document": document})
		)
	)

@app.errorhandler(404)
def f404_notfound(e):
	logging.info("here")
	return "404 not found <a href='/'>exit</a>", 404


@app.errorhandler(500)
def server_error(e):
	# handle a 404 too!
	logging.exception('An error occurred during a request.')
	return "An error occured and this is the fail.".format(e), 500


if __name__ == '__main__':
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.
	app.run(host='0.0.0.0', port=7070, debug=True)
