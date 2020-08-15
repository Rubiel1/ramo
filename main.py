# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:21:49 2020

@author: Dr. Eric Dolores
"""
# get the text from pdf
import os
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
def get_data():
    caching = True
    rsrcmgr = PDFResourceManager(caching=caching)
    #outfile = path + 'test.txt'
    #outfp = io.open(outfile, 'wt', encoding='utf-8', errors='ignore')
    outfp = io.StringIO()
    close_outfp = True
    laparams = LAParams()
    device = TextConverter(rsrcmgr, outfp, laparams=laparams)
    pagenos = set()
    maxpages = 0
    password = ''
    path = 'C:\\Users\\FSU\\Documents\\GitHub\\ramo\\neurons\\'
    (_, _, files) = next(os.walk(path))
    
    args = [thing for thing in files if thing.endswith('.pdf')] #['10343-10353.pdf']
    for fname in args:
        outfp.write('PDFmill')
        fp = io.open(path+fname, 'rb')
        process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password,
                    caching=caching, check_extractable=True)
        
        fp.close()
    
    file = outfp.getvalue()
    device.close()
    if close_outfp:
        outfp.close()
    docs = file.split('PDFmill')[1:]
    return docs


from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
#from sklearn.datasets import fetch_20newsgroups

# We first read the papers

n_samples = 2000
n_features = 1000
n_components = 10
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

print("Loading dataset...")
t0 = time()
#data, _ = fetch_20newsgroups(shuffle=True, random_state=1,
#                             remove=('headers', 'footers', 'quotes'),
#                             return_X_y=True)
#data_samples = data[:n_samples]
data = get_data()
data_samples = data
print("done in %0.3fs." % (time() - t0))

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   max_features=n_features,
                                   stop_words='english')
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=n_features,
                                stop_words='english')
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
print()

# Fit the NMF model
print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in NMF model (Frobenius norm):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

# Fit the NMF model
print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
      "tf-idf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

print("Fitting LDA models with tf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)


"""Here is a sample output when the input are newspapers"""
"""Fitting the NMF model (Frobenius norm) with tf-idf features, n_samples=2000 and n_features=1000...
done in 0.221s.

Topics in NMF model (Frobenius norm):
Topic #0: just people don think like know good time make way really say ve right want did ll new use years
Topic #1: windows use dos using window program os application drivers help software pc running ms screen files version work code mode
Topic #2: god jesus bible faith christian christ christians does sin heaven believe lord life mary church atheism love belief human religion
Topic #3: thanks know does mail advance hi info interested email anybody looking card help like appreciated information list send video need
Topic #4: car cars tires miles 00 new engine insurance price condition oil speed power good 000 brake year models used bought
Topic #5: edu soon send com university internet mit ftp mail cc pub article information hope email mac home program blood contact
Topic #6: file files problem format win sound ftp pub read save site image help available create copy running memory self version
Topic #7: game team games year win play season players nhl runs goal toronto hockey division flyers player defense leafs bad won
Topic #8: drive drives hard disk floppy software card mac computer power scsi controller apple 00 mb pc rom sale problem monitor
Topic #9: key chip clipper keys encryption government public use secure enforcement phone nsa law communications security clinton used standard legal data
"""


















