import requests
import os
from notification_manager import NotificationManager
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime,timedelta
FLIGHT_URL=os.environ["FLIGHT_GET_URL"]
FLIGHT_API_KEY=os.environ["FLIGHT_KEY"]
notifier = NotificationManager()

class FlightData:
    def get_details(self,row):
        tomorrow = datetime.now() + timedelta(days=30)
        six_month_later = tomorrow + timedelta(days=7)
        results = {
            "engine": "google_flights",
            "departure_id": "COK",
            "arrival_id":row["iataCodes"],
            "currency": "INR",
            "type": "1",
            "outbound_date": tomorrow.strftime("%Y-%m-%d"),
            "return_date": six_month_later.strftime("%Y-%m-%d"),
            "api_key":FLIGHT_API_KEY
        }
        response=requests.get(url=FLIGHT_URL,params=results)
        response.raise_for_status()
        file=response.json()
        if len(file["best_flights"])==0:
            print(f"No flights found for {row['destination']}")
            return
        cheapest_flight = file["best_flights"][0]

        departure_id = cheapest_flight["flights"][0]["departure_airport"]["id"]
        arrival_id = cheapest_flight["flights"][0]["arrival_airport"]["id"]
        airline = cheapest_flight["flights"][0]["airline"]
        cheapest_price = cheapest_flight["price"]

        if cheapest_price < row["lowestPrice"]:
            notifier.send_sms(
                departure_id=departure_id,
                arrival_id=arrival_id,
                airline=airline,
                cheapest_price=cheapest_price,
                destination=row["destination"]
            )