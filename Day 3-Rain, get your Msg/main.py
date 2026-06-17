import os
import requests
from twilio.rest import Client

# Fetch credentials securely from GitHub Actions Repository Secrets
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
api_key = os.environ["API_KEY"]

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
            body="Hey, It's gonna rain today. Grab your umbrella!",
            from_="+18143240614",  # Your Twilio Trial Number
            to="+919497026123",    # Your Verified Phone Number
        )
        print(f"SMS Sent Successfully! Status: {message.status}")
        break