# ************ Вариант 1 **********
# denied = True
# while denied:
#     usrpass = int(input('Введите пароль: '))
#     if usrpass == 123:
#         denied = False
#         print('Access granted.')
#     else:
#         print('Access denied!')

# *********** Вариант 2************
while input('Введите пароль: ') != '123':
    print('Access denied.')
print('Access granted!')