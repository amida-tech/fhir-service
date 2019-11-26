'''
Created on Nov 18, 2019

@author: gregory
'''
from search import subset_search
from .constants import OUTPUT_TOKEN_DICT, CONDITIONS

def test_find_subset_variety():
    """
    test find_subset_variety function
    """
    # Cor pulmonale won't be included because there is no "aneurysm" in it
    expected_matches = 5

    scoring = subset_search.find_subset_variety(OUTPUT_TOKEN_DICT, CONDITIONS)
    assert expected_matches == len(scoring)
