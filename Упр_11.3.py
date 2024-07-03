from random import *
cont = True
while cont:
    dice = randint(1,6)
    print(dice)
    x = input('Нажмите любую кнопку')
    if x == 'q':
        cont = False