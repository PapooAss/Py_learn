txt = '''Подумав немного,  он положил на блины самый жирный 
кусок семги, кильку и сардинку, потом уж, млея и задыхаясь, 
свернул оба блина в трубку,  с чувством выпил рюмку водки, 
крякнул, раскрыл рот… Но тут его хватил апоплексический удар. '''
cnt = 0
txt2=''
for i in range(len(txt)-1):
    if txt[i] != ' ' or txt[i+1] != ' ':
        txt2 = txt2+txt[i]
    else:
        cnt += 1
print(txt2)
print('Удалено двойных пробелов-', cnt)