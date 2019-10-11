'''
Created on Oct 11, 2019

@author: gregory
'''

from nltk.stem import PorterStemmer

# stem a single token
# porter is known as the gentle stemmer and is not too aggressive
def apply_nltk_porter_stemmer(token):
    porter = PorterStemmer()
    return porter.stem(token)