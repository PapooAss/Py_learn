h = 1  #высота шайбы в мм
mu = 8.5  #г/см3
D = int(input('Введите наружный диаметр шайбы (мм): '))
d = int(input('Введите внутренний диаметр шайбы (мм): '))
def vol (d, D, h):
    S = ((3.14*D**2)/4*h)-((3.14*d**2)/4*h)
    M = S*mu/1000
    return M
print('Вес шайбы: ', vol(d,D,h))