def countdown(n):
    while n >= 0:
        yield n
        n -= 1

x = int(input())

for number in countdown(x):
    print(number)