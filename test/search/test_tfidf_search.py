'''
Created on Nov 18, 2019

@author: gregory
'''
from search import tfidf_search

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

def test_find_tfidf_variety():
    threshold = 0.0

    expected_top_result = ('Aneurysm, aortic', 0.4559686538756185)
    expected_matches = 6

    scoring = tfidf_search.find_tfidf_variety(output_token_dict, conditions, threshold)
    assert expected_matches == len(scoring)
    assert expected_top_result == scoring[0]
