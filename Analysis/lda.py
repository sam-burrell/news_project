from classes.RedisArticles import RedisArticles
import gensim

redis = RedisArticles()

articles = list(redis.yieldArticleTokens())
dictionary = gensim.corpora.Dictionary(articles)
dictionary.filter_extremes(no_below=5, no_above=0.5)
corpus = [dictionary.doc2bow(doc) for doc in articles]

lsi = gensim.models.LsiModel(corpus, id2word=dictionary, num_topics=30)

vec_bow = dictionary.doc2bow(['antarctica'])
vec_lsi = lsi[vec_bow] # convert the query to LSI space
index = gensim.similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
sims = index[vec_lsi] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])

for i in sims:
    print(list(redis.getHeadline())[i[0]])
