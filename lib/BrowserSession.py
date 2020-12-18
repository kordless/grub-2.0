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


class BrowserSession:
    

    def __init__(self, url=None, persistent=False, debug=False):
        
        # currently the configuration is going to be config.json 
        # soon it will be from MongoDB/LocalBox

        self.debug = debug
        #Navigation
        self.url = url
        self.stayopen = False
        #BrowserSpecific
        self.headless = False
        self.fullscreen = True
        #CrawlSpecific
        self.local_db = None # stick to local socket
        self.local_index = None # somelocalIndex Store
        self.save_text = False

    def setup_session(self):

        self.config = json.loads(open('config.json', 'r').read()) 

        if self.headless:
            self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--headless')
            self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--height=1080')
            self.config['capabilities']['alwaysMatch']['moz:firefoxOptions']['args'].insert(1,'--width=1920')

        print(self.config['capabilities'])

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


    def save_screenshot(self,filename=None):
        if filename is None:
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
    
        
def main_test():
    new_session = BrowserSession()
    new_session.headless = True
    new_session.setup_session()
    #new_session.go_to_url('https://google.com/search?q=MLK',fullscreen=True)
    print("going for it")
    new_session.go_to_url('https://news.ycombinator.com/',fullscreen=True)
    # new_session.go_to_url('https://www.theguardian.com/us-news/2020/jul/05/trump-july-fourth-speech-rushmore-coronavirus-race-protests',fullscreen=True)
    print("waiting two seconds for page to load")
    time.sleep(2)
    new_session.save_screenshot()
    
if __name__ == '__main__':
    main_test()
