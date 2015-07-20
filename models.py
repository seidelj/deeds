from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
import time, sys, os

engine = create_engine('postgresql://postgres:joseph@localhost/deeds')
Base = declarative_base()
Session = sessionmaker(bind=engine)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(PROJECT_DIR, 'download')


class HouseHold(Base):
	__tablename__ = 'household'
	id = Column(Integer, Sequence("household_id_seq"), primary_key=True)
	pin = Column(String)

	def split_pin(self):
		box0 = self.pin[0:2]
		box1 = self.pin[2:4]
		box2 = self.pin[4:7]
		box3 = self.pin[7:10]
		box4 = self.pin[10:]
		
		pinlist = [box0, box1, box2, box3, box4]
		return pinlist
	
	def get_total_rows(self, browser):
		total_rows = browser.find_elements_by_id('SearchInfo1_ACSLabel_SearchResultCount.cssLabelText').text
		return int(total_rows.replace(" ",""))

	def search_pin(self, browser):
		if len(self.pin) != 14:
			return False
		else:
			input_id = "SearchFormEx1_PINTextBox"
			sb0 = browser.find_element_by_id("{}0".format(input_id))
			sb1 = browser.find_element_by_id("{}1".format(input_id))
			sb2 = browser.find_element_by_id("{}2".format(input_id))
			sb3 = browser.find_element_by_id("{}3".format(input_id))
			sb4 = browser.find_element_by_id("{}4".format(input_id))
		
			for x in range(0,5):
				browser.find_element_by_id("{}{}".format(input_id, x)).sendkeys(self.split_pin[x])
			browser.find_element_by_id('SearchFormEx1_btnSearch')
			return True

	def show_all_results(self, browser):
		total_rows = self.get_total_rows(browser)
		if total_rows <= 20:
			browser.find_element_by_id('DocList1_PageView20Btn').click()
		elif 20 < total_rows <= 50:
			browser.find_element_by_id('DocList1_PageView50Btn').click()
		elif 50 < total_rows:
			browser.find_element_by_id('DocList1_PageView100Btn').click()
		else:
			sys.exit("Could not determine quantity of results")

	def save_file(self, filename, html):
		try:
			with open(filename, 'w') as f:
				f.write(html)
		except IOError:
			print "Could not write to file {}".format(filename)

	def download(self, browser):
		num_of_rows = self.get_total_rows(browser)
		for x in range(0, num_of_rows):
			link = browser.find_element_by_id('DocList1_GridView_Document_ctl{}_ButtonRow_PIN_{}'.format(x + 2, x))
			document_no = browser.find_element_by_id('DocList1_GridView_Document_ctl02_ButtonRow_Doc. #_{}'.format(x))
			filename = document_no.replace(" ","") + self.pin
			filename = os.path.join(DOWNLOAD_FOLDER, "{}.html".format(filename))
			if not os.path.exists(filename):
				link.click()
				time.sleep(1)
				html = browser.page_source
				self.save_file(filename, html)
			else:
				print "Already downloaded {}".format(filename)
		
class Record(Base):
	
	__tablename__ = 'record'
	id = Column(Integer, Sequence("record_id_seq"), primary_key=True)
	document_no = Column(String)
	executed = Column(String)
	recorded = Column(String)
	document_type = Column(String)
	case_no = Column(String)
	amount = Column(String)

	household_id = Column(Integer, ForeignKey('household.id'))
	household = relationship("HouseHold", backref=backref('record', order_by=id))

Base.metadata.create_all(engine)
