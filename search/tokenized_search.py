'''
Created on Oct 15, 2019

@author: gregory
'''

from nlp import Metrics, Tokenizer

def find_tokenized_variety(output_token_dict, conditions, threshold, similarity_metric):
    total_set = set()
    for condition in conditions:
        condition = condition.strip().lower()
        tokens = Tokenizer.whitespace_tokenize(condition, 'Porter')
        for item in output_token_dict:
            item_tokens = output_token_dict[item]
            # here we compare tokens and item_tokens
            if 'cosine' == similarity_metric:
                similarity = Metrics.cosine_similarity(tokens, item_tokens)
            elif 'jaccard' == similarity_metric:
                similarity = Metrics.jaccard_similarity(tokens, item_tokens)                
            else:
                similarity = Metrics.harmonic_similarity(tokens, item_tokens)
            if similarity > threshold:
                # add the similarity so that we can rank descending
                total_set.add((item, similarity))
    
    sorted_by_similarity = sorted(total_set, key=lambda tup: tup[1], reverse=True)
    #sorted_by_similarity = [x[0] for x in sorted_by_similarity]
    
    return sorted_by_similarity

