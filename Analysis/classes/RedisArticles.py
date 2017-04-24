import json
import redis
import re
import gensim
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from datetime import datetime

redisServer = redis.Redis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
bigram_dictionary = 'bigrams.dictionary'
DATA_DIRECTORY = '/Users/samburrell/Documents/News Project/Analysis/data/'

def tokenize_article(article):
    stops = set(stopwords.words('english') + article['stopwords']) # Set stopwords
    tokens = article['body'].lower()  # Lower the article.
    tokens = [re.sub(r'^[^\w]*|[^\w]*$|[\(\)]|[\[\]]|[\{\}]','',word) for word in tokens.split(' ')] # Remove odd characters
    tokens = [word.strip() for word in tokens if word.isalpha()]  # Remove numbers and punctuation.
    tokens = [token for token in tokens if token not in stops] # Remove stopwords
    tokens = [token for token in tokens if len(token) > 2] # Remove words less than 2 characters
    tokens = [WordNetLemmatizer().lemmatize(token) for token in tokens] # Lemmatize
    return tokens

def update_bigram_dictionary(tokens):
    train_bigram = gensim.models.phrases.Phrases()
    try:
        train_bigram.load(DATA_DIRECTORY+bigram_dictionary)
        print(tokens)
        train_bigram.add_vocab(list(tokens))
    except FileNotFoundError:
        train_bigram.add_vocab(list(tokens))
    train_bigram.save(DATA_DIRECTORY+bigram_dictionary)
    return

class RedisArticles(object):
    def getBody(self, url):
        article = json.loads(redisServer.get(url))
        return tokenize_article(article)

    def getHeadline(self):
        for url in redisServer.zrange('urls', 0, -1):
            article = json.loads(redisServer.get(url))
            yield article['headline']


    def yieldArticleTokens(self):
        for url in redisServer.zrange('urls', 0, -1):
            article = json.loads(redisServer.get(url))
            yield tokenize_article(article)
