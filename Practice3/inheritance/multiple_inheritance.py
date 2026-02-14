class Engine:
    def start(self):
        return "Engine started"


class Wheels:
    def roll(self):
        return "Wheels rolling"


class Car(Engine, Wheels):
    def drive(self):
        return "Car is driving"


c = Car()

print(c.start())
print(c.roll())
print(c.drive())
