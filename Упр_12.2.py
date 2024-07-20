n = int(input('Введите число: '))
def SummDig(n):
    if n<10:
        return n
    else:
        return(n%10 + SummDig(n//10))
print('Сумма всех чисел =',SummDig(n))
