'''
Created on Oct 11, 2019

@author: gregory
'''

from collections import Counter
import math

def harmonic_similarity(list1, list2):
    """
    Find the harmonic similarity between two lists

    @param: list1: a list of tokens
    @param: list2: a list of tokens
    @type: list1: list of str
    @type: list2: list of str
    @return: the similariy score in [0.0,1.0]
    """
    set1 = set(list1)
    set2 = set(list2)

    score1 = 0.0
    score2 = 0.0

    for s1 in set1:
        if s1 in set2:
            score1 += 1.0
    for s2 in set2:
        if s2 in set1:
            score2 += 1.0

    score1 = 0.0 if not set1 else score1 / len(set1)
    score2 = 0.0 if not set2 else score2 / len(set2)

    if score1 + score2 == 0.0:
        return 0.0

    return round(2.0 * score1 * score2 / (score1 + score2), 3)

def cosine_similarity(list1, list2):
    """
    Find the cosine similarity between two lists

    @param: list1: a list of tokens
    @param: list2: a list of tokens
    @type: list1: list of str
    @type: list2: list of str
    @return: the similariy score in [0.0,1.0]
    """
    counter1 = Counter(list1)
    counter2 = Counter(list2)
    terms = set(counter1).union(counter2)
    dotprod = sum(counter1.get(k, 0) * counter2.get(k, 0) for k in terms)
    mag_a = math.sqrt(sum(counter1.get(k, 0)**2 for k in terms))
    mag_b = math.sqrt(sum(counter2.get(k, 0)**2 for k in terms))
    magnitude = mag_a * mag_b
    return 0.0 if magnitude == 0.0 else round(dotprod / magnitude, 3)

def jaccard_similarity(list1, list2):
    """
    Find the jaccard similarity between two lists

    @param: list1: a list of tokens
    @param: list2: a list of tokens
    @type: list1: list of str
    @type: list2: list of str
    @return: the similariy score in [0.0,1.0]
    """
    s1 = set(list1)
    s2 = set(list2)
    denominator = len(s1.union(s2))
    return 0.0 if denominator == 0 else round(len(s1.intersection(s2)) / denominator, 3)
