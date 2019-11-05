'''
Created on Oct 10, 2019

@author: gregory
'''

import FHIR_Helper
import json
import sys

from flask import Flask, request
from util import Dedup_Medfind
app = Flask(__name__)

test_data_dict = dict()

output_dict = dict()

output_data_file = 'data/output.tsv';
fhir_data_dir = 'data/fhir_stu3'
text_list_file = 'output/text_list.tsv'
html_lookup_file = 'data/medfind.txt'

#ingest "training" data from disc
FHIR_Helper.ingest_output_data(output_data_file)
    
#bring in test data from disc
FHIR_Helper.ingest_fhir_data(fhir_data_dir)
    
# send this list to disc for safe keeping
with open(text_list_file, 'w', encoding='utf-8') as fs:
    for key in test_data_dict.keys():
        fs.write(key + '\t' + str(test_data_dict[key]) + '\n')

# make sure our html lookup list contains only unique rows
Dedup_Medfind.cleanup_html_lookup_file(html_lookup_file)

@app.route('/suggest', methods=['POST'])
def lookup_candidates():
    user_query = request.form.get('query')
    response_limit = request.form.get('limit')
    threshold = request.form.get('threshold')
    similarity_metric = request.form.get('similarity_metric')
    query_method = request.form.get('query_method')
    
    if response_limit is None:
        response_limit = sys.maxsize
    else:
        response_limit = int(response_limit)
    if threshold is None:
        threshold = 0.0
    else:
        threshold = float(threshold)
    if similarity_metric is None:
        similarity_metric = 'harmonic'
    if query_method is None:
        query_method = 'tokenized'
    
    more_candidates = FHIR_Helper.lookup_medlineplus(user_query, html_lookup_file)
    if user_query not in more_candidates:
        more_candidates.append(user_query.lower())

    more_candidates += FHIR_Helper.lookup_icd10data(user_query, html_lookup_file)
                
    condition_information = FHIR_Helper.find_condition_information(more_candidates, query_method, similarity_metric, threshold)
    condition_information = condition_information[0:min(response_limit, len(condition_information))]
    return json.dumps(condition_information)

@app.route('/fetch', methods=['POST'])
def fetch_information():
    user_candidate = request.form.get('candidate')
    
    return str(FHIR_Helper.display_matching_information(user_candidate))

if __name__ == '__main__':
    app.run()