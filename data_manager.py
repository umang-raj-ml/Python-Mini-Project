import os
from flight import Flight

class FlightDataManager:
    def __init__(self, storage_folder="flights"):
        self.storage_folder = storage_folder
        os.makedirs(storage_folder, exist_ok=True)

    def save_all_flights(self, flights):
        for flight in flights.values():
            flight.save_to_file()

    def load_all_flights(self):
        flights = {}
        for filename in os.listdir(self.storage_folder):
            if filename.endswith(".json"):
                path = os.path.join(self.storage_folder, filename)
                flight = Flight.load_from_file(path)
                flights[flight.flight_number] = flight
        return flights
