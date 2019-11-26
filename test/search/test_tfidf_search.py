'''
Created on Nov 18, 2019

@author: gregory
'''
from .constants import OUTPUT_TOKEN_DICT, CONDITIONS
from search import tfidf_search

def test_find_tfidf_variety():
    """
    test find_tfidf_variety
    """
    threshold = 0.0
    # force reload of training data
    tfidf_search.train_x = None

    expected_top_result = ('Aneurysm, aortic', 0.4559686538756185)
    expected_matches = 6

    scoring = tfidf_search.find_tfidf_variety(OUTPUT_TOKEN_DICT, CONDITIONS, threshold)
    assert expected_matches == len(scoring)
    assert expected_top_result == scoring[0]
