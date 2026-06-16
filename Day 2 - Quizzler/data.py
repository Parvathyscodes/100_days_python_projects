from xmlrpc.client import boolean

import requests

parameters={"amount":10,"type":"boolean","category":18}
responses=requests.get(url="https://opentdb.com/api.php",params=parameters)
responses.raise_for_status()
data=responses.json()
question_data=data["results"]