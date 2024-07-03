def Vpiramid (A,h):
    return (A**2)*h/3
Vmax = Vpiramid(150,49)
Vmin = Vpiramid(22,7)
print('Объем пирамиды: ', round(Vmax-Vmin), 'м3')
