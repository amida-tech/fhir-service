'''
Created on Oct 15, 2019

@author: gregory
'''

import operator

from nlp import metrics, tokenizer

def find_tokenized_variety(output_token_dict, conditions, threshold, similarity_metric,
                           stemmer, tokenizer_name):
    """
    search for most relevant matches to query based on tokenization

    :param output_token_dict: The pre-known list of conditions
    :param conditions: The list of conditions to consider
    :param threshold: The minimum similarity to retrain
    :param similarity_metric: Which similarity strategy to use
    :param stemmer: Which stemmer to use
    :param tokenizer_name: Which tokenizer to use
    :type output_token_dict: dict
    :type conditions: list
    :type threshold: float
    :type similarity_metric: str
    :type stemmer: str
    :type tokenizer_name: str
    :return: the top search matches
    :rtype: list
    """
    total_dict = {}
    for condition in conditions:
        condition = condition.strip().lower()
        if 'whitespace' == tokenizer_name:
            tokens = tokenizer.whitespace_tokenize(condition, stemmer)
        elif 'nltk' == tokenizer_name:
            tokens = tokenizer.nltk_tokenize(condition)
        else:
            tokens = []
        for item in output_token_dict:
            item_tokens = output_token_dict[item]
            # here we compare tokens and item_tokens
            if 'cosine' == similarity_metric:
                similarity = metrics.cosine_similarity(tokens, item_tokens)
            elif 'jaccard' == similarity_metric:
                similarity = metrics.jaccard_similarity(tokens, item_tokens)
            else:
                similarity = metrics.harmonic_similarity(tokens, item_tokens)
            if similarity > threshold:
                # add the similarity so that we can rank descending
                if item in total_dict:
                    if similarity > total_dict[item]:
                        total_dict[item] = similarity
                else:
                    total_dict[item] = similarity
                print(condition + ' -> ' + item)
                print(similarity)

    sorted_by_similarity = sorted(total_dict.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_by_similarity
