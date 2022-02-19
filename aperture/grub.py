import os
import re
import time

import datetime
import logging

import requests
import urllib
import json

import sys
from subprocess import Popen

from flask import Flask, render_template, make_response, request, abort, send_from_directory

# app up
app = Flask(__name__)


# main route
@app.route('/g', methods=['POST'])
def grub():
	# url, upload_url and user_token from appengine
	url = request.form.get('url')
	upload_url = request.form.get('upload_url')
	api_token = request.form.get('api_token')
	sidekick_name = request.form.get('sidekick_name')
	doc_id = request.form.get('doc_id')

	if not url or not upload_url or not api_token:
		abort(404, "go away")

	# don't allow any quotes in the URL
	if '"' in url or "'" in url:
		abort(404, "go away")

	
	# killing joe over and over again, for safety
	p = Popen([
		"python3", 
		"/opt/grub-2.0/aperture/BrowserSession.py", 
		"%s" % url,
		"%s" % upload_url,
		"%s" % api_token,
		"%s" % sidekick_name,
		"%s" % doc_id
	])

	# reponse to appengine
	response = make_response(
		render_template(
			'grub.json',
			json = json.dumps({"result": "success",	"upload_url": upload_url})
		)
	)

	return response


@app.route('/h', methods=['GET'])
def health_check():
	return "OK"


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
	app.run(host='0.0.0.0', port=7070, debug=True)
