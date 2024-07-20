Lst = list("Я, вас, люб,,,,,ил. Любовь, еще, быть может...")
Symb = ","
cnt = Lst.count(Symb)
for i in range (cnt-1):
    J = Lst.index(Symb)
    Lst.pop(J)
NewLst = ''.join(Lst)
print (NewLst)