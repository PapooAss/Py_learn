# part 1
for l in range(10):
    for i in range(10):
        for k in range(10):
            for b in range(10):
                for u in range(10):
                    if l==i or l==k or l==b or l==u:
                        continue
                    if i==k or i==b or i==u:
                        continue
                    if k==b or k==u:
                        continue
                    if b==u:
                        continue
                    lik = l*100 + i*10 + k
                    bublik = b*100000 + u*10000 + b*1000 + l*100 + i*10 + k
                    if (lik*lik) == bublik:
                        print(lik,'*',lik,'=',bublik)

# part 2
for r in range(10):
    for e in range(6):
        for sh in range(10):
            for i in range(6):
                for s in range(6):
                    for l in range(6):
                        for n in range(6):
                            if r==e or r==sh or r==i or r==s or r==l or r==n:
                                continue
                            if e==sh or e==i or e==s or e==l or e==n:
                                continue
                            if sh==i or sh==s or sh==l or sh==n:
                                continue
                            if i==s or i==l or i==n:
                                continue
                            if s==l or s==n:
                                continue
                            if l==n:
                                continue
                            reshi = r*1000 + e*100 + sh*10 + i
                            esli = e*1000 + s*100 + l*10 +i
                            silen = s*10000 + i*1000 + l*100 + e*10 + n
                            if (reshi+esli) == silen:
                                print(reshi, '+', esli, '=', silen)