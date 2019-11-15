'''
Created on Nov 15, 2019

@author: gregory
'''

from nlp import metrics

LEFT_EMPTY = []
LEFT_POPULATED_1 = ['apple', 'banana', 'cherry']
LEFT_POPULATED_2 = ['apple', 'cherry', 'dorian', 'grape', 'lemon']
RIGHT_EMPTY = []
RIGHT_POPULATED_1 = ['apple', 'banana', 'cherry']
RIGHT_POPULATED_2 = ['apple', 'banana', 'elderberry,', 'fig', 'grape', 'honeydew', 'jackfruit']

def test_harmonic_similarity_double_empty():
    """
        test harmonic similarity for 2 empty lists
    """
    assert metrics.harmonic_similarity(LEFT_EMPTY, RIGHT_EMPTY) == 0.0

def test_harmonic_similarity_left_empty():
    """
        test harmonic similarity if the 1st parameter is empty
    """
    assert metrics.harmonic_similarity(LEFT_EMPTY, RIGHT_POPULATED_1) == 0.0

def test_harmonic_similarity_right_empty():
    """
        test harmonic similarity if the 2nd parameter is empty
    """
    assert metrics.harmonic_similarity(LEFT_POPULATED_1, RIGHT_EMPTY) == 0.0

def test_harmonic_similarity_populated_1():
    """
        test harmonic similarity for one pair of populated lists
    """
    assert metrics.harmonic_similarity(LEFT_POPULATED_1, RIGHT_POPULATED_1) == 1.0

def test_harmonic_similarity_populated_2():
    """
        test harmonic similarity for another pair of populated lists
    """
    assert metrics.harmonic_similarity(LEFT_POPULATED_2, RIGHT_POPULATED_2) == 0.333

def test_cosine_similarity_double_empty():
    """
        test cosine similarity for 2 empty lists
    """
    assert metrics.cosine_similarity(LEFT_EMPTY, RIGHT_EMPTY) == 0.0

def test_cosine_similarity_left_empty():
    """
        test cosine similarity if the 1st parameter is empty
    """
    assert metrics.cosine_similarity(LEFT_EMPTY, RIGHT_POPULATED_1) == 0.0

def test_cosine_similarity_right_empty():
    """
        test cosine similarity if the 2nd parameter is empty
    """
    assert metrics.cosine_similarity(LEFT_POPULATED_1, RIGHT_EMPTY) == 0.0

def test_cosine_similarity_populated_1():
    """
        test cosine similarity for one pair of populated lists
    """
    assert metrics.cosine_similarity(LEFT_POPULATED_1, RIGHT_POPULATED_1) == 1.0

def test_cosine_similarity_populated_2():
    """
        test cosine similarity for another pair of populated lists
    """
    assert metrics.cosine_similarity(LEFT_POPULATED_2, RIGHT_POPULATED_2) == 0.338

def test_jaccard_similarity_double_empty():
    """
        test jaccard similarity for 2 empty lists
    """
    assert metrics.jaccard_similarity(LEFT_EMPTY, RIGHT_EMPTY) == 0.0

def test_jaccard_similarity_left_empty():
    """
        test jaccard similarity if the 1st parameter is empty
    """
    assert metrics.jaccard_similarity(LEFT_EMPTY, RIGHT_POPULATED_1) == 0.0

def test_jaccard_similarity_right_empty():
    """
        test jaccard similarity if the 2nd parameter is empty
    """
    assert metrics.jaccard_similarity(LEFT_POPULATED_1, RIGHT_EMPTY) == 0.0

def test_jaccard_similarity_populated_1():
    """
        test jaccard similarity for one pair of populated lists
    """
    assert metrics.jaccard_similarity(LEFT_POPULATED_1, RIGHT_POPULATED_1) == 1.0

def test_jaccard_similarity_populated_2():
    """
        test jaccard similarity for another pair of populated lists
    """
    assert metrics.jaccard_similarity(LEFT_POPULATED_2, RIGHT_POPULATED_2) == 0.2
    