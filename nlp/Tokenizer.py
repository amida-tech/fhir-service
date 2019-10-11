'''
Created on Oct 11, 2019

@author: gregory
'''

from nlp import StemmingLemmatization

def whitespace_tokenize(document, stemmer):
    tokens = document.split(' ')
    if stemmer is None or stemmer != 'Porter':
        return tokens
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(StemmingLemmatization.apply_nltk_porter_stemmer(token))
    return stemmed_tokens