import random

for m in range(2,30,2):
    for n in range(1,30,2):
        N = (2**m)*(3**n)
        if N>2e8 and N<4e8:
            print('n=', n, ', m=', m, ', N=', N)
