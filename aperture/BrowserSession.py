#!/usr/bin/env python3
import sys
import time
import json
import base64
import string
import random

import traceback
import logging

import webdriver
import requests


def random_string(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


class BrowserSession:
	
	def __init__(self, url=None, persistent=False, debug=False):

		self.debug = debug
		self.url = url
		self.stayopen = False
		self.headless = False
		self.fullscreen = True
		self.local_db = None
		self.local_index = None
		self.save_text = False

	def setup_session(self, offset=0):

		self.config = json.loads(open('config.json', 'r').read())

		# randomly pick a port to try - if it's running we'll throw an error down at the bottom
		self.config['webdriverport'] = 4444 + offset

		if self.headless:
			self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--headless')
			self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--height=1080')
			self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--width=1920')

		self.session = webdriver.Session(self.config['webdriverip'], self.config['webdriverport'], capabilities=self.config['capabilities'])

		return


	def go_to_url(self,url=None,fullscreen=True):

		if url is None:
			url = self.url 
		
		self.session.url = url
		if fullscreen:
			self.fullscreen=True
			self.session.window.fullscreen()
		if self.debug:
			print("WebDriver to sessionID -------> {}".format(self.session.session_id))

		return


	def save_screenshot(self,filename=None,offset=0):
		if filename is None:
			filename = "%s.png" % random_string(23)

			if self.debug:
				print("filename="+filename)
				print("in debug")

		try:
			port = 4444 + offset
			if self.fullscreen:
				r = requests.get(url="http://localhost:"+"%s"%port+"/session/" + self.session.session_id + "/moz/screenshot/full")
			else:
				r = requests.get(url="http://localhost:"+"%s"%port+"/session/" + self.session.session_id + "/screenshot")
			if r.status_code == 200:
				try:
					with open("/opt/grub-2.0/aperture/images/%s" % filename, 'wb') as screenshot:
						screenshot.write(base64.b64decode(r.json()['value']))
				except IOError as err:
					print("I/O error: {0}".format(err))
			elif r.status_code == 404:
				if self.debug:
					print("Something is wrong with the session? maybe it's closed????")
					print(r.json())

		except Exception:
			print("got exception")
			traceback.print_exc()
			pass

		# upload to the spool endpoint
		# always return image/png
		url = "%s?token=%s&sidekick_name=%s&document_id=%s" % (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]) 
		files = [('images', (filename, open("/opt/grub-2.0/aperture/images/%s" % filename.rstrip('\r\n'), 'rb'), 'image/png'))]
		response = requests.request("POST", url, files = files)

		file_object = open('/opt/grub-2.0/aperture/mitta_API_Upload.log', 'a')
		file_object.write(response.text)
		file_object.close()

		return response.text
	
		
def main():
	error_count = 0
	yeah = True
	while yeah:
		try:
			new_session = BrowserSession()
			new_session.headless = True

			# randomize who we pick, if we pick wrong we'll drop to the except below
			offset = random.randrange(5)
			new_session.setup_session(offset=offset)

			new_session.go_to_url(sys.argv[1], fullscreen=True)

			time.sleep(3)
			filename = new_session.save_screenshot(offset=offset)

			# we got something, so leave the loop
			yeah = False

		except Exception as ex:
			# probably have a session	
			print("error %s" % ex)
			time.sleep(1) # hang out for a second

			# leave if it isn't going to work after 10 times (keeps many from being created)
			error_count = error_count + 1
			if error_count > 10:
				yeah = False

if __name__ == '__main__':
	main()
