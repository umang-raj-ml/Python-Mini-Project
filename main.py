# main.py - CLI-based Flight Booking System (Starts with predefined flights and allows search)

import re
from booking_system import BookingSystem
from flight import Flight
from passenger import Passenger
from exceptions import InvalidPassportError, SeatNotAvailableError
from data_manager import FlightDataManager

system = BookingSystem()
manager = FlightDataManager()

# Load flights from files if available
loaded_flights = manager.load_all_flights()
if loaded_flights:
    system.flights.update(loaded_flights)

# Predefined Indian flights
predefined_flights = [
    ("AI101", "Delhi", "Mumbai", 2),
    ("IX202", "Bangalore", "Delhi", 5),
    ("SG303", "Hyderabad", "Kolkata", 5),
    ("UK404", "Chennai", "Bangalore", 5),
    ("AI505", "Mumbai", "Goa", 5)
]

for code, src, dest, seats in predefined_flights:
    if code not in system.flights:
        system.flights[code] = Flight(code, dest, seats)
        system.flights[code].source = src

def menu():
    print("\n===== Flight Booking System =====")
    print("1. Search Flights")
    print("2. Book a Seat")
    print("3. Cancel a Booking")
    print("4. View All Flights")
    print("5. View Passengers in a Flight")
    print("6. Save All Flights to File")
    print("7. Exit")
    return input("Choose an option: ")

def search_flights():
    src = input("From: ").strip().title()
    dest = input("To: ").strip().title()
    found = False
    for f in system.flights.values():
        if getattr(f, 'source', '').title() == src and f.destination.title() == dest:
            print(f"{f.flight_number}: {src} -> {dest} ({len(f.passengers)}/{f.total_seats} booked)")
            found = True
    if not found:
        print("No flights found between those cities.")

def book_seat():
    src = input("From: ").strip().title()
    dest = input("To: ").strip().title()
    available_flights = [
        f for f in system.flights.values()
        if getattr(f, 'source', '').title() == src and f.destination.title() == dest
    ]

    if not available_flights:
        print("No flights found for the given route.")
        return

    print("Available Flights:")
    for i, f in enumerate(available_flights, start=1):
        print(f"{i}. {f.flight_number} ({len(f.passengers)}/{f.total_seats} booked)")

    try:
        choice = int(input("Choose a flight number from above list (e.g., 1): "))
        selected_flight = available_flights[choice - 1]

        num_passengers = int(input("How many passengers do you want to book for? "))
        if num_passengers <= 0:
            print("Booking cancelled.")
            return

        seats_left = selected_flight.total_seats - len(selected_flight.passengers)
        use_waitlist = False

        if seats_left <= 0:
            print("All seats are booked for this flight.")
            ask = input("Do you want to add all to the waiting list? (y/n): ").strip().lower()
            if ask != "y":
                print("Booking cancelled.")
                return
            use_waitlist = True

        for i in range(num_passengers):
            print(f"\n--- Booking for Passenger #{i + 1} ---")
            name = input("Passenger Name: ")
            passport = input("Passport ID (2 letters + 7 digits): ").upper()
            p = Passenger(name, passport)

            seat = None
            if not use_waitlist and len(selected_flight.passengers) < selected_flight.total_seats:
                while True:
                    seat = input("Seat Number (1A–1E or leave blank for waiting list): ") or None
                    if seat:
                        if not re.match(r"^1[A-E]$", seat.upper()):
                            print("Invalid seat number. Only 1A to 1E allowed.")
                            continue
                        seat = seat.upper()

                    try:
                        result = selected_flight.add_passenger(p, seat)
                        print(f"{p.name} → Booking successful: {result}")
                        break
                    except SeatNotAvailableError:
                        print("Seat already taken.")
                        retry = input("Do you want to choose another seat? (y/n): ").strip().lower()
                        if retry != 'y':
                            wait_choice = input("Do you want to be added to the waiting list? (y/n): ").strip().lower()
                            if wait_choice == 'y':
                                result = selected_flight.add_passenger(p, None)
                                print(f"{p.name} → Waitlisted.")
                            else:
                                print(f"{p.name} → Booking skipped.")
                            break
                    except Exception as e:
                        print(f"{p.name} → Booking failed:", e)
                        break
            else:
                try:
                    result = selected_flight.add_passenger(p, None)
                    print(f"{p.name} → Booking successful: {result}")
                except Exception as e:
                    print(f"{p.name} → Booking failed:", e)

    except (IndexError, ValueError):
        print("Invalid input.")
    except InvalidPassportError as e:
        print("Error:", e)

def cancel_booking():
    flight_no = input("Flight Number: ").upper()
    passport = input("Passport ID: ").upper()
    system.cancel_booking(flight_no, passport)

def view_flights():
    system.display_flights()

def view_passengers():
    flight_no = input("Flight Number: ").upper()
    if flight_no in system.flights:
        system.flights[flight_no].display_passengers()
    else:
        print("Flight not found.")

def save_all():
    manager.save_all_flights(system.flights)
    print("Flights saved to files.")

if __name__ == "__main__":
    while True:
        choice = menu()
        if choice == "1":
            search_flights()
        elif choice == "2":
            book_seat()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            view_flights()
        elif choice == "5":
            view_passengers()
        elif choice == "6":
            save_all()
        elif choice == "7":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")