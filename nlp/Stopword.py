'''
Created on Oct 11, 2019

@author: gregory
'''

AGGRESSIVE_LIST = ['&', 'the', 'and', 'or', 'of', 'to', 'for', 'from', 'a', 'not',
                   'disorder', 'situation']

def remove_agressive_stopwords(tokens):
    return [x for x in tokens if x not in AGGRESSIVE_LIST]