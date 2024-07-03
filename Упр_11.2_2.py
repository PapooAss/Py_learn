from random import *
cnt = 0
correct = False
word = ''
Dau = ["ши","ин","г","да","фт","ун"]
while not correct:
    for i in Dau:
        word = word+i
    if word == 'дауншифтинг':
        print("слово составлено за",cnt,"итераций")
        correct = True
    else:
        cnt += 1
        shuffle(Dau)
        word = ''