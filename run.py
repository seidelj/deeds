from sqlutils import page_query
import os, time, argparse
#from pyvirtualdisplay import Display
from models import HouseHold, Record, Session
import Queue
from threadclasses import ThreadDownload
from utils import qdumper
import atexit
import threading
import pickle

#display = Display(visible=0, size=(800,600))
#display.start()
URL = "http://12.218.239.82/i2/default.aspx?AspxAutoDetectCookieSupport=1"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(PROJECT_DIR, 'download')

session = Session()

def exit_handler():
	print _queue.qsize()
	remaining = [item for item in qdumper(_queue)]
	pickle.dump(remaining, open("queue.p", "wb"))

def main(args):
	if not args.STARTING_ID:
		STARTING_ID = 0
	else:
		STARTING_ID = args.STARTING_ID
	create_download_folder()
	global _queue
	_queue = Queue.Queue()
	qfile = os.path.join(PROJECT_DIR, 'queue.p')
	if os.path.isfile(qfile):
		queue = pickle.load(open(qfile))
		for item in queue:
			_queue.put(item)
	else:
		for hh in session.query(HouseHold).filter(HouseHold.id >= STARTING_ID).order_by(HouseHold.id):
			_queue.put(hh)
	
	for i in range(20):
		td = ThreadDownload(_queue, URL)
		td.setDaemon(True)
		td.start()
		
	while threading.active_count() > 0:
		time.sleep(0.1)
	
	_queue.join()
	
	print "Finished?"
		

def create_download_folder():
	if not os.path.isdir(DOWNLOAD_FOLDER):
		print "Making {}".format(DOWNLOAD_FOLDER)
		os.mkdir(DOWNLOAD_FOLDER)


atexit.register(exit_handler)
if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = "Optional to specify ID to begin on",
		add_help = False,
		usage = "%(prog)s [options]"
	)
	parser.add_argument(
		"-i","--id",
		dest = "STARTING_ID",
		metavar = "<number>",
		help = "hh.id to begin on",
		required = False,
		type = int,
	)
	
	main(parser.parse_args())

