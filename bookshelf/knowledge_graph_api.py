#https://www.googleapis.com/freebase/v1/topic/m/0h29c

import requests

KNOWLEDGE_GRAPH_RESULT_LIMIT = 10
print 'start req'
SERVICE_URL = 'https://www.googleapis.com/freebase/v1/topic'
topic_id = '/m/0d6lp' + "?limit=" + str(KNOWLEDGE_GRAPH_RESULT_LIMIT)


def get_from_freebase_knowledge_graph(machine_id):
	mid = machine_id
	if mid.startswith("/m"):
		url = SERVICE_URL + mid 
		response = requests.get(url)
		return response.json()
	else:
		raise ValueError("Invalid machine id(mid) provided. mid starts with /m. You provided " + mid)
	return None
