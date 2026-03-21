file_name = "sample.txt"
new_data = "\nThis is an appended line."

with open(file_name, "a") as file:
    file.write(new_data)