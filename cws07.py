# -*- coding: utf-8 -*-
import re

import hashlib

#db = pymongo.MongoClient().weixin.text_articles

def getText():
    import os, codecs
    texts_set = set()
    fileNames = os.listdir(dataMainDir)    
    for fileName in fileNames:
        with codecs.open("%s/%s" % (dataMainDir,fileName) ,"r",  'UTF-8') as f:
            doc=f.readlines()
            for a in doc:
                
                if md5(a.encode('utf-8')) in texts_set:
                    continue
                else:
                    texts_set.add(md5(a.encode('utf-8')))
                    for t in re.split(u'[^\u4e00-\u9fa50-9a-zA-Z]+', a):
                        if t:
                            yield t
            print ('total=%d'%len(texts_set))
            
def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w

def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

if __name__ == '__main__':
    
    import sys,os
    if len(sys.argv) < 2: 
        print ("Usage:", sys.argv[0], "目錄")
        sys.exit(1)       
    else:
        dataMainDir = sys.argv[1]
    
    md5 = lambda s: hashlib.md5(s).hexdigest()
    
    from collections import defaultdict
    import numpy as np
    
    n = 4
    #min_count = 128
    min_count = 5
    ngrams = defaultdict(int)
    
    for t in getText():
        for i in range(len(t)):
            for j in range(1, n+1):
                if i+j <= len(t):
                    
                    ngrams[t[i:i+j]] += 1
    
    ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
    total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])
    #print(ngrams)
    min_proba = {2:5, 3:25, 4:125}
    
    
    ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))
    
    #print(ngrams)
    words = defaultdict(int)
    
    
    
    
    for t in getText():
        
        for i in cut(t):
            words[i] += 1
    #print(words)
    words = {i:j for i,j in words.items() if j >= min_count}
    
    w = {i:j for i,j in words.items() if is_real(i)}
    print(w)
    
        