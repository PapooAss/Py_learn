import random
deck = ['6п','6ч','6т','6б','7п','7ч','7т','7б','8п','8ч','8т','8б','9п','9ч','9т','9б','10п','10ч',
        '10т','10б','Вп','Вч','Вт','Вб','Дп','Дч','Дт','Дб','Кп','Кч','Кт','Кб','Тп','Тч','Тт','Тб']
pl1 = []
pl2 = []
pl3 = []
def shuf(deck):
    x = random.choice(deck)
    deck.remove(x)
    return x
for i in range (6):
    pl1.append(shuf(deck))
    pl2.append(shuf(deck))
    pl3.append(shuf(deck))
print('1 Игрок:',pl1)
print('2 Игрок:',pl2)
print('3 Игрок:',pl3)
print('Колода:',deck)

