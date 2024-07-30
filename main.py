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
SHEETY_USERS_URL = os.getenv('SHEETY_USERS_URL')
PASSWORD = os.getenv('PASSWORD')
FROM_EMAIL = os.getenv('FROM_EMAIL')

# get the users from google sheet
response_users = requests.get(url=SHEETY_USERS_URL)
users_data = response_users.json()["users"]
users_list = [
    {
        "name": user["whatIsYourFirstName?"],
        "email": user["whatIsYourEmail?"]
    }
    for user in users_data
]

response = requests.get(url=SHEETY_URL)
data = response.json()["prices"]  # list of dict containing flight info

# initialize flights data
flights = [FlightData(flight["city"], flight["iataCode"], flight["lowestPrice"]) for flight in data]
flights_manager = FlightSearch(API_KEY, API_SECRET, HOME_CODE)

# check flights deals for the next 6 months
start_date = datetime.date.today()
end_date = start_date + datetime.timedelta(days=6 * 30)
message = NotificationManager(ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER)

while start_date <= end_date:
    start_date += datetime.timedelta(days=1)
    for flight in flights:
        response = flights_manager.search_flights(flight, start_date)  # returns a dictionary
        if response:
            formatted_message = message.format_message(response)
            message.send_message(formatted_message)
            for user in users_list:
                message.send_email(user["name"], user["email"], formatted_message, PASSWORD, FROM_EMAIL)
