#https://www.googleapis.com/freebase/v1/topic/m/0h29c

import requests

SERVICE_URL = 'https://www.googleapis.com/freebase/v1/topic'

def get_from_freebase_knowledge_graph(machine_id):
	mid = machine_id
	if mid.startswith("/m"):
		url = SERVICE_URL + mid + "?filter=/common/topic"
		response = requests.get(url)
		return response.json()
	else:
		raise ValueError("Invalid machine id(mid) provided. mid starts with /m. You provided " + mid)
	return None
