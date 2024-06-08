from array import *
nums1 = array('f',[12.34, 34.67, 64.33, 86.22, 25.09])
tryagain = True
while tryagain:
    usr_num = int(input("Введите число от 2 до 5: "))
    if usr_num<2 or usr_num>5:
        print("Попробуйте еще раз.")
    else:
        tryagain = False
for i in nums1:
    print(f"{round(i/usr_num, 2)}")