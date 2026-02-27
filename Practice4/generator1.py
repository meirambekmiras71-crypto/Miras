def square_generator(n):
    for i in range(n + 1):
        yield i ** 2

x = int(input())

for sq in square_generator(x):
    print(sq)