# from array import *
table = [[2, 5, 8], [3, 7, 4], [1, 6, 9], [4, 2, 0]]
roam = int(input("Введите номер строки: "))
print(table[roam])
usr_num = int(input("Введите добавочное значение: "))
table[roam].append(usr_num)
print(table[roam])
