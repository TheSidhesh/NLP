import json
import sys
import string
import glob
import math
import os

f = open('nbmodel.txt', 'r');
data=json.load(f)
f.close()

prior = math.log(0.5, 10)
path = sys.argv[1]


stopset = set(["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours    ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"])

fout = open('nboutput.txt','w+');
ctr=0
def calclabel():
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                f1=open(os.path.join(root, file), 'r')  
                allwords=[]
                probtrue=0
                probnegative=0
                probdeceptive=0
                probpositive=0
                lines=f1.readlines()   
                for line in lines:
                    words = line.split()
                    for word in words:
                        word = "".join(l for l in word if l not in string.punctuation)
                        word = word.lower()
                        allwords.append(word) 
                    allwords = [x for x in allwords if x not in stopset] 
                    for currword in allwords:
                        if currword in data["true_reviews"]:
                            probtrue += math.log(data["true_reviews"][currword],10)
                        if currword in data["deceptive_reviews"]:
                            probdeceptive += math.log(data["deceptive_reviews"][currword],10)
                        if currword in data["positive_reviews"]:
                            probpositive += math.log(data["positive_reviews"][currword],10)
                        if currword in data["negative_reviews"]:
                            probnegative += math.log(data["negative_reviews"][currword],10)
                     
                    if probtrue>probdeceptive:
                        fout.write('truthful ')   
                    else:
                        fout.write('deceptive ')
                    if probpositive>probnegative:
                        fout.write('positive ')
                        fout.write(os.path.join(root, file)+'\n')   
                    else: 
                        fout.write('negative ') 
                        fout.write(os.path.join(root, file)+'\n') 
                      
                f.close()  
          
calclabel()






    
    