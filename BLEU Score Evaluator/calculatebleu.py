import sys
import os
from collections import Counter
from itertools import tee, islice
import math
from math import log

candidatepath = sys.argv[1]
referencepath = sys.argv[2]
candidatelist=[]

f=open(candidatepath, 'r')
candidatelist=f.readlines()
f.close()
 
referencelist=[]

if os.path.isdir(referencepath):
    for root, dirs, files in os.walk(referencepath):
        for file in files:
            if file.endswith(".txt"):
                f1=open(os.path.join(root, file), 'r')
                templist=[]
                templist=f1.readlines()
                referencelist.append(templist)
                f1.close()
else:
    f=open(referencepath, 'r')
    templist=[]
    templist=f.readlines()
    referencelist.append(templist)
    f.close()  
    
def ngrams(lst, n):
  tlst = lst
  while True:
    a, b = tee(tlst)
    l = tuple(islice(a, n))
    if len(l) == n:
      yield l
      next(b)
      tlst = b
    else:
      break 

referencecounter=[] 
              
def calcbleuscore(ngram):
    rlens=[]
    for i in range(0,len(referencelist)):
        rlens.append(0)
    linecounter = 0 
    finalbleuscore=0
    finalr=0
    tempr=0
    totalwords=0
    for candidateline in candidatelist:
        referencecounter=[]
        candidatecounter=[]
        candidateline=ngrams(candidateline.split(), ngram)
        temp=[]
        for word in candidateline:
            temp.append(word)
        candidatecounter = Counter(temp)
        totalwords+= sum(candidatecounter.values())
        bleuscore=0
        minr=0
        
        if sum(candidatecounter.values())==0:
            linecounter+=1 
            continue
        minr=sys.maxint
        minlen=sys.maxint
        for i in range(0,len(referencelist)):
            tempr=sys.maxint
            l=referencelist[i]
            line=l[linecounter]
            line=ngrams(line.split(), ngram)
            temp=[]
            for word in line:
                temp.append(word)
            tempcounter=Counter(temp)
            templen=sum(tempcounter.values())
            tempr= abs(sum(candidatecounter.values())-templen)
            if minr>tempr:
                minr=tempr
                minlen=templen
            referencecounter.append(tempcounter)
            rlens[i]+=templen
        finalr+=minlen
        linecounter+=1  
        
        for w in candidatecounter:
            
            candcount = candidatecounter[w]
            maxcount=-99
            
            for i in range(0,len(referencelist)):
                tempcount=referencecounter[i][w]
                
                if(tempcount>maxcount):
                    maxcount=tempcount
                
            if candcount<maxcount:
                final=(candcount*1.0)
            else:
                final=(maxcount*1.0)
            
            bleuscore+=final
        
        finalbleuscore+=bleuscore 
    if(totalwords==0):
        finalbleuscore=0
    else:
        finalbleuscore = finalbleuscore/totalwords
    return finalbleuscore,totalwords,rlens,finalr     

bleu=[]
bleu.append(0)
bleu.append(0)
bleu.append(0)
bleu.append(0)
bleu[0],candy,rl,r1=calcbleuscore(1)
bleu[1],c2,rl2,r2=calcbleuscore(2)
bleu[2],c3,rl3,r3=calcbleuscore(3)
bleu[3],c4,rl4,r4=calcbleuscore(4)

if candy!=0:
    if candy > r1:
        bp = 1
    else:
        bp = math.exp(1 - 1.0*r1 / candy)
else:
    bp=0    
temp=0
for i in range(0,4):
    if bleu[i]!=0:
        temp+=log(bleu[i])
        
finalbleu=(math.exp((0.25)*(temp)))*bp

f5=open("bleu_out.txt","w")
f5.write(str(finalbleu))
f5.close()
