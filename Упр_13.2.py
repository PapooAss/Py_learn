# Кодировщик
word='Привет, как дела?'
word2=''
WORD = ''
for i in word:
    Ord = ord(i)+3
    word2=word2+chr(Ord)
print(word2)

# декодировщик
T = True
while T:
    key = int(input('Введите ключ: '))
    for i in word2:
        Ord = ord(i)+key
        WORD = WORD+chr(Ord)
    print(WORD)
    answ = input('Ключ подходит?')
    if answ == 'да':
        T = False
    print('Еще попытка...')
    WORD=''