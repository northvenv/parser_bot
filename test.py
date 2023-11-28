def f():
    return (1, 2)

z, x = f()[0], f()[1]
print(z, x)