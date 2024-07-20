simple_array = [[2, 5, 8], [3, 7, 4], [1, 6, 9]]
print(simple_array)
simple_array[2][1] = 5
print(simple_array)
print(simple_array[1])
simple_array[1].append(33)
print(simple_array)
data_set = {"A": {"x": 54, "y": 82, "z": 91}, "B": {"x": 75, "y": 29, "z": 80}}
print(data_set)
print(data_set["A"])
for i in data_set:
    print(data_set[i]["y"])
data_set["B"]["y"] = 555
print(data_set)
