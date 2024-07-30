class FlightData:
    def __init__(self, name: str, code: str, price: int):
        self.city_name = name
        self.iata_code = code
        self.lowest_price = price
