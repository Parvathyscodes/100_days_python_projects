from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
ACCOUNT_ID=os.environ["ACCOUNT_SID"]
ACCOUNT_KEY=os.environ["AUTH_TOKEN"]
MY_NUMBER=os.environ["TWILIO_NUMBER"]
SEND_TO=os.environ["MY_NUMBER"]

class NotificationManager:
    def send_sms(self,departure_id, arrival_id, airline, cheapest_price, destination):
        client=Client(ACCOUNT_ID,ACCOUNT_KEY)
        message=client.messages.create(
            body=f"CHEAP FLIGHT FOUND from {departure_id} to {arrival_id} for {airline}! "
                 f"{destination} for ₹{cheapest_price}",
            from_=MY_NUMBER,
            to=SEND_TO)
        print(message.body)