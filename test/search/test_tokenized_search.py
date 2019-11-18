'''
Created on Nov 15, 2019

@author: gregory
'''
from search import tokenized_search

conditions = ['aneurysm', 'Aneurysm, heart', 'Aneurysm, ventricle', 'Heart wall aneurysm',
              'Left ventricle aneurysm', 'Left ventricular aneurysm', 'Right ventricle aneurysm',
              'Right ventricular aneurysm', 'Ventricle aneurysm', 'Ventricular aneurysm',
              'Ventricle aneurysm', 'Left ventricle aneurysm', 'Right ventricular aneurysm',
              'Aneurysm, ventricle', 'Ventricular aneurysm', 'Left ventricular aneurysm',
              'Aneurysm, heart', 'Right ventricle aneurysm', 'Heart wall aneurysm']

output_dict = {'Aneurysm, aorta or branches': None, 'Aneurysm, aortic': None,
               'Aneurysm, arteriovenous, traumatic': None, 'Aneurysm, cerebral': None,
               'Aneurysm, large artery': None, 'Cor pulmonale (secondary heart disease)': None
               }
output_token_dict = {'Aneurysm, aorta or branches': ['Aneurysm', 'aorta', 'branches'],
                     'Aneurysm, aortic': ['Aneurysm', 'aortic'],
                     'Aneurysm, arteriovenous, traumatic': ['Aneurysm', 'artertiovenous', 'traumatic'],
                     'Aneurysm, cerebral': ['Aneurysm', 'cerebral'],
                     'Aneurysm, large artery': ['Aneurysm', 'large', 'artery'],
                     'Cor pulmonale (secondary heart disease)': ['Cor', 'pulmonale', 'secondary', 'heart', 'disease']
                     }

def test_find_tokenized_variety_basic():
    threshold = 0.0
    similarity_metric = 'cosine'
    stemmer = 'Porter'
    tokenizer = 'whitespace'

    scoring = tokenized_search.find_tokenized_variety(output_token_dict, conditions, threshold, 
                                            similarity_metric, stemmer, tokenizer)
    print(scoring)
    