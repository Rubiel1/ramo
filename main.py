 # -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:21:49 2020

@author: Dr. Eric Dolores
@co-author: Roberto Maldonado
We used code available on https://scikit-learn.org
"""


import os
import io
from itertools import compress
from operator import mul
from functools import reduce
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from sklearn.feature_extraction.text import CountVectorizer
try:
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    def processPDF(rsrcmgr, device, fp, pagenos=None, maxpages=0, password='', caching=True, check_extractable=True):
        """
        This function processes the pdf pages.
        Args: 
            rsrcmgr,
            device,
            fp,
            pagenos,
            maxpages,
            password,
            caching, 
            check_extractable, 
        Returns:
        """
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                  caching=caching, check_extractable=check_extractable):
            interpreter.process_page(page)
        return

except ModuleNotFoundError:
    from pdfminer.pdfinterp import PDFResourceManager, process_pdf as processPDF #test



def getData(folder): 
    """
    This function reads the PDF files in the given folder
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
        processPDF(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password,
                    caching=caching, check_extractable=True)
        fp.close()
    
    file = outfp.getvalue()
    device.close()
    if close_outfp:
        outfp.close()
    docs = file.split('PDFmill')[1:]
    print("Files processed.")
    return docs


def isThereACommonPhrase(corpus, numberOfWords=2, fileName="results.txt"):
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
      print(f"{'='*10}there is no common prhase of size {numberOfWords}")
      return  False
    names = compress(vectorizer2.get_feature_names(), common)    
    second = "\n ".join(list(names))
    with open(fileName, 'a') as f:
        f.write(f"\n \n{'='*10}list of common sentences with {numberOfWords} words:\n\n")
        f.writelines(second)
        print(f"\n \n{'='*10} there are {(sum(common))} common sentences with {numberOfWords} words")
        return  True


def commonWordCount(corpus, numberOfWords=1, fileName="results.txt"):
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
        f.write(f"\n \n {'='*10} All documents share {numberOfPhrases} words:\n\n")
        f.writelines(firstiter)


def analyzer(folderName='mill', size=4, defaultFilename="results.txt"): 
    """
    This function reads the PDF files in the given folder
    Args: 
        folderName, should be located at the same place of this file
        size, minimun number of words that a phrase should have to be consideres
        defaultFilename, Name for the file that stores results
    Returns:
    """
    fileName = defaultFilename  #"/tmp/"+defaultFilename
    with open(fileName, 'w') as f:
        dev_note = "This program finds common phrases on different PDF files.\nFor any inquiries/suggestions please contact at eric.rubiel[at]u.northwestern.edu \n"
        f.write(f"{'='*10}{dev_note}")

        step_one = "Step 1. Analyzing words shared by all documents \n"
        f.write(f"{'='*10}{step_one}")

    folder = folderName  # for google collab'/content/drive/My Drive/'+folderName
    if size<1 or type(size) != type(2):
        print("provide an integrer size>1")
        with open(fileName, 'a') as f:
            f.write(f"wrong input")
        return False

    corpus = getData(f'{folder}')
    if not corpus:
        with open(fileName, 'a') as f:
            f.write(f"wrong files")
        return None
    
    print(f"\n \n {'='*10} The actual words are returned in the txt that is downloaded for future manipulation.\n")
    print(f"\n{'='*10} We first analyze words shared by all documents\n")
    commonWordCount(corpus, 1, fileName)

    with open(fileName, 'a') as f:
            f.write(f"\n \n {'='*10} Now we search for common phrases of lenght >3\n")
    print(f"{'='*10} now we search for common phrases of lenght >3\n")
    value = True

    while value:
        value = isThereACommonPhrase(corpus, size, fileName)
        size = size +1
    
    print(f"\n \n {'='*10} The actual words are returned in the txt that is downloaded for future manipulation.\n")
   

if __name__ == "__main__":
    description = "The function analyzer has two parameters: The name of the folder and the size. \
                    \nThe folder should be located at the same place where this file is\
                    \n-Size is the minimun number of words that a phrase should have \
                    \n*Note: Size = 1 asks for all words shared by all documents \
                    actually return this value, so use size > 1"
    print(f'{description}')

    analyzer("mill",2)
