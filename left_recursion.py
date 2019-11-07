def eilr(c):
    lr=[]
    nlr=[]
    for i in range(len(d[c][1])):
        if(d[c][1][i][0]==d[c][0][0]):
            lr.append(d[c][1][i])
        else:
            nlr.append(d[c][1][i])
    if(len(lr)!=0):
        nvar=d[c][0][0]+'1'
        d[c][1]=[i+nvar for i in nlr]
        d.append([[nvar],[i[1:]+nvar for i in lr]+['^']])
d=[]
V=['S','A']
d.append([['S'],['Sa','Sad','bd','^']])
# d.append([['A'],['Ac','Sd','e']])

print(d)
n=len(V)
eilr(0)
#print(d)
for i in range(1,n):
    for j in range(i):
        #previous production for ith production
        prev=d[j][0][0]
        #print(prev)
        for k in range(len(d[i][1])):
            if(d[i][1][k][0]==prev):
                x=d[i][1][k][1:]
                #print(x)
                d[i][1].pop(k)
                d[i][1]+=[l+x for l in d[j][1]]
    #print(d)
    eilr(i)
print(d)
