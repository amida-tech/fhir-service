"""
constants for search package
"""

CONDITIONS = ['aneurysm', 'Aneurysm, heart', 'Aneurysm, ventricle', 'Heart wall aneurysm',
              'Left ventricle aneurysm', 'Left ventricular aneurysm', 'Right ventricle aneurysm',
              'Right ventricular aneurysm', 'Ventricle aneurysm', 'Ventricular aneurysm',
              'Ventricle aneurysm', 'Left ventricle aneurysm', 'Right ventricular aneurysm',
              'Aneurysm, ventricle', 'Ventricular aneurysm', 'Left ventricular aneurysm',
              'Aneurysm, heart', 'Right ventricle aneurysm', 'Heart wall aneurysm']

OUTPUT_DICT = {'Aneurysm, aorta or branches': None, 'Aneurysm, aortic': None,
               'Aneurysm, arteriovenous, traumatic': None, 'Aneurysm, cerebral': None,
               'Aneurysm, large artery': None, 'Cor pulmonale (secondary heart disease)': None
               }

OUTPUT_TOKEN_DICT = {'Aneurysm, aorta or branches': ['Aneurysm', 'aorta', 'branches'],
                     'Aneurysm, aortic': ['Aneurysm', 'aortic'],
                     'Aneurysm, arteriovenous, traumatic': ['Aneurysm', 'artertiovenous', 'traumatic'],
                     'Aneurysm, cerebral': ['Aneurysm', 'cerebral'],
                     'Aneurysm, large artery': ['Aneurysm', 'large', 'artery'],
                     'Cor pulmonale (secondary heart disease)': ['Cor', 'pulmonale', 'secondary', 'heart', 'disease']
                     }
