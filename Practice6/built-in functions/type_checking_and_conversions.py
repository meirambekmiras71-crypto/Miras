raw_data = "150"

if isinstance(raw_data, str):
    converted_data = int(raw_data)

print(type(converted_data))
print(converted_data + 50)

items_tuple = (1, 2, 3)
items_list = list(items_tuple)
items_list.append(4)
print(items_list)