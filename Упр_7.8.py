# N = 100
# for Y in range(2,N):
#     x = Y//2
#     while x>1:
#         if Y%x == 0:
#             break
#         x -= 1
#     else:
#         print(Y, end=" ")

for i in range(101, 1213270, 171):
    if i == 154856:
        print('154856 done')
        break
else:
    print("Нет такого числа")
print("Hasta la vista")