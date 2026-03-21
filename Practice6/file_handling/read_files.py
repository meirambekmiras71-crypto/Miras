filename = "data.txt"

with open(filename, "w") as file:
    file.write("First line of data.\n")
    file.write("Second line of data.\n")

with open(filename, "r") as file:
    content = file.read()
    print(content)