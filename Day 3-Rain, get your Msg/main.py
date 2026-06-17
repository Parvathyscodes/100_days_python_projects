import os
import requests
from twilio.rest import Client

# Fetch credentials securely from GitHub Actions Repository Secrets
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
api_key = os.environ["API_KEY"]
twilio_number = os.environ["TWILIO_NUMBER"]
my_number = os.environ["MY_NUMBER"]

parameters = {
    "lat": 10.1960,
    "lon": 76.3860,
    "appid": api_key,
    "cnt": 4,
}
condition_codes = []

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()

for i in range(4):
    code = data["list"][i]["weather"][0]["id"]
    condition_codes.append(code)

# Standard Twilio initialization (No proxy needed on GitHub!)
client = Client(account_sid, auth_token)

for code in condition_codes:
    if int(code) >= 700:
        message = client.messages.create(
    body="Hey, It is going to rain today. Grab your umbrella!",
    from_=twilio_number,
    to=my_number,
)
        print(f"SMS Sent Successfully! Status: {message.status}")
        break
