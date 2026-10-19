from collections import Counter
from pathlib import Path
import math, re

def tokenize(s):
    return re.findall(r'[a-z0-9]+', s.lower())

def chunks(text, max_words=90):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0,len(words),max_words)]

class Retriever:
    def __init__(self, directory):
        self.records=[]
        for path in sorted(Path(directory).glob('*.md')):
            for i,chunk in enumerate(chunks(path.read_text(encoding='utf-8'))):
                self.records.append({'source':path.name,'chunk':i,'text':chunk})
        self.docs=[Counter(tokenize(r['text'])) for r in self.records]
        self.df=Counter(w for d in self.docs for w in d)
        self.n=len(self.docs)

    def vector(self, counts):
        return {w:(1+math.log(tf))*math.log((self.n+1)/(self.df.get(w,0)+1))+0.01
                for w,tf in counts.items()}

    def search(self, query, k=3):
        if not query.strip():
            return []
        q=self.vector(Counter(tokenize(query)))
        out=[]
        for record,counts in zip(self.records,self.docs):
            v=self.vector(counts)
            numerator=sum(q[w]*v.get(w,0) for w in q)
            norm=math.sqrt(sum(x*x for x in q.values())*sum(x*x for x in v.values()))
            score=numerator/norm if norm else 0
            if score>0:
                out.append(dict(record,score=round(score,5)))
        return sorted(out,key=lambda r:(-r['score'],r['source']))[:max(1,min(int(k),20))]
