'''
Created on Oct 11, 2019

@author: gregory
'''

from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

def apply_nltk_porter_stemmer(token):
    """
    stem a single token
    porter is known as the gentle stemmer and is not too aggressive

    @param: token: a single token
    @type: token: str
    @return: the stemmed token
    @rtype: str
    """
    porter = PorterStemmer()
    return porter.stem(token)

def apply_nltk_snowball_stemmer(token, stopwords=False):
    """
    stem a single token
    snowball is a more aggressive stemmer (yet more mature

    @param: token: a single token
    @type: token: str
    @return: the stemmed token
    @rtype: str
    """
    stemmer = SnowballStemmer("english", ignore_stopwords=not stopwords)
    return stemmer.stem(token)
