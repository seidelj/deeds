import os, sys, threading, time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

PROXY = "52.10.218.136:3128"
proxy = webdriver.Proxy({
	'httpProxy':PROXY,
	'ftpProxy':PROXY,
	'noProxy':None,
	'proxyType': ProxyType.MANUAL,
})
class ThreadDownload(threading.Thread):
	def __init__(self, queue, url):
		threading.Thread.__init__(self)
		self.queue = queue
		self.url = url

	def run(self):
		while True:
			b = False
			while not b:
				try:
					browser = webdriver.Firefox()
				except WebDriverException:
					print "could not open remote driver"
				else:
					b = True	
			browser.set_window_size(1440,900)
			browser.implicitly_wait(10)
			browser.get(self.url)
			hh = self.queue.get()
			go = hh.search_pin(browser)
			if go == True:
				hh.show_all_results(browser)
				try:
					hh.download(browser)
				except StaleElementReferenceException:
					time.sleep(2)
					hh.download(browser)
			print hh.id
			browser.quit()
			self.queue.task_done()
		
