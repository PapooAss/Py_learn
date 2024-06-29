box=[]
door=[]
for i in range(3):
    box.append(int(input(f'Введите {i+1} сторону ящика:')))
for i in range(2):
    door.append(int(input(f'Введите {i+1} сторону двери:')))
mid = sum(box)-min(box)-max(box)
if mid<min(door) and max(box)<max(door):
    print("Короб проходит в дверь.")
else:
    print("Короб НЕ проходит в дверь.")