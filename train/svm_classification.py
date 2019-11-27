'''
Created on Nov 27, 2019

@author: gregory
'''

import fhir_helper
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split

def train_svm_classification(output_dict):    
    transformed_dict = {}
    transformed_dict['condition'] = []
    transformed_dict['codes'] = []
    for key in output_dict:
        transformed_dict['condition'].append(key)
        transformed_dict['codes'].append(output_dict[key][1])
    
    df = pd.DataFrame.from_dict(transformed_dict)
    df['codes_id'], uniques = df['codes'].factorize()
    with open('model/svm_uniques.p', 'wb') as fs:
        pickle.dump(uniques, fs)    
    
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    features = tfidf.fit_transform(df.condition).toarray()
    with open('model/svm_tfidf_vectorizer.p', 'wb') as fs:
        pickle.dump(tfidf, fs)

    labels = df.codes_id
    
    model = LinearSVC()
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)
    svm_model = model.fit(X_train, y_train)
    with open('model/svm.p', 'wb') as fs:
        pickle.dump(svm_model, fs)
        
if __name__ == '__main__':
    config_dict = fhir_helper.ingest_config_file('config/config.txt')
    fhir_helper.ingest_output_data(config_dict['OUTPUT_DATA_FILE'], config_dict['STEMMER'],
                       config_dict['TOKENIZER'], config_dict['STOPWORD'])    
    train_svm_classification(fhir_helper.output_dict)