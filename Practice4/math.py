import math
# 1
a = int(input("Input degree: "))
print("Output radian:", math.radians(a))
# 2
h, b, c = int(input("Height: ")), int(input("Base, first value: ")), int(input("Base, second value: "))
print("Expected Output:", h*((b+c)/2))
# 3
d, e = int(input("Input number of sides: ")), int(input("Input the length of a side: "))
print("The area of the polygon is:", int((d * e**2) / (4 * math.tan(math.pi / d))))
# 4
f, g = int(input("Length of base: ")), int(input("Height of parallelogram: "))
print("Expected Output:", f*g)
