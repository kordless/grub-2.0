import os
import re

import datetime
import logging

import requests
import urllib
import json

from lib.browser import Session

from flask import Flask, render_template, make_response, request, abort

# app up
app = Flask(__name__)

@app.route('/g', methods=['POST'])
def grub():
	# build document
	document = {}
	
	# url
	url = request.form.get('url')

	if not url:
		abort(404, "go away")

	# snapshot page
	gbrowser = Session()
	browser.image_url(url)

	response = make_response(
		render_template(
			'grub.json',
			json = json.dumps({"result": "success", "document": document})
		)
	)
	return response

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
