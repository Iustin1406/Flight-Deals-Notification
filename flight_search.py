import requests
from flight_data import FlightData


class FlightSearch:
    def __init__(self, key, secret, code):
        self.api_key = key
        self.api_secret = secret
        self.home_code = code
        self.token = self.get_access_token()

    def get_access_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        if 'access_token' in response_data:
            return response_data['access_token']
        else:
            raise Exception(f"Failed to get access token: {response_data}")

    def search_flights(self, flight_data: FlightData, departure_date):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        params = {
            "originLocationCode": self.home_code,
            "destinationLocationCode": flight_data.iata_code,
            "departureDate": departure_date,
            "adults": 1,
            "maxPrice": flight_data.lowest_price,
            "max": 20
        }
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        if "data" not in response_data or not response_data["data"]:
            return None

        flights = response_data["data"]

        if not flights:
            return None

        cheapest_flight = flights[0]
        # print(flights)
        for flight in flights:
            if float(flight["price"]["total"]) < float(cheapest_flight["price"]["total"]):
                cheapest_flight = flight

        return cheapest_flight
