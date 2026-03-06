import re

#  Python program that matches a string that has an 'a' followed by zero or more 'b''s.
def exercise_1(text):
    return re.findall(r'ab*', text)

# Python program that matches a string that has an 'a' followed by two to three 'b'.
def exercise_2(text):
    return re.findall(r'ab{2,3}', text)

# Python program to find sequences of lowercase letters joined with a underscore.
def exercise_3(text):
    return re.findall(r'[a-z]+_[a-z]+', text)

# Python program to find the sequences of one upper case letter followed by lower case letters.
def exercise_4(text):
    return re.findall(r'[A-Z][a-z]+', text)

# Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
def exercise_5(text):
    return re.findall(r'a.*b', text)

# Python program to replace all occurrences of space, comma, or dot with a colon.
def exercise_6(text):
    return re.sub(r'[ ,.]', ':', text)

# python program to convert snake case string to camel case string.
def exercise_7(text):
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), text)

# Python program to split a string at uppercase letters.
def exercise_8(text):
    return re.findall(r'[A-Z][^A-Z]*', text)

# Python program to insert spaces between words starting with capital letters.
def exercise_9(text):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)

# Python program to convert a given camel case string to snake case.
def exercise_10(text):
    return re.sub(r'(?<=[a-z])([A-Z])', lambda m: '_' + m.group(1).lower(), text)


text = "abbc hello_world CamelCaseString foo.bar, baz"

print("\n=== Exercise 1: Match 'a' followed by zero or more 'b's ===")
print(exercise_1(text))

print("\n=== Exercise 2: Match 'a' followed by two to three 'b's ===")
print(exercise_2(text))

print("\n=== Exercise 3: Find lowercase sequences joined with underscore ===")
print(exercise_3(text))

print("\n=== Exercise 4: Find one uppercase letter followed by lowercase letters ===")
print(exercise_4(text))

print("\n=== Exercise 5: Match 'a' followed by anything ending in 'b' ===")
print(exercise_5(text))

print("\n=== Exercise 6: Replace spaces, commas, and dots with colons ===")
print(exercise_6(text))

print("\n=== Exercise 7: Convert snake_case to camelCase ===")
print(exercise_7(text))

print("\n=== Exercise 8: Split string at uppercase letters ===")
print(exercise_8(text))

print("\n=== Exercise 9: Insert spaces before capital letters ===")
print(exercise_9(text))

print("\n=== Exercise 10: Convert camelCase to snake_case ===")
print(exercise_10(text))