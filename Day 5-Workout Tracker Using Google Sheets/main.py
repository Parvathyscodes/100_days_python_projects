from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()

# ---------- ENV ----------
NUTRITION_API_ID = os.getenv("NUTRITION_API_ID")
NUTRITION_API_KEY = os.getenv("NUTRITION_API_KEY")
MY_TOKEN = os.getenv("MY_TOKEN")
SHEETY_API = os.getenv("SHEETY_API")

GENDER = os.getenv("GENDER")
WEIGHT_KG = os.getenv("WEIGHT_KG")
HEIGHT_CM = os.getenv("HEIGHT_CM")
AGE = os.getenv("AGE")

# ---------- INPUT ----------
exercise_text = input("What exercise did you perform today? ")

# ---------- NUTRITION API ----------
headers = {
    "x-app-id": NUTRITION_API_ID,
    "x-app-key": NUTRITION_API_KEY
}

params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": int(WEIGHT_KG),
    "height_cm": int(HEIGHT_CM),
    "age": int(AGE)
}

response = requests.post(
    "https://app.100daysofpython.dev/v1/nutrition/natural/exercise",
    json=params,
    headers=headers
)

result = response.json()

# ---------- DATE/TIME ----------
today_date = datetime.datetime.now().strftime("%d/%m/%Y")
today_time = datetime.datetime.now().strftime("%X")

# ---------- SHEETY ----------
bearer_header = {
    "Authorization": f"Bearer {MY_TOKEN}"
}

# ---------- SAVE TO GOOGLE SHEET ----------
if "exercises" in result:
    for exercise in result["exercises"]:
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": today_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        sheet_response = requests.post(
            url=SHEETY_API,
            json=sheet_inputs,
            headers=bearer_header
        )

        print(sheet_response.text)
else:
    print("API error:", result)