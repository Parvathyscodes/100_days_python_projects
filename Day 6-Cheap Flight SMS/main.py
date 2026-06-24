from data_manager import DataManager
from flight_data import FlightData

data_manager=DataManager()
flight_data=FlightData()
sheet_data=data_manager.get_rows()
print(sheet_data)
for row in sheet_data:
    flight_data.get_details(row)


