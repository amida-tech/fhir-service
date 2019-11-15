'''
Created on Oct 11, 2019

@author: gregory
'''

from nlp import StemmingLemmatization

def whitespace_tokenize(document, stemmer):
    if not document:
        return []
    tokens = document.split(' ')
    if stemmer is None or (stemmer != 'Porter' and stemmer != 'Snowball'):
        return tokens
    stemmed_tokens = []
    for token in tokens:
        if 'Porter' == stemmer: 
            stemmed_tokens.append(StemmingLemmatization.apply_nltk_porter_stemmer(token))
        elif 'Snowball' == stemmer:
            stemmed_tokens.append(StemmingLemmatization.apply_nltk_snowball_stemmer(token))            
    return stemmed_tokens