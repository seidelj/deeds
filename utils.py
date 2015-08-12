import Queue
def qdumper(q):
	try:
		while 1:
			yield q.get(False)
	except Queue.Empty:
		pass


