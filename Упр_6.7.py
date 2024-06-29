for x in range(41,60):
    x5 = False
    x25 = False
    if x%5 == 0:
        x5 = True
    if x%25 == 0:
        x25 = True
    y = not((x5)<=(x25))
    print('x=', x, '-', y)