'''
Created on Nov 27, 2019

@author: gregory
'''

import fhir_helper
import pandas as pd
import pickle

def find_svm_variety(conditions, svm_model, tfidf_model, unique_encoding):
    with open(tfidf_model, 'rb') as fs:
        tfidf = pickle.load(fs)
    
    transformed_dict = {}
    transformed_dict['condition'] = []
    transformed_dict['codes_id'] = []
    for condition in conditions:
        transformed_dict['condition'].append(condition)
        transformed_dict['codes_id'].append('')
    
    df = pd.DataFrame.from_dict(transformed_dict)    
    features = tfidf.transform(df.condition).toarray()

    X_test = pd.DataFrame(data=features)

    with open(svm_model, 'rb') as fs:
        model = pickle.load(fs)    
    
    y_pred = model.predict(X_test)
    
    with open(unique_encoding, 'rb') as fs:
        unique = pickle.load(fs)    

    answer = unique.take(y_pred)
    
    return answer.tolist()

if __name__ == '__main__':
    config_dict = fhir_helper.ingest_config_file('config/config.txt')
    conditions = ['stroke', 'Anatomical Loss Of One Eye With Inability To Wear Prosthesis']
    answer = find_svm_variety(conditions, config_dict['SVM_MODEL'], config_dict['SVM_TFIDF_MODEL'],
                     config_dict['SVM_UNIQUES'])
    print(answer)