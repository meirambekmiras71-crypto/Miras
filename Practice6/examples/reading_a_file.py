file_name = "sample.txt"

with open(file_name, "r") as file:
    content = file.read()
    print(content)