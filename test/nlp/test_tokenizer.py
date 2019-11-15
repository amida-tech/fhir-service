'''
Created on Nov 15, 2019

@author: gregory
'''

from nlp import Tokenizer

PHRASE_1 = "The man, Ivan Ivanovich, did not know the cat's eye color."

def test_whitespace_tokenize_no_stemming():
    """
        Test whitespace tokenization on a standard sentence
    """
    expected_result = ['The', 'man,', 'Ivan', 'Ivanovich,', 'did', 'not', 'know',
                       'the', "cat's", 'eye', 'color.']
    assert Tokenizer.whitespace_tokenize(PHRASE_1, None) == expected_result

def test_whitespace_tokenize_empty_sentence():
    """
        Test whitespace tokenization on an empty string
    """
    expected_result = []
    assert Tokenizer.whitespace_tokenize('', None) == expected_result

def test_whitespace_tokenize_none():
    """
        Test whitespace tokenization if None is received
    """
    expected_result = []
    assert Tokenizer.whitespace_tokenize(None, None) == expected_result

def test_nltk_tokenize():
    """
        Test nltk tokenization on a standard sentence
    """
    expected_result = ['The', 'man', ',', 'Ivan', 'Ivanovich', ',', 'did', 'not', 'know',
                       'the', 'cat', "'s", 'eye', 'color', '.']
    assert Tokenizer.nltk_tokenize(PHRASE_1) == expected_result

def test_nltk_tokenize_empty_sentence():
    """
        Test nltk tokenization on an empty string
    """
    expected_result = []
    assert Tokenizer.nltk_tokenize('') == expected_result

def test_nltk_tokenize_none():
    """
        Test nltk tokenization if None is received
    """
    expected_result = []
    assert Tokenizer.nltk_tokenize(None) == expected_result
