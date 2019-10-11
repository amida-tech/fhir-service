'''
Created on Oct 11, 2019

@author: gregory
'''

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