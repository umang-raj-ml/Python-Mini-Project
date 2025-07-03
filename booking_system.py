import datetime
from exceptions import SeatNotAvailableError

class BookingSystem:
    def __init__(self, log_file="booking_log.txt"):
        self.flights = {}
        self.log_file = log_file

    def book_seat(self, flight_number, passenger, seat_no=None):
        flight = self.flights.get(flight_number)
        if flight:
            try:
                result = flight.add_passenger(passenger, seat_no)
                self._log_transaction(result, flight_number, passenger.passport_id)
                print(f"{passenger.name} has been {result.lower()} on flight {flight_number}.")
            except SeatNotAvailableError as e:
                print(f"Booking failed: {e}")
        else:
            print("Flight not found.")

    def cancel_booking(self, flight_number, passport_id):
        flight = self.flights.get(flight_number)
        if flight and flight.remove_passenger(passport_id):
            self._log_transaction("CANCELLED", flight_number, passport_id)
            print("Booking cancelled.")
        else:
            print("Cancellation failed. Passenger not found.")

    def _log_transaction(self, action, flight_number, passport_id):
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()} | {action} | {flight_number} | {passport_id}\n")

    def display_flights(self):
        print("\n=== Available Flights ===")
        for flight in self.flights.values():
            print(f"{flight.flight_number} {flight.source} to {flight.destination} "
                  f"({len(flight.passengers)}/{flight.total_seats} booked)")
