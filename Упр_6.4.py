num1 = int(input('Введите первое число: '))
num2 = int(input('Введите второе число: '))
if num1<5 or num1>10:
    res1 = False
else:
    res1 = True
if num2<5 or num2>10:
    res2 = False
else:
    res2 = True
if res1 and res2:
    print('Числа подходят.')
elif res1 or res2:
    print('Подходит одно число.')
else:
    print('Числа не подходят.')