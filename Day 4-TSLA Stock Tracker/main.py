from datetime import timedelta
import os

NEWS_API_KEY=os.environ["NEWS_API_KEY"]
STOCK_API_KEY=os.environ["STOCK_API_KEY"]
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT="https://newsapi.org/v2/everything"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
parameters={"function":"TIME_SERIES_DAILY","symbol":STOCK,"apikey":STOCK_API_KEY}
parameter={"q":COMPANY_NAME,"apikey":NEWS_API_KEY}

import datetime
yesterday=(datetime.datetime.now().date()-timedelta(1)).strftime("%Y-%m-%d")
day_before_yesterday=(datetime.datetime.now().date()-timedelta(2)).strftime("%Y-%m-%d")

import requests
def get_news():
    say=requests.get(url=NEWS_ENDPOINT,params=parameter)
    say.raise_for_status()
    file=say.json()
    news=file["articles"][:3]
    formatted_news=[]

    for article in news:
        title=article["title"]
        description=article["description"]
        formatted_news.append(
            f"Headline:{title}\nBrief:{description}"
        )
    return "\n\n".join(formatted_news)

from twilio.rest import Client
# Fetch credentials securely from GitHub Actions Repository Secrets
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]

response=requests.get(url=STOCK_ENDPOINT,params=parameters)
response.raise_for_status()
data=response.json()
if "Time Series (Daily)" not in data:
    print(data)
    raise Exception("Stock data not returned")
daily_data=data["Time Series (Daily)"]
daily_data_list=list(daily_data.keys())
daily_data=data["Time Series (Daily)"]
yesterday_close=float(daily_data[daily_data_list[0]]["4. close"])
day_before_yesterday_close=float(daily_data[daily_data_list[1]]["4. close"])
difference=yesterday_close-day_before_yesterday_close
value=(abs(difference)/day_before_yesterday_close)*100
if value >5:
    if difference>0:
        client = Client(account_sid,auth_token)
        message=client.messages.create(
            body=f"TSLA:🔺{value}%\n\n{get_news()}",
            from_="+18143240614",
            to="+916235958612"
        )
        print(message.body)
    elif difference<0:
        client=Client(account_sid,auth_token)
        message=client.messages.create(
            body=f"TSLA:🔻{value}%\n\n{get_news()}",
            from_="+18143240614",
            to="+916235958612"
        )
        print(message.body)