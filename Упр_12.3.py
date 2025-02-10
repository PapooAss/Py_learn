a = int(input("Введите 1 число:"))
b = int(input("Введите 2 число:"))


def gcd(a, b):
    if a == b:
        return (b)
    else:
        if a < b:
            return (gcd(a, b - a))
        else:
            return (gcd(a - b, b))


print(gcd(a, b))
