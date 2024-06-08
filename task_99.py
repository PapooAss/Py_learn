# from array import *
table = [[2, 5, 8], [3, 7, 4], [1, 6, 9], [4, 2, 0]]
count = 0
for i in table:
    print(f"Строка {count} - {i}")
    count += 1
row = int(input("Введите номер строки: "))
print(table[row])
col = int(input("Введите номер столбца: "))
print(table[row][col])
choice = input("Хотите заменить значение? да/нет")
if choice == "да":
    usr_num = int(input("Введите новое значение: "))
    table[row][col] = usr_num
print(table[row])
