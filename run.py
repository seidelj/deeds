from sqlutils import page_query
from selenium import webdriver
import os, time, argparse
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from models import HouseHold, Record, Session
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

display = Display(visible=0, size=(800,600))
#display.start()
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
	for hh in session.query(HouseHold).filter(HouseHold.id >= STARTING_ID).order_by(HouseHold.id):
		print hh.id
		browser = webdriver.Firefox()	
		browser.implicitly_wait(5)
		browser.get(URL)
		go = hh.search_pin(browser)
		print go
		if go == True:
			try:
				browser.find_element_by_id("MessageBoxCtrl1_ErrorLabel1")
			except NoSuchElementException:
				hh.show_all_results(browser)
				try:
					hh.download(browser)
				except StaleElementReferenceException:
					time.sleep(2)
					hh.download(browser)
			else:
				browser.quit()
				continue

		browser.quit()

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
