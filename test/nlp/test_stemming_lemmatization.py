'''
Created on Nov 14, 2019

@author: gregory
'''

from nlp import StemmingLemmatization, Tokenizer

phrase_1 = 'The fox was quickly walking by the seashore in the morning daylight.'

def test_apply_nltk_porter_stemmer():
    stemmer = 'Porter'
    expected_output = ['the', 'fox', 'wa', 'quickli', 'walk', 'by', 'the', 'seashor', 'in', 'the', 'morn', 'daylight.']
    tokens = Tokenizer.whitespace_tokenize(phrase_1, stemmer)
    assert(expected_output == tokens)

def test_apply_nltk_snowball_stemmer():
    stemmer = 'Snowball'
    expected_output = ['the', 'fox', 'was', 'quick', 'walk', 'by', 'the', 'seashor', 'in', 'the', 'morn', 'daylight.']
    tokens = Tokenizer.whitespace_tokenize(phrase_1, stemmer)
    assert(expected_output == tokens)
