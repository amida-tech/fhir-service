'''
Created on Oct 15, 2019

@author: gregory
'''

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

vectorizer = TfidfVectorizer(use_idf=True)

train_x = None
# we need a consisted ordering of keys to use this
train_corpus = []

def find_tfidf_variety(output_dict, conditions, threshold):
    """
    find possible matches using tf_idf

    :param output_token_dict: The pre-known list of conditions
    :param conditions: The list of conditions to consider
    :param threshold: The minimum similarity to retrain
    :return: the top search matches
    :rtype: list
    """
    global train_x
    global train_corpus
    # lazy initialization of train_X (and fitting of vectorizer)
    if train_x is None:
        train_corpus = list(output_dict.keys())
        train_x = vectorizer.fit_transform(train_corpus)
        pickle.dump(vectorizer, open('model/tfidf_vectorizer.sav', 'wb'))

    # wasteful, but for clarity
    test_corpus = [condition.strip().lower() for condition in conditions]
    test_x = vectorizer.transform(test_corpus)
    number_of_conditions = len(conditions)

    cosine_similarities = linear_kernel(test_x, train_x).flatten()
    related_docs_indices = cosine_similarities.argsort()[::-1]
    results = cosine_similarities[related_docs_indices]

    matching_docs = []
    matching_docs_set = set()
    counter = 0
    for i in related_docs_indices:
        if results[counter] <= threshold:
            break
        document_term = train_corpus[i // number_of_conditions]
        if document_term not in matching_docs_set:
            matching_docs.append((document_term, results[counter]))
            matching_docs_set.add(document_term)
        counter += 1

    return matching_docs
