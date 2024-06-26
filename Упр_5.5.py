# one = [1]
# two = [2, 3, 4]
# five = [0, 5, 6, 7, 8, 9, 10]
# elevn = [11, 12, 13, 14]
# num = int(input('Введите число: '))
# num1 = num % 100
# if num in one:
#     rub = 'рубль'
# elif num in two:
#     rub = 'рубля'
# elif num in five or num in elevn:
#     rub = 'рублей'
# elif num1 in elevn:
#     rub = 'рублей'
#
# else:
#     num1 = num % 10
#     if num1 in one:
#         rub = 'рубль'
#     elif num1 in two:
#         rub = 'рубля'
#     elif num1 in five:
#         rub = 'рублей'
# print(f'У вас {num} {rub}.')

# Решение из учебника
Rub = int(input('Сколько у Вас рублей? '))
rub = Rub % 100
print(rub)
if 10 <= rub <= 20 or rub % 10 > 4 or rub % 10 == 0:
    txt = 'рублей'
elif rub % 10 == 1:
    txt = 'рубль'
else:
    txt = 'рубля'
print('У вас', Rub, txt)