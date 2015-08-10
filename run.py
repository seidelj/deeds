from sqlutils import page_query
from selenium import webdriver
import os, time, argparse
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from models import HouseHold, Record, Session
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import Queue
from threadclasses import ThreadDownload

display = Display(visible=0, size=(800,600))
display.start()
URL = "http://12.218.239.82/i2/default.aspx?AspxAutoDetectCookieSupport=1"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(PROJECT_DIR, 'download')

session = Session()

def main(args):
	if not args.STARTING_ID:
		STARTING_ID = 0
	else:
		STARTING_ID = args.STARTING_ID
	create_download_folder()
	queue = Queue.Queue()
	for hh in session.query(HouseHold).filter(HouseHold.id >= STARTING_ID).order_by(HouseHold.id):
		queue.put(hh)
	for i in range(100):
		td = ThreadDownload(queue)
		td.setDaemon(true)
		pt.start()
	
	queue.join()
	print "Finished?"
	


def create_download_folder():
	if not os.path.isdir(DOWNLOAD_FOLDER):
		print "Making {}".format(DOWNLOAD_FOLDER)
		os.mkdir(DOWNLOAD_FOLDER)

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
	main()
