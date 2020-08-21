 # -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:21:49 2020

@author: Dr. Eric Dolores
I used code available on https://scikit-learn.org
"""

import os
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import logging
from operator import mul
from functools import reduce
from itertools import compress
from sklearn.feature_extraction.text import CountVectorizer


logging.propagate = False 
logging.getLogger().setLevel(logging.ERROR)


def get_data(folder): 
    # we read the pdf files in the folder
    caching = True
    rsrcmgr = PDFResourceManager(caching=caching)
    outfp = io.StringIO()
    close_outfp = True
    laparams = LAParams()
    device = TextConverter(rsrcmgr, outfp, laparams=laparams)
    pagenos = set()
    maxpages = 0
    password = ''
    cwd = os.getcwd()
    path = os.path.join(cwd, f'{folder}')
    if not os.path.isdir(path):
        print(f"folder missing at {path}")
        return None
    (_, _, files) = next(os.walk(path))
    print(f'Reading pdf files in {path}\n')
    args = [thing for thing in files if thing.endswith('.pdf')] #['10343-10353.pdf']
    for fname in args:
        outfp.write('PDFmill')
        fp = io.open(os.path.join(path,fname), 'rb')
        process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password,
                    caching=caching, check_extractable=True)
        fp.close()
    
    file = outfp.getvalue()
    device.close()
    if close_outfp:
        outfp.close()
    docs = file.split('PDFmill')[1:]
    print("Files processed.")
    return docs

def isThereACommonPrhase(corpus, numberOfWords=2):
    # we search for phrases with numberOfWords words
    vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(numberOfWords, numberOfWords), binary=True)
    X2 = vectorizer2.fit_transform(corpus)
    array = X2.toarray()
    common = reduce(mul, array)
    names = compress(vectorizer2.get_feature_names(), common>0)    
    second = list(names)
    for name in second:
        print(f"\n--- list of common sentences with {numberOfWords} words:\n\n{second}")
        return  True
    else:
        print(f'--- there is no common prhase of size {numberOfWords}')
        return  False


def howManyCommonWords(corpus, numberOfWords=1):
    # we search for words shared by all documents
    vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(numberOfWords, numberOfWords))
    X2 = vectorizer2.fit_transform(corpus)
    array = X2.toarray()
    common = reduce(mul, array)
    numberOfPhrases = sum(common>0)
    print(f"All documents share {numberOfPhrases} words")
    names = compress(vectorizer2.get_feature_names(), common>0)
    print(list(names))


def analyzer(folder='mill', size=4):    
    # folder should be located at the same place of this file,
    # size is the minimun number of words that a phrase should have
    # to be considered
    if size<1 or type(size) != type(2):
        print("provide an integrer size>1")
        return False
    corpus = get_data(f'{folder}')
    if not corpus:
        return None
    print("\n=================We first analyze words shared by all documents\n")
    howManyCommonWords(corpus, numberOfWords=1)
    print("\n=================now we search for common phrases of lenght >3\n")
    value = True
    while value:
        value = isThereACommonPrhase(corpus, size)
        size = size +1
    print(f"\nThe longest common phrase has {size-2} words")


if __name__ == "__main__":
    print("The function analyzer has two parameters, the name of the folder and the size")
    print(" -the folder should be located at the same place that this file,")
    print(" -size is the minimun number of words that a phrase should have")
    print("  note that size = 1 asks for all words shared by all documents")
    print("we actually return this value, so use size>1")
    analyzer("mill",3)