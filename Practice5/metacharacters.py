import re

text = "Hello World! Price: $99.99, Dates: 2023-01-15, Email: test@mail.com"

pattern = r"[aeiou]"
result = re.findall(pattern, "Hello World")
print(f"[] → {result}")

pattern = r"\d+"
result = re.findall(pattern, text)
print(f"\\ → {result}")

pattern = r"H.llo"
result = re.findall(pattern, text)
print(f". → {result}")

pattern = r"^Hello"
result = re.findall(pattern, text)
print(f"^ → {result}")

pattern = r"com$"
result = re.findall(pattern, text)
print(f"$ → {result}")

pattern = r"lo*"
result = re.findall(pattern, "l lo loo looo")
print(f"* → {result}")

pattern = r"lo+"
result = re.findall(pattern, "l lo loo looo")
print(f"+ → {result}")

pattern = r"colou?r"
result = re.findall(pattern, "color colour")
print(f"? → {result}")

pattern = r"\d{4}"
result = re.findall(pattern, text)
print(f"{{}} → {result}")

pattern = r"cat|dog|bird"
result = re.findall(pattern, "I have a cat and a dog")
print(f"| → {result}")

pattern = r"(\d{4})-(\d{2})-(\d{2})"
result = re.search(pattern, text)
if result:
    print(f"() → {result.group(1)}, {result.group(2)}, {result.group(3)}")