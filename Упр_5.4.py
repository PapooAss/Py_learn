days = int(input('Сколько дней прошло с начала года? '))
wday = days % 7
if wday == 1:
    print('Понедельник')
elif wday == 2:
    print('Вторник')
elif wday == 3:
    print('Среда')
elif wday == 4:
    print('Четверг')
elif wday == 5:
    print('Пятница')
elif wday == 6:
    print('Суббота')
else:
    print('Воскресенье')