class Vehicle:
    def move(self):
        return "The vehicle is moving"


class Car(Vehicle):
    def move(self):
        return "The car is driving"


class Bicycle(Vehicle):
    def move(self):
        return "The bicycle is pedaling"


v = Vehicle()
c = Car()
b = Bicycle()

print(v.move())
print(c.move())
print(b.move())
