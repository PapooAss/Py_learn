# *******Моё решение*************
x = int(input('Введите максимальный знаменатель:'))
znak = True
sum = 0
for i in range(1,x+1,2):
    if znak:
        sum = sum+1/i
        znak = False
    else:
        sum = sum-1/i
        znak = True
print('Сумма ряда:', round(sum,3))

# ****** РЕКУРСИЯ *********
def Row(sum,N,m):   #sum-сумма(изн =1), N-кол-во повт (дробей), m-делитель (изначально = 3, затем +2)
    sum = sum + (1/m)*(-1)**N
    if N<=1:
        return sum
    return Row(sum, N-1, m+2) # вызываем функцию с товым параметрами
print('Сумма ряда 1-1/3+1/5-1/7.... = ',Row(1,4, 3))
