'''
Created on Oct 15, 2019

@author: gregory
'''

def find_subset_variety(output_dict, conditions):
    total_set = set()
    for condition in conditions:
        condition = condition.strip().lower()
        matches = [item for item in output_dict if condition in item]
        total_set |= set(matches)
    return list(total_set)
