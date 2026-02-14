class Student:
    school_name = "Green Valley High"
    student_count = 0

    def __init__(self, name):
        self.name = name
        Student.student_count += 1

    def info(self):
        return f"{self.name} studies at {Student.school_name}"


s1 = Student("Alice")
s2 = Student("Bob")

print(s1.info())
print(s2.info())
print(Student.student_count)
print(Student.school_name)
