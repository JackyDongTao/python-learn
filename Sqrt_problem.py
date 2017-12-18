from math import sqrt #This code could be used to solve Sqrt problem.
n = input("Maximum Number? \n")
print("The number of groups that satisfy the Pythagorean theorem within ",n, "is:")
n = int(n)+1
for a in range(1,n):
    for b in range(a,n):
        c_square = a**2 + b**2
        c = int(sqrt(c_square))
        if ((c_square - c**2) == 0):
            print(a, b, c)                   