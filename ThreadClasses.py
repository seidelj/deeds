import os, sys, threading

class ThreadDownload(threading.Thread):
	def __init__(self, queue)
	threading.Thread.__init__(self)
	self.queue = queue

	def run(self):
		while True:
			
