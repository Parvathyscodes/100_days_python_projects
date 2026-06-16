import requests
import datetime
import smtplib
import time
from config import(MY_LAT,MY_LONG,EMAIL,PASSWORD)

def overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return(MY_LAT-5<=iss_latitude<=MY_LAT+5 and MY_LONG-5<=iss_longitude<=MY_LONG+5)

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    sunrise=(sunrise+5)%24
    sunset=(sunset+5)%24
    current_hour=datetime.datetime.now().hour
    return(current_hour>=sunset or current_hour<= sunrise)

def send_mail():
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=EMAIL,password=PASSWORD)
        connection.sendmail(from_addr=EMAIL,to_addrs=EMAIL,msg="Subject:Look Up !\n\nThe ISS is above you in the sky !")

while True:
    time.sleep(60)
    print("checking ISS position")
    if is_night() and overhead():
        print("ISS overhead ! Sending your mail")
    else:
        print("Conditions not met.")