import string  
import sys
import glob
import json
from collections import Counter

 
path = sys.argv[1]
negpath = '/negative_polarity'
pospath = '/positive_polarity'
truepathforneg = '/truthful_from_Web'
truepathforpos = '/truthful_from_TripAdvisor'
deceptivepath = '/deceptive_from_MTurk'
arrayforfolds = ["/fold1","/fold2/","/fold3/","/fold4/"]
stopset = set(["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours    ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"])

trainmain= {}
trainmain['positive_reviews']={}
trainmain['negative_reviews']={}
trainmain['true_reviews']={}
trainmain['deceptive_reviews']={}


def makelist(dir):

    allwords=[]
    for fold in (dir + s for s in arrayforfolds):
        fold = fold + '*.txt'
        ##print fold
        files=glob.glob(fold)  
        for file in files:    
            f=open(file, 'r')  
            lines=f.readlines()   
            for line in lines:
                words = line.split()
                for word in words:
                    word = "".join(l for l in word if l not in string.punctuation)
                    print word
                    allwords.append(word)       
            f.close() 
           
   
    allwords = [x for x in allwords if x not in stopset]              
    return allwords


negreviews = makelist(path + negpath + truepathforneg)
negreviews += makelist(path + negpath + deceptivepath)
negreviews = [x for x in negreviews if x!='']  

posreviews = makelist(path + pospath + truepathforpos)
posreviews += makelist(path + pospath + deceptivepath)
posreviews = [x for x in posreviews if x!=''] 

truereviews = makelist(path + negpath + truepathforneg)
truereviews += makelist(path + pospath + truepathforpos)
truereviews = [x for x in truereviews if x!=''] 

deceptivereviews = makelist(path + negpath + deceptivepath)
deceptivereviews += makelist(path + pospath + deceptivepath)
deceptivereviews = [x for x in deceptivereviews if x!=''] 

vocabnegpos = set(negreviews+posreviews)

countneg =  Counter(negreviews)
countpos =  Counter(posreviews)
counttrue =  Counter(truereviews)
countdeceptive =  Counter(deceptivereviews)

for word in vocabnegpos:
    
    
    truecount = 1 + counttrue[word]
    deceptivecount = 1 +  countdeceptive[word]
    negcount = 1 +  countneg[word]
    poscount = 1 +  countpos[word]
    
    trainmain['true_reviews'][word] = (truecount * 1.0) / ( len(truereviews) + len(vocabnegpos))
    trainmain['deceptive_reviews'][word] = (deceptivecount * 1.0) / ( len(deceptivereviews) + len(vocabnegpos))
    trainmain['positive_reviews'][word] = (poscount * 1.0) / ( len(posreviews) + len(vocabnegpos))
    trainmain['negative_reviews'][word] = (negcount * 1.0) / ( len(negreviews) + len(vocabnegpos))
    

f = open('nbmodel.txt', 'w+');
json.dump(trainmain,f)
f.close()