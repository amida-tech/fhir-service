'''
Created on Nov 15, 2019

@author: gregory
'''

from nlp import Metrics

left_empty = []
left_populated_1 = ['apple','banana','cherry']
left_populated_2 = ['apple','cherry','dorian','grape','lemon']
right_empty = []
right_populated_1 = ['apple','banana','cherry']
right_populated_2 = ['apple','banana','elderberry,','fig','grape','honeydew','jackfruit']

def test_harmonic_similarity_double_empty():
    assert(Metrics.harmonic_similarity(left_empty, right_empty) == 0.0)

def test_harmonic_similarity_left_empty():
    assert(Metrics.harmonic_similarity(left_empty, right_populated_1) == 0.0)

def test_harmonic_similarity_right_empty():
    assert(Metrics.harmonic_similarity(left_populated_1, right_empty) == 0.0)

def test_harmonic_similarity_populated_1():
    assert(Metrics.harmonic_similarity(left_populated_1, right_populated_1) == 1.0)

def test_harmonic_similarity_populated_2():
    assert(Metrics.harmonic_similarity(left_populated_2, right_populated_2) == 0.333)

def test_cosine_similarity_double_empty():
    assert(Metrics.cosine_similarity(left_empty, right_empty) == 0.0)

def test_cosine_similarity_left_empty():
    assert(Metrics.cosine_similarity(left_empty, right_populated_1) == 0.0)

def test_cosine_similarity_right_empty():
    assert(Metrics.cosine_similarity(left_populated_1, right_empty) == 0.0)

def test_cosine_similarity_populated_1():
    assert(Metrics.cosine_similarity(left_populated_1, right_populated_1) == 1.0)

def test_cosine_similarity_populated_2():
    assert(Metrics.cosine_similarity(left_populated_2, right_populated_2) == 0.338)

def test_jaccard_similarity_double_empty():
    assert(Metrics.jaccard_similarity(left_empty, right_empty) == 0.0)

def test_jaccard_similarity_left_empty():
    assert(Metrics.jaccard_similarity(left_empty, right_populated_1) == 0.0)

def test_jaccard_similarity_right_empty():
    assert(Metrics.jaccard_similarity(left_populated_1, right_empty) == 0.0)

def test_jaccard_similarity_populated_1():
    assert(Metrics.jaccard_similarity(left_populated_1, right_populated_1) == 1.0)

def test_jaccard_similarity_populated_2():
    assert(Metrics.jaccard_similarity(left_populated_2, right_populated_2) == 0.2)