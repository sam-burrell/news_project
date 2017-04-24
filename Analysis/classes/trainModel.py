import gensim
import re
import json
import redis
import operator
from pprint import pprint
from nltk.stem import WordNetLemmatizer

redisServer = redis.Redis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

class newsArticles(object):
    def __iter__(self):
        for key in redisServer.zrange('urls', 0, -1):
            processed_tags = []
            for tag in json.loads(redisServer.get(key)):
                processed_tags.append(re.sub(r'\s','_',tag))
            yield processed_tags

    def getKey(self, key):
        return json.loads(redisServer.get(key))





articles = list(newsArticles())

dictionary = gensim.corpora.Dictionary(articles)
dictionary.filter_extremes(no_below=2, no_above=0.5)
#print(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in articles]

print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))
#lsimodel = gensim.models.LsiModel(corpus=corpus, num_topics=20, id2word=dictionary)
#print(lsimodel.show_topics(formatted=False))
#hdpmodel = gensim.models.HdpModel(corpus=corpus, id2word=dictionary)
#print(hdpmodel.show_topics())

model = gensim.models.Word2Vec(articles, workers=3)

from gensim.similarities import WmdSimilarity
num_best = 10
instance = WmdSimilarity(articles, model, num_best=10)

test = articles[227]
print(test)
sims = instance[test]
i=2
print('sim = %.4f' % sims[i][1])
print(articles[sims[i][0]])
print(model)
#from gensim.similarities import WmdSimilarity
#num_best = 10
#instance = WmdSimilarity(corpus, model, num_best=10)
