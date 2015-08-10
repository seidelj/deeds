import os, sys, threading
from selenium import webdriver
from selenium.common.exceptions import StateElementReferenceException

class ThreadDownload(threading.Thread):
	def __init__(self, queue, url):
		threading.Thread.__init(self)
		self.queue = queue
		self.url = url
	
	def run(self):
		while True:
			hh = self.queue
			browser = webdriver.FireFox()
			browser.implicitely_wait(5)
			browser.get(self.url)
			go = hh.search_pin(browser)
			if go == True:
				hh.show_all_results(browser)
				try:
					hh.download(browser)
				except StaleElementReferenceException:
					time.sleep(2)
					hh.download(browser)
					browser.quit()
			print hh.id
			self.queue.task_done()
		
