from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirualdisplay import Display
from models import HouseHold, Record, Session

URL = "http://12.218.239.82/i2/default.aspx?AspxAutoDetectCookieSupport=1"

session = Session()

def main():
	create_download_folder()
	for hh in session.query(HouseHold).all():
		browser.get(
		hh.

def create_download_folder():
	if not os.path.isdir(DOWNLOAD_FOLDER):
		print "Making {}".format(DOWNLOAD_FOLDER)
		os.mkdir(DOWNLOAD_FOLDER)
