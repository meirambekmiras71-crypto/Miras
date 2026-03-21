fruits = ["apple", "banana", "cherry"]
counts = [10, 20, 30]

for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")

for fruit, count in zip(fruits, counts):
    print(f"We have {count} {fruit}s")