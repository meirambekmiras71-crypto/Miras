with open("data.txt", "a") as file:
    file.write("Third line appended.\n")

with open("data.txt", "r") as file:
    updated_content = file.read()
    print(updated_content)