import requests
import datetime
import os
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
HOME_CODE = os.getenv('HOME_CODE')
SHEETY_URL = os.getenv('SHEETY_URL')
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
FROM_NUMBER = os.getenv('FROM_NUMBER')
TO_NUMBER = os.getenv('TO_NUMBER')

response = requests.get(url=SHEETY_URL)
data = response.json()["prices"]  # list of dict containing flight info

# initialize flights data
flights = [FlightData(flight["city"], flight["iataCode"], flight["lowestPrice"]) for flight in data]
flights_manager = FlightSearch(API_KEY, API_SECRET, HOME_CODE)

# check flights deals for the next 6 months
start_date = datetime.date.today()
end_date = start_date + datetime.timedelta(days=6*30)
message = NotificationManager(ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER)

while start_date <= end_date:
    start_date += datetime.timedelta(days=1)
    for flight in flights:
        response = flights_manager.search_flights(flight, start_date)  # returns a dictionary
        if response:
            message.format_message(response)
