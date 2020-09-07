 # -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:21:49 2020

@author: Dr. Eric Dolores
@co-author: Roberto Maldonado
I used code available on https://scikit-learn.org
"""


import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
from operator import mul
from functools import reduce
from itertools import compress
from sklearn.feature_extraction.text import CountVectorizer


def process_pdf(rsrcmgr, device, fp, pagenos=None, maxpages=0, password='', caching=True, check_extractable=True):
    """
    This functons processes the pdf pages.
    Args: 
    Returns:
    """
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
              caching=caching, check_extractable=check_extractable):
        interpreter.process_page(page)
    return


def get_data(folder): 
    """
    This fucntion reads the PDF files in the given folder
    Args: 
        folder, 
    Returns:
    """
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


def isThereACommonPrhase(corpus, numberOfWords=2, fileName="results.txt"):
    """
    This function searches for phrases with a given numberOfWords
    Args: 
        corpus, 
        numberOfWords,
        fileName, 
    Returns:
    """
    vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(numberOfWords, numberOfWords), binary=True)
    X2 = vectorizer2.fit_transform(corpus)
    array = X2.toarray()
    common = reduce(mul, array)
    if (sum(common))<1:
      print(f'  =================there is no common prhase of size {numberOfWords}')
      return  False
    names = compress(vectorizer2.get_feature_names(), common)    
    second = "\n ".join(list(names))
    with open(fileName, 'a') as f:
        f.write(f"\n \n  =================list of common sentences with {numberOfWords} words:\n\n")
        f.writelines(second)
        print(f"\n \n  =================there are {(sum(common))} common sentences with {numberOfWords} words")
        return  True


def howManyCommonWords(corpus, numberOfWords=1, fileName="results.txt"):
    """
    This function searches for words shared by all documents if there are common phrases
    Args: 
        corpus, 
        numberOfWords,
        fileName, 
    Returns:
    """
    vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(numberOfWords, numberOfWords), binary=True)
    X2 = vectorizer2.fit_transform(corpus)
    array = X2.toarray()
    common = reduce(mul, array)
    numberOfPhrases = sum(common)
    names = compress(vectorizer2.get_feature_names(), common)
    firstiter = ", ".join(list(names))
    with open(fileName, 'a') as f:
        f.write(f"\n \n =================All documents share {numberOfPhrases} words:\n\n")
        f.writelines(firstiter)


def analyzer(nameOfFolder='mill', size=4, file_Name="results.txt"): 
    
    """
    This fucntion reads the PDF files in the given folder
    Args: 
        nameOfFolder, should be located at the same place of this file
        size, minimun number of words that a phrase should have to be consideres
        file_Name, Name for the file that stores results
    Returns:
    """
    fileName = file_Name  #"/tmp/"+file_Name
    with open(fileName, 'w') as f:
        f.write("\n \n =================This program finds common phrases on different pdf files.\n")
        f.write("\n \n =================For any suggestion contact me at eric.rubiel@u.northwestern.edu\n")
        f.write("\n \n =================We first analyze words shared by all documents\n")
    folder = nameOfFolder  # for google collab'/content/drive/My Drive/'+nameOfFolder
    if size<1 or type(size) != type(2):
        print("provide an integrer size>1")
        with open(fileName, 'a') as f:
            f.write(f"wrong input")
        return False
    corpus = get_data(f'{folder}')
    if not corpus:
        with open(fileName, 'a') as f:
            f.write(f"wrong files")
        return None
    
    print("\n \n =================The actual words are returned in the txt that is downloaded for future manipulation.\n")
    print("\n=================We first analyze words shared by all documents\n")
    howManyCommonWords(corpus, 1, fileName)
    with open(fileName, 'a') as f:
            f.write("\n \n =================Now we search for common phrases of lenght >3\n")
    print("\n=================now we search for common phrases of lenght >3\n")
    value = True
    while value:
        value = isThereACommonPrhase(corpus, size, fileName)
        size = size +1

if __name__ == "__main__":
    description = "The function analyzer has two parameters: The name of the folder and the size. \
                    \nThe folder should be located at the same place where this file is\
                    \n-Size is the minimun number of words that a phrase should have \
                    \n*Note: Size = 1 asks for all words shared by all documents \
                    actually return this value, so use size > 1"
    print(f'{description}')

    analyzer("mill",2)
