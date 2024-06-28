for x in (False, True):
    for y in (False, True):
        z = x and not y or not x and y
        print(x,y,z)