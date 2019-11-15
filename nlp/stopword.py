'''
Created on Oct 11, 2019

@author: gregory
'''

from nltk.corpus import stopwords

def remove_agressive_stopwords(tokens):
    """
    remove tokens listed in the aggressive stopword list

    param: tokens: a list of tokens
    type: tokens: list of str
    return: valid tokens
    rtype: list of str
    """
    with open('data/stopword_lists/aggressive.txt', 'r', encoding='utf-8') as fs:
        lines = fs.read().splitlines()
    return [x for x in tokens if x not in lines]

def remove_nltk_stopwords(tokens):
    """
    remove tokens listed in the nltp stopword list

    param: tokens: a list of tokens
    type: tokens: list of str
    return: valid tokens
    rtype: list of str
    """
    stop_words = set(stopwords.words('english'))
    return [t for t in tokens if not t in stop_words]
