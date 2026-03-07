import re

text = "The rain in Spain stays mainly in the plain"

result = re.findall(r"\AThe", text)
print(f"\\A → {result}")  # Match at the beginning of the string

result = re.findall(r"\bain", text)
print(f"\\b (start) → {result}")  # Match at the beginning of a word

result = re.findall(r"ain\b", text)
print(f"\\b (end) → {result}")  # Match at the end of a word

result = re.findall(r"\Bain", text)
print(f"\\B (start) → {result}")  # Match NOT at the beginning of a word

result = re.findall(r"ain\B", text)
print(f"\\B (end) → {result}")  # Match NOT at the end of a word

result = re.findall(r"\d", "Room 101, Floor 3")
print(f"\\d → {result}")  # Match any digit (0-9)

result = re.findall(r"\D", "Room 101")
print(f"\\D → {result}")  # Match any non-digit character

result = re.findall(r"\s", text)
print(f"\\s → {result}")  # Match any whitespace character

result = re.findall(r"\S", "Hi there")
print(f"\\S → {result}")  # Match any non-whitespace character

result = re.findall(r"\w", "Hello_123!")
print(f"\\w → {result}")  # Match any word character (a-z, A-Z, 0-9, _)

result = re.findall(r"\W", "Hello_123!")
print(f"\\W → {result}")  # Match any non-word character

result = re.findall(r"Spain\Z", text)
print(f"\\Z → {result}")  # Match at the end of the string