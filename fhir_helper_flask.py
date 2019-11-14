'''
Created on Oct 10, 2019

@author: gregory
'''

import json
import sys

from flask import Flask, request
from util import Dedup_Medfind

import fhir_helper

app = Flask(__name__)

test_data_dict = dict()

output_dict = dict()

OUTPUT_DATA_FILE = 'data/output.tsv'
FHIR_DATA_DIR = 'data/fhir_stu3'
TEXT_LIST_FILE = 'output/text_list.tsv'
HTML_LOOKUP_FILE = 'data/medfind.txt'

#ingest "training" data from disc
fhir_helper.ingest_output_data(OUTPUT_DATA_FILE)

#bring in test data from disc
fhir_helper.ingest_fhir_data(FHIR_DATA_DIR)

# send this list to disc for safe keeping
with open(TEXT_LIST_FILE, 'w', encoding='utf-8') as fs:
    for key in test_data_dict:
        fs.write(key + '\t' + str(test_data_dict[key]) + '\n')

# make sure our html lookup list contains only unique rows
Dedup_Medfind.cleanup_html_lookup_file(HTML_LOOKUP_FILE)

@app.route('/suggest', methods=['POST'])
def lookup_candidates():
    '''
        The suggest endpoint
    '''
    user_query = request.form.get('query')
    response_limit = request.form.get('limit')
    threshold = request.form.get('threshold')
    similarity_metric = request.form.get('similarity_metric')
    query_method = request.form.get('query_method')
    stemmer = request.form.get('stemmer')

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
    if stemmer in None:
        stemmer = 'Porter'

    more_candidates = fhir_helper.lookup_medlineplus(user_query, HTML_LOOKUP_FILE)
    if user_query not in more_candidates:
        more_candidates.append(user_query.lower())

    more_candidates += fhir_helper.lookup_icd10data(user_query, HTML_LOOKUP_FILE)

    condition_information = fhir_helper.find_condition_information(
        more_candidates, query_method, similarity_metric, stemmer, threshold)
    condition_information = condition_information[0:min(response_limit, len(condition_information))]
    return json.dumps(condition_information)

@app.route('/fetch', methods=['POST'])
def fetch_information():
    '''
        The fetch endpoint
    '''
    user_candidate = request.form.get('candidate')

    return json.dumps(fhir_helper.display_matching_information(user_candidate))

if __name__ == '__main__':
    app.run()
