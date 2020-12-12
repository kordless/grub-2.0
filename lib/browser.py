#!/usr/bin/env python3
import webdriver
import json
import base64
import sys
import requests
import traceback
import logging
import time




# TODO Setup Interaction with DB rather than with flags and config files

# ideally we just want something like -> LookUpWord -> Provider -> Google
# ideally we just want something like -> go_to_url -> Cached/NotCached -> nytimes


# Explorer Mode
# Use Whois, Dig, nc, etc...
# Think of this like the Selenium but a true browser


class Session:
    
    def __init__(self, url=None, persistent=False, debug=False):
        
        # currently the configuration is going to be config.json 
        # soon it will be from MongoDB/LocalBox

        self.debug = debug

        self.url = url
        self.stayopen = False

        self.headless = True
        self.fullscreen = True

        self.local_db = None # stick to local socket
        self.local_index = None # somelocalIndex Store
        self.save_text = False
        self.headless = True
        self.session = webdriver.Session(self.config['webdriverip'], self.config['webdriverport'], capabilities=self.config['capabilities'])

        self.config = json.loads(open('lib/config.json', 'r').read()) 

        if self.headless:
            self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--headless')
            self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--height=1080')
            self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--width=1920')

    def image_url(self, url = None, fullscreen = True):

        print(self.config['capabilities'])

        if url is None:
            url = self.url 
        
        self.session.url = url
        if fullscreen:
            self.fullscreen=True
            self.session.window.fullscreen()
        if self.debug:
            print("WebDriver to sessionID -------> {}".format(self.session.session_id))

        filename = "ss_{:.0f}.png".format(time.time())
        print("Full Filename to use:\n\n")
        print(filename + "\n\n")

        try:
            if self.fullscreen:
                r = requests.get(url="http://localhost:4444/session/" + self.session.session_id + "/moz/screenshot/full")
                print(r.status_code)
            else:
                r = requests.get(url="http://localhost:4444/session/" + self.session.session_id + "/screenshot")
            if r.status_code == 200:
                try:
        
                    with open(filename, 'wb') as screenshot:
                        screenshot.write(base64.b64decode(r.json()['value']))
                except IOError as err:
                    print("I/O error: {0}".format(err))
            elif r.status_code == 404:
                print("Something is wrong with the session? maybe it's closed????")
                print(r.json())

        except Exception:
            traceback.print_exc()
            pass

        return "all functions return things, joe"
    
        
def main_test():
    new_session = Session()
    
    new_session.image_url('https://news.ycombinator.com',fullscreen=True)
    
    time.sleep(2)
    
    new_session.save_screenshot()
    
if __name__ == '__main__':
    main_test()
