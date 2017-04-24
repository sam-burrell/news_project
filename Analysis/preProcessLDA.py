#!/usr/bin/python3
import redis
import json
import re
#from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from datetime import datetime

redisServer = redis.Redis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

def tokenize_article(article):
    stops = set(stopwords.words('english') + article['stopwords']) # Set stopwords
    tokens = article['body'].lower()  # Lower the article.
    tokens = [re.sub(r'^[^\w]*|[^\w]*$|[\(\)]|[\[\]]|[\{\}]','',word) for word in tokens.split(' ')] # Remove odd characters
    tokens = [word.strip() for word in tokens if word.isalpha()]  # Remove numbers and punctuation.
    tokens = [token for token in tokens if token not in stops] # Remove stopwords
    tokens = [token for token in tokens if len(token) > 2] # Remove words less than 2 characters
    #tokens = [WordNetLemmatizer().lemmatize(token) for token in tokens] # Lemmatize
    return tokens

for key in redisServer.zrange('urls', 0, -1):
    article = json.loads(redisServer.get(key))
    print("%s %s\n" % (key, " ".join(tokenize_article(article))))
