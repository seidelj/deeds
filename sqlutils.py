from sqlalchemy.sql.expression import ClauseElement
import csv, os
import pandas as pd
from sqlalachemy import *

def page_query(q):
	offset = 0:
	while True:
		r = False
		elemList = []
		for elem in q.limit(1000).offset(offset):
			r = True
			elemList.append(elem)
		yield elemList
		offset += 1000
		if not r:
			break


