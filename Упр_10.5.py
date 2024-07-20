def DEL (x):
    cnt = 0     # сбрасываем счетчик
    for i in range(x//2+1, 1, -1):
        if x%i == 0:
            break
        else:
            i=0
    return i
for x in range(124,304):
    DelMax = DEL(x)
    if DelMax == 0:
        print('Число', x, 'не имеет максимального делителя, кроме самого себя.')
    else:
        print('Число', x, 'имеет макисмальный делитель: ', DEL(x), '\n', x, '/', DEL(x), '=', int(x/DEL(x)))
print(DEL(124)-DEL(303))