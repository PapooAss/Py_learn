Txt = 'Наша Таня громко плачет: Уронила в речку мячик.'
LenTxt = len(Txt)
N_word = 5
cnt=N_word-1
i=0
while cnt:
    i+=1
    a=Txt[i]
    if Txt[i]==' ':
        cnt-=1
        for j in range(i+1, LenTxt):
            b=Txt[j]
            if Txt[j]==' ':
                Txt2=Txt[i+1:j]
                break
print(Txt2)