'''
Created on Nov 15, 2019

@author: gregory
'''

from nlp import stopword

# this list has been lowercased by this point in time
PHRASE_1 = ['this', 'patient', 'suffers', 'from', 'chronic', 'pain', 'of', 'the',
            'lumbar', 'region', '.']

def test_remove_aggressive_stopwords():
    """
    Tests the ability of the aggressive stoplist to remove tokens
    """
    clean_tokens = stopword.remove_agressive_stopwords(PHRASE_1)
    expected_tokens = ['patient', 'suffers', 'pain', 'lumbar', 'region']
    assert expected_tokens == clean_tokens

def test_remove_nltk_stopwords():
    """
    Tests the ability of the nltk stoplist to remove tokens
    """
    clean_tokens = stopword.remove_nltk_stopwords(PHRASE_1)
    expected_tokens = ['patient', 'suffers', 'chronic', 'pain', 'lumbar', 'region', '.']
    assert expected_tokens == clean_tokens
