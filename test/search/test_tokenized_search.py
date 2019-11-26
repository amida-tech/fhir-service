'''
Created on Nov 15, 2019

@author: gregory
'''
from search import tokenized_search
from .constants import OUTPUT_TOKEN_DICT, CONDITIONS

def test_find_tokenized_variety_basic():
    """
    test find_tokenized_variety
    """
    threshold = 0.0
    similarity_metric = 'cosine'
    stemmer = 'Porter'
    tokenizer = 'whitespace'

    expected_result = [('Cor pulmonale (secondary heart disease)', 0.316)]

    scoring = tokenized_search.find_tokenized_variety(OUTPUT_TOKEN_DICT, CONDITIONS, threshold,
                                                      similarity_metric, stemmer, tokenizer)
    assert expected_result == scoring
