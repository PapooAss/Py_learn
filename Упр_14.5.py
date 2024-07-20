import random
nums=[]
Q = 6 # длина списка
#newnums=nums
move = 3
for i in range(Q):
    nums.append(random.randint(0,99))
print(nums)
while move > 0:
    last_num = nums[Q-1]
    for i in range (Q-1, -1, -1):
        nums[i] = nums[i-1]
    nums[0] = last_num
    move -= 1
print(nums)
