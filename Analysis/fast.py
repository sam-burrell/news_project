import fasttext
from classes.readRedis import readArticlesRedis

articles = list(readArticlesRedis())
articles_file = 'fasttext.model.train'

with open(articles_file, 'w') as f:
    for article in articles:
        f.write(article['url']+', '+article['clean_body']+'\n')

model = fasttext.skipgram(articles_file, 'data/fasttext.model')
#model = fasttext.load_model('model.bin', encoding='utf-8')

WMD SIMILARITY????? with FAST TEXT???????

print(articles[2]['clean_body'])
