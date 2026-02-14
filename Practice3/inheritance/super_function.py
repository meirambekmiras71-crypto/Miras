class Person:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        return f"My name is {self.name}"


class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

    def introduce(self):
        base_intro = super().introduce()
        return f"{base_intro} and I am in grade {self.grade}"


s = Student("Alice", 10)

print(s.introduce())
