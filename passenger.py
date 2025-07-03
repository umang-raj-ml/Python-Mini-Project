import re
from exceptions import InvalidPassportError

class Passenger:
    def __init__(self, name, passport_id):
        if not re.match(r'^[A-Z]{2}\d{7}$', passport_id):
            raise InvalidPassportError("Invalid passport format (must be 2 uppercase letters followed by 7 digits).")
        self.name = name
        self.__passport_id = passport_id
    

    @property
    def passport_id(self):
        return self.__passport_id
    def __str__(self):
        return f"Passenger(name={self.name}, passport_id={self.passport_id})"
    
