import random
sum = 0
for i in range(100_000):
    x = random.random()
    sum = sum + x
print("Сумма чисел=", sum, '\nСреднее арифметическое=',sum/100000)