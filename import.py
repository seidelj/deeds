from sqlalchemy.sql.expression import ClauseElement
import csv, os
from models import Session, HouseHold

session = Session()

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
	filename = os.path.join(PROJECT_DIR, 'pins.csv')
	import_to_sql(filename)

def import_to_sql(filename):
	with open(filename, 'rb') as f:
		mycsv = csv.reader(f)
		next(mycsv, None)
		for row in mycsv:
			try:
				pin = row[0]
			except IndexError:
				continue
			else:
				household = get_or_create(session, HouseHold, pin=pin)
		session.commit()	

def get_or_create(session, model, defaults=None, **kwargs):
	instance = session.query(model).filter_by(**kwargs).first()
	if instance:
		return instance, False

	else:
		params = dict((k,v) for k,v in kwargs.iteritems() if not isinstance(v, ClauseElement))
		params.update(defaults or {})
		instance = model(**params)
		session.add(instance)
		return instance, True

if __name__ == "__main__":
	main()
