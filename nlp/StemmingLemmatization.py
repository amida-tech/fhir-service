'''
Created on Oct 11, 2019

@author: gregory
'''

from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

# stem a single token
# porter is known as the gentle stemmer and is not too aggressive
def apply_nltk_porter_stemmer(token):
    porter = PorterStemmer()
    return porter.stem(token)


# snowball is a more aggressive stemmer (yet more mature)
def apply_nltk_snowball_stemmer(token, stopwords=False):
    stemmer = SnowballStemmer("english", ignore_stopwords=not stopwords)
    return stemmer.stem(token)