import operator
import sys

from math import log10 
f = open('hmmmodel.txt', 'r');
ll=f.readlines()
f.close()
emission = eval(ll[0])
transition = eval(ll[1])
tagcount = eval(ll[2])

path=sys.argv[1]
f=open(path, 'r')
lines=f.readlines()
f.close()

maxval=-(sys.maxint)-1
transval=0
prevword='_q'
stateno = 0
prob={}
backpt={}
f = open('hmmoutput.txt','w+')
count=0
for line in lines:
    count+=1
    words = line.split()
    stateno = 0
    prevword='_q'
    prob={}
    backpt={}
    for word in words:
       
        if word not in emission:
            for tags in tagcount:
                maxval=-(sys.maxint)-1
                transval=0
                if prevword != '_q':
                    if prevword not in emission:
                        prevtaglist = tagcount.keys()
                    else:
                        prevtaglist=emission[prevword]
                    for ptag in prevtaglist:
                        transval=prob[stateno-1][ptag]+log10(transition[ptag][tags])
                        if maxval<transval:
                            maxval=transval
                            if stateno not in prob:
                                prob[stateno]={}
                                prob[stateno][tags]=transval
                            else:
                                prob[stateno][tags]=transval
                            if stateno not in backpt:
                                backpt[stateno]={}
                                backpt[stateno][tags]=ptag
                            else:
                                backpt[stateno][tags]=ptag
                else:
                    transval=log10(transition['_q'][tags])
                    if stateno not in prob:
                        prob[stateno]={}
                        prob[stateno][tags]=transval
                    else:
                        prob[stateno][tags]=transval
                    if stateno not in backpt:
                        backpt[stateno]={}
                        backpt[stateno][tags]='_q'
                    else:
                         backpt[stateno][tags]='_q'
        else:
            for tag in emission[word]:
                maxval=-(sys.maxint)-1
                transval=-(sys.maxint)-1
                if prevword != '_q':
                    if prevword not in emission:
                        prevtaglist = tagcount.keys()
                        
                    else:
                        prevtaglist=emission[prevword]
                    for ptag in prevtaglist:
                        transval=prob[stateno-1][ptag]+log10(emission[word][tag])+log10(transition[ptag][tag])

                        if maxval<transval:
                            maxval=transval
                            if stateno not in prob:
                                prob[stateno]={}
                                prob[stateno][tag]=transval
                            else:
                                prob[stateno][tag]=transval
                            if stateno not in backpt:
                                backpt[stateno]={}
                                backpt[stateno][tag]=ptag
                            else:
                                backpt[stateno][tag]=ptag
                else:
                    transval=transval=log10(transition['_q'][tag]*emission[word][tag])
                    if stateno not in prob:
                        prob[stateno]={}
                        prob[stateno][tag]=transval
                    else:
                        prob[stateno][tag]=transval
                    if stateno not in backpt:
                        backpt[stateno]={}
                        backpt[stateno][tag]='_q'
                    else:
                         backpt[stateno][tag]='_q' 
                
        stateno+=1       
        prevword = word
    
    str = ''
    stats = prob[stateno-1] 
    s = max(stats.iteritems(), key=operator.itemgetter(1))[0] 
    str = words[stateno-1] + '/' + s
    try:
        for i in range(len(words)-2,-1,-1):
            s = backpt[i+1][s]
            str += ' ' + words[i] + '/'+ s
    except:
        #str = ' '.join(reversed(str.split()))
        #print count
        pass
    str = ' '.join(reversed(str.split()))
    f.write(str+'\n')
f.close()
