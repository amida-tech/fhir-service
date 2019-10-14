'''
Created on Oct 11, 2019

@author: gregory
'''

from collections import Counter
import math

def harmonic_similarity(list1, list2):    
    set1 = set(list1)
    set2 = set(list2)
    
    score1 = 0.0
    score2 = 0.0
    
    for s1 in set1:
        if s1 in set2:
            score1 += 1
    for s2 in set2:
        if s2 in set1:
            score2 += 1
        
    score1 /= len(s1)
    score2 /= len(s2)
        
    if score1 + score2 == 0.0:
        return 0.0
    
    return 2.0 * score1 * score2 / (score1 + score2)

def cosine_similarity(list1, list2):
    counter1 = Counter(list1)
    counter2 = Counter(list2)
    terms = set(counter1).union(counter2)
    dotprod = sum(counter1.get(k, 0) * counter2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(counter1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(counter2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)