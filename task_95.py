from array import *
import random
val = int(input("Введите количество чисел в массиве: "))
nums_array = array('f', [])
for i in range(0, val):
    rand_num = round(((random.randrange(1, 1000) / random.randrange(1, 1000))*10), 2)
    print(rand_num)
    nums_array.append(round(rand_num, 2))
# print(nums_array)
formatted_nums = [f"{num:.2f}" for num in nums_array]
print("Отформатированные значения массива: ", formatted_nums)
# print(nums_array)
usr_num = int(input("Введите свое число: "))
usr_nums = array('f', [])
for i in range(0, len(formatted_nums)):
    rrr = float(formatted_nums[i]) / usr_num
    usr_nums.append(rrr)
print("Новый массив: ", usr_nums)
