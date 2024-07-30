from twilio.rest import Client
from datetime import datetime


class NotificationManager:
    def __init__(self, account, auth, from_num, to_num):
        self.account_sid = account
        self.auth_token = auth
        self.from_number = from_num
        self.to_number = to_num

    def send_message(self, message):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            from_=self.from_number,
            body=message,
            to=self.to_number
        )
        print(message.sid)

    def format_message(self, flight_offer):
        price = flight_offer['price']['total']
        currency = flight_offer['price']['currency']
        itinerary = flight_offer['itineraries'][0]
        segments = itinerary['segments']

        departure_segment = segments[0]
        departure_city = departure_segment['departure']['iataCode']
        departure_time = departure_segment['departure']['at']

        arrival_segment = segments[-1]
        arrival_city = arrival_segment['arrival']['iataCode']
        arrival_time = arrival_segment['arrival']['at']

        departure_time = datetime.fromisoformat(departure_time).strftime('%Y-%m-%d %H:%M:%S')
        arrival_time = datetime.fromisoformat(arrival_time).strftime('%Y-%m-%d %H:%M:%S')

        message = (
            f"Flight Details:\n"
            f"From: {departure_city} (Departure Time: {departure_time})\n"
            f"To: {arrival_city} (Arrival Time: {arrival_time})\n"
            f"Price: {price} {currency}\n"
        )

        self.send_message(message)
