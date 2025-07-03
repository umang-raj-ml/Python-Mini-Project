import re
import json
from collections import deque
from passenger import Passenger
from exceptions import InvalidFlightNumberError, SeatNotAvailableError

class Flight:
    def __init__(self, flight_number, destination, total_seats):
        if not re.match(r'^[A-Z]{2}\d{3}$', flight_number):
            raise InvalidFlightNumberError("Invalid flight number format (must be 2 letters + 3 digits).")
        self.flight_number = flight_number
        self.destination = destination
        self.total_seats = total_seats
        self.passengers = []
        self.seat_assignments = {}
        self.waiting_list = deque()

    def add_passenger(self, passenger, seat_no=None):
        if len(self.passengers) < self.total_seats:
            if seat_no in self.seat_assignments:
                raise SeatNotAvailableError("Seat already booked.")
            self.passengers.append(passenger)
            self.seat_assignments[seat_no] = passenger
            return "BOOKED"
        else:
            self.waiting_list.append(passenger)
            return "WAITLISTED"

    def remove_passenger(self, passport_id):
        for seat, passenger in list(self.seat_assignments.items()):
            if passenger.passport_id == passport_id:
                self.passengers.remove(passenger)
                del self.seat_assignments[seat]
                if self.waiting_list:
                    next_passenger = self.waiting_list.popleft()
                    self.passengers.append(next_passenger)
                    self.seat_assignments[seat] = next_passenger
                    print(f"{next_passenger.name} promoted from waiting list to seat {seat}.")
                return True
        for p in list(self.waiting_list):
            if p.passport_id == passport_id:
                self.waiting_list.remove(p)
                return True
        return False

    def display_passengers(self):
        print(f"\nFlight: {self.flight_number} to {self.destination}")
        print("=== Seat Assignments ===")
        for seat, passenger in self.seat_assignments.items():
            print(f"Seat {seat}: {passenger}")
        print("\n=== Waiting List ===")
        for idx, passenger in enumerate(self.waiting_list, 1):
            print(f"{idx}. {passenger}")

    def save_to_file(self):
        data = {
            "flight_number": self.flight_number,
            "destination": self.destination,
            "total_seats": self.total_seats,
            "seat_assignments": {
                seat: {"name": p.name, "passport_id": p.passport_id}
                for seat, p in self.seat_assignments.items()
            },
            "waiting_list": [
                {"name": p.name, "passport_id": p.passport_id}
                for p in self.waiting_list
            ]
        }
        with open(f"flights/{self.flight_number}.json", "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        flight = cls(data["flight_number"], data["destination"], data["total_seats"])
        for seat, p_info in data["seat_assignments"].items():
            passenger = Passenger(p_info["name"], p_info["passport_id"])
            flight.passengers.append(passenger)
            flight.seat_assignments[seat] = passenger
        for p_info in data.get("waiting_list", []):
            passenger = Passenger(p_info["name"], p_info["passport_id"])
            flight.waiting_list.append(passenger)
        return flight
