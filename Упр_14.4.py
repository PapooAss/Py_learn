import random
alf = 'qwertyuiopasdfghjklzxcvbnm'
shifr = []
num = 0
cnt = 1000
for i in range(cnt):
    shifr.append(random.choice(alf))
KOD = ''.join(shifr)
AU = ('au' in KOD)
if AU:
    pos = KOD.index('au')
    print('Ящик номер: ', pos)
else:
    print('Сегодня поставок не будет.')
