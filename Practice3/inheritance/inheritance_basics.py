class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Some sound"


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def speak(self):
        return "Meow"


a = Animal("Creature")
d = Dog("Buddy")
c = Cat("Whiskers")

print(a.name, a.speak())
print(d.name, d.speak())
print(c.name, c.speak())
