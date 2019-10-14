'''
Created on Oct 11, 2019

@author: gregory
'''

def remove_agressive_stopwords(tokens):
    with open('data/stopword_lists/aggressive.txt', 'r', encoding='utf-8') as fs:
        lines = fs.readlines()
    return [x for x in tokens if x not in lines]