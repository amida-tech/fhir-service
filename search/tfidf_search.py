'''
Created on Oct 15, 2019

@author: gregory
'''

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

vectorizer = TfidfVectorizer(use_idf=True)

train_X = None
# we need a consisted ordering of keys to use this
train_corpus = []

def find_tfidf_variety(output_dict, conditions, threshold):
    global train_X
    global train_corpus
    # lazy initialization of train_X (and fitting of vectorizer)
    if train_X is None:
        train_corpus = list(output_dict.keys())
        train_X = vectorizer.fit_transform(train_corpus)
        pickle.dump(vectorizer, open('model/tfidf_vectorizer.sav', 'wb'))

    # wasteful, but for clarity
    test_corpus = [condition.strip().lower() for condition in conditions]
    test_X = vectorizer.transform(test_corpus)
    number_of_conditions = len(conditions)

    cosine_similarities = linear_kernel(test_X, train_X).flatten()
    related_docs_indices = cosine_similarities.argsort()[::-1]
    results = cosine_similarities[related_docs_indices]

    matching_docs = []
    counter = 0
    for i in related_docs_indices:
        if results[counter] <= threshold:
            break
        matching_docs.append((train_corpus[i // number_of_conditions], results[counter]))
        counter += 1

    return matching_docs
