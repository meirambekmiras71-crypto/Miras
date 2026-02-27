def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

x, y = int(input()), int(input())

for val in squares(x, y):
    print(val)