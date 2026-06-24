import os
import requests
from dotenv import load_dotenv
load_dotenv()
SHEETY_API = os.environ["SHEETY_API_GET"]

class DataManager:
    def get_rows(self):
        responses = requests.get(url=SHEETY_API)
        responses.raise_for_status()
        data = responses.json()
        return data["sheet1"]
