
def page_query(q):
	offset = 0
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


