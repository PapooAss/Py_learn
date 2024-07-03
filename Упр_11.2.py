import math
def corner(a,b,c):
    X = math.acos((b**2+c**2-a**2)/(2*b*c))
    Degr = math.degrees(X)
    return Degr
a = int(input('Введите 1 сторону треугольника: '))
b = int(input('Введите 2 сторону треугольника: '))
c = int(input('Введите 3 сторону треугольника: '))
corn_a = round(corner(a,b,c),2)
corn_b = round(corner(b,a,c),2)
corn_c = round(corner(c,a,b),2)
print('Угол А=',corn_a,'Угол B=',corn_b,'Угол С=',corn_c)
print(corn_a+corn_b+corn_c)