import os
import re
import time

import datetime
import logging

import requests
import urllib
import json

import sys
from subprocess import check_output

from flask import Flask, render_template, make_response, request, abort, send_from_directory

# app up
app = Flask(__name__)

"""
# serving images
@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('/opt/grub-2.0/aperture/images/', path)
"""

# main route
@app.route('/g', methods=['POST'])
def grub():
	# url, upload_url and user_token from appengine
	url = request.form.get('url')
	upload_url = request.form.get('upload_url')
	api_token = request.form.get('api_token')

	if not url or not upload_url or not api_token:
		abort(404, "go away")

	# killing joe over and over again, for softly
	filename = check_output(["python3", "/opt/grub-2.0/aperture/BrowserSession.py", "%s" % url])

	# upload to the spool endpoint
	with open(r'/opt/grub-2.0/aperture/images/%s' % str(filename),'rb') as filedata:
		appengine_response = requests.post(
			"%s?token=%s" % (upload_url, api_token),
			files={'file': filedata}
		)

	print(appengine_response.text)

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
