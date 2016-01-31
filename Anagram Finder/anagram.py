import sys

def perm(current):
    r=[]
    if len(current)==1:
        r = [current]
    else:
        for i,c in enumerate(current):
            others = current[:i]+current[i+1:]
            for temp in perm(others):
                r+=[c+temp]
    return r

str = sys.argv[1];
str = ''.join(sorted(str))

f = open('anagram_out.txt', 'w+');
for p in perm(str):
    f.write(p+'\n'); 