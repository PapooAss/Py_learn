for x in range(20, 25):
    y = ((x<25) <= (x<23)) and ((x<22) <= (x>21))
    print('x=',x, ' - ', y)