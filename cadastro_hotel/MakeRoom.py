from abc import ABC, abstractmethod


# A interface desse ser implementada pelas classes quartos(single, delux,...)
class MakeRoom(ABC):

    def __init__(self, room_number, price):
        self.room_number = room_number
        self.price = price
    
    @abstractmethod
    def room(self):
        pass

# Classes produto, onde herdam a classe abstrata MakeRoom
class StandardRoom(MakeRoom):
    def __init__(self, room_number, price):
        super().__init__(room_number, price)

    def room(self):
        return f"StandardRoom {self.room_number} e preço {self.price}"
    
class DeluxeRoom(MakeRoom):
    def __init__(self, room_number, price):
        super().__init__(room_number, price)

    def room(self):
        return f"DeluxRoom {self.room_number} e preço {self.price}"
    
class SuiteRoom(MakeRoom):
    def __init__(self, room_number, price):
        super().__init__(room_number, price)

    def room(self):
        return f"SuiteRoom {self.room_number} e preço {self.price}"
    
class RoomFactory:
    @staticmethod
    def create_room(room_type, room_number):
        if room_type == "standard":
            return StandardRoom(room_number)
        elif room_type == "deluxe":
            return DeluxeRoom(room_number)
        elif room_type == "suite":
            return SuiteRoom(room_number)
        else:
            raise ValueError(f"Room type {room_type} is not recognized.")


room1 = RoomFactory.create_room("standard", 101)
room2 = RoomFactory.create_room("suite", 202)

print(room1.room())  # Output: Standard Room 101 booked at 100.
print(room2.room())  # Output: Suite Room 202 booked at 500.
