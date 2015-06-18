# -*- coding: utf-8 -*-
import pandas as pd
import lda
from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize, pos_tag
import re, collections
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn import svm, metrics, cross_validation
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.cluster import KMeans

def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return ''
    else:
        return s
        
# Tokenizing (Document to list of sentences. Sentence to list of words.)
def tokenize(str):
  '''Tokenizes into sentences, then strips punctuation/abbr, converts to lowercase and tokenizes words'''
  return  [word_tokenize(" ".join(re.findall(r'\w+', t,flags = re.UNICODE | re.LOCALE)).lower()) 
      for t in sent_tokenize(str.replace("'", ""))]
          
def stemming(words_l, type="PorterStemmer", lang="english", encoding="utf8"):
  supported_stemmers = ["PorterStemmer","SnowballStemmer","LancasterStemmer","WordNetLemmatizer"]
  if type is False or type not in supported_stemmers:
    return words_l
  else:
    l = []
    if type == "PorterStemmer":
      stemmer = PorterStemmer()
      for word in words_l:
        l.append(stemmer.stem(word).encode(encoding))
    if type == "SnowballStemmer":
      stemmer = SnowballStemmer(lang)
      for word in words_l:
        l.append(stemmer.stem(word).encode(encoding))
    if type == "LancasterStemmer":
      stemmer = LancasterStemmer()
      for word in words_l:
        l.append(stemmer.stem(word).encode(encoding))
    if type == "WordNetLemmatizer": #TODO: context
      wnl = WordNetLemmatizer()
      for word in words_l:
        l.append(wnl.lemmatize(word).encode(encoding))
    return l       

#Removing stopwords. Takes list of words, outputs list of words.
def remove_stopwords(l_words, lang='english'):
  l_stopwords = stopwords.words(lang)
  content = [w for w in l_words if w.lower() not in l_stopwords]
  return content
 
def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#Stem all words with stemmer of type, return encoded as "encoding"
def preprocess_pipeline(str, lang="english", stemmer_type="PorterStemmer", return_as_str=False, 
            do_remove_stopwords=False, do_clean_html=False):
  l = []
  words = []
  if do_clean_html:
    sentences = tokenize(str)
  else:
    sentences = tokenize(str)
  for sentence in sentences:
    if do_remove_stopwords:
      words = remove_stopwords(sentence, lang)
    else:
      words = sentence
    words = stemming(words, stemmer_type)
    if return_as_str:
      l.append(" ".join(words))
    else:
      l.append(words)
  if return_as_str:
    return " ".join(l)
  else:
    return l   
    
df = pd.read_csv('./../data/horoscopes/astrosign.csv', sep='|')
df = df.drop('Unnamed: 0', 1)
df=df.dropna()

d = []
for i, scope in enumerate(df['horoscope']):
    preprocessed = preprocess_pipeline(scope, stemmer_type="SnowballStemmer", do_remove_stopwords=True)
    doc = []
    for sent in preprocessed:
         doc.append(' '.join(word for word in sent))
    d.append('. '.join(sent for sent in doc))

df['cleaned'] = d

#create dtm
cv = CountVectorizer()
wordcounts = cv.fit_transform(df['cleaned'])
wc = to.array(wordcounts)

#fit a 20-topic lda model. print out top 8 words for each topic, and a plot of the loglikelihoods
model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model.fit(wordcounts)
topic_word = model.topic_word_
n_top_words=8
vocab = cv.get_feature_names()
for i, topic_dist in enumerate(topic_word):
    topic_words=np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    topic_words=[w.encode('utf-8') for w in topic_words]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    
plt.plot(model.loglikelihoods_[5:])

#fit a 50-topic lda model. print out top 8 words for each topic, and a plot of the loglikelihoods
model = lda.LDA(n_topics=50, n_iter=1500, random_state=1)
model.fit(wordcounts)
topic_word = model.topic_word_
n_top_words=8
vocab = cv.get_feature_names()
for i, topic_dist in enumerate(topic_word):
    topic_words=np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    topic_words=[w.encode('utf-8') for w in topic_words]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    
plt.plot(model.loglikelihoods_[5:])

km = KMeans(n_clusters=12, init='k-means++', max_iter=100, n_init=1)

km.fit(wordcounts)

metrics.homogeneity_score(df['zodiac'], km.labels_)

metrics.completeness_score(df['zodiac'], km.labels_)

by_sign = df.groupby('zodiac')
by_sign['kmeans_guess'].value_counts()

metrics.v_measure_score(df['zodiac'], km.labels_)
metrics.confusion_matrix(df['zodiac'], km.labels_)