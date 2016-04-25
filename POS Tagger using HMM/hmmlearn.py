import json
import sys

path = sys.argv[1]
allwords=[]
f=open(path, 'r')
lines=f.readlines()
f.close()

for line in lines:
    words = line.split()
    for word in words:
        allwords.append(word)

wordbytag= {}
tagcount={}
 #----------------------Emission
 
for word in allwords:
    w = word.split('/')
    tag = w[len(w)-1]
    currword = "/".join(w[0:len(w)-1])
    
    if currword not in wordbytag:
        wordbytag[currword]={}
        wordbytag[currword][tag] = 1  
    else:
        if tag not in wordbytag[currword]:
            wordbytag[currword][tag]=1
        else:
            wordbytag[currword][tag]+=1
    
    if tag not in tagcount:
        tagcount[tag]=1
    else:
        tagcount[tag]+=1


for word in wordbytag:
    for t in wordbytag[word]:
        wordbytag[word][t]= (wordbytag[word][t] * 1.0) / tagcount[t]
#----------------------- Transition

transition={}
for line in lines:
    prevtag=''
    words = line.split()
    for word in words:
        w = word.split('/')
        tag = w[len(w)-1]
        
        if prevtag=='':
            currtag = '_q'
        else:
            currtag = prevtag
            
        if currtag not in transition:
            transition[currtag] = {}
            transition[currtag][tag] = 1 
        else:
            
            if tag not in transition[currtag]:
                transition[currtag][tag]=1
            else:
                transition[currtag][tag]+=1  
        prevtag=tag
        
l=len(lines)

for tag in transition:
    total=0
    totcnt=0
    for t in tagcount:
        if t not in transition[tag]:
            transition[tag][t]=0
            total+=1
    if total>0:
        for t in tagcount:
            transition[tag][t]+=1
    
    totcnt=sum(transition[tag].values())     
         
    for currtag in transition[tag]:
        if tag =='_q':
            transition[tag][currtag]= (transition[tag][currtag] * 1.0) / (totcnt)
        else:   
            transition[tag][currtag]= (transition[tag][currtag] * 1.0) / (totcnt)              
    
emission = str(wordbytag)
trans = str(transition) 
tags = str(tagcount) 

f1 = open('hmmmodel.txt', 'w+')
f1.write(emission)
f1.write('\n')
f1.write(trans)
f1.write('\n')
f1.write(tags)
f1.close()
