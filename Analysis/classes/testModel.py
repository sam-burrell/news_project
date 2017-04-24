import gensim
import json
import redis

redisServer = redis.Redis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

class newsArticles(object):
    def __iter__(self):
        for key in redisServer.zrange('urls', 0, -1):
            yield key

print(list(newsArticles()))
# add new articles to ngram set
#bigram = gensim.models.Phrases(list(newsArticles()))

#bigram[[list(newsArticles())[5]]]
