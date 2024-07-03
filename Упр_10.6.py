diff = 1.0
x0 = 3
x1 = 4
def Fun(x):
    return 1.24*x**5+0.12689*x**2-100.45*x-36.235
while diff >= 0.02:
    F0 = Fun(x0)
    F1 = Fun(x1)
    x01 = (x1+x0)/2
    F01 = Fun(x01)
    if F0*F01<0:
        x1=x01
    else:
        x0=x01
    diff = (x1-x0)/2
    # print(x0,x1,diff)
print('Корень с погрешностью не более 0.02: ', round((x0+x1)/2, 3))