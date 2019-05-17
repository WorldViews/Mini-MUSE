"""
Must install selenium and a driver for the desired kind of browswer
"""
import time, traceback
import MUSEClient

class Client(MUSEClient.MUSEClient):
    def onMessage(self, msg):
        print "***** ", msg
        try:
            self.onMessage_(msg)
        except:
            traceback.print_exc()

    def onMessage_(self, msg):
        print "***** ", msg
        if msg['type'] == 'setDisplayURL':
            url = msg['url']
            print "URL:", url
            self.browser.get(url)

from selenium import webdriver

browser = webdriver.Chrome()
urls = [
    'http://seleniumhq.org/',
    'http://palweb',
    'http://fxpal.com',
    'http://youtube.com'
    ]

client = Client()
client.browser = browser
client.runInThread()

for url in urls:
    browser.get(url)
    time.sleep(8)
    
