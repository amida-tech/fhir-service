'''
Created on Oct 10, 2019

@author: gregory
'''

import json
import sys

import argparse
from flask import Flask, request
from util import dedup_medfind

import fhir_helper

app = Flask(__name__)

test_data_dict = dict()

output_dict = dict()

config_dict = dict()

OUTPUT_DATA_FILE = 'data/output.tsv'
FHIR_DATA_DIR = 'data/fhir_stu3'
TEXT_LIST_FILE = 'output/text_list.tsv'
HTML_LOOKUP_FILE = 'data/medfind.txt'

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
    tokenizer = request.form.get('tokenizer')

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
    if stemmer is None:
        stemmer = 'Porter'
    if tokenizer is None:
        tokenizer = 'whitespace'

    more_candidates = list(fhir_helper.lookup_medlineplus(config_dict['BASE_MEDLINEPLUS_URL'],
                                                     user_query, HTML_LOOKUP_FILE))
    if user_query not in more_candidates:
        more_candidates.append(user_query.lower())

    more_candidates += list(fhir_helper.lookup_icd10data(config_dict['BASE_ICD_URL'],
                                                    user_query, HTML_LOOKUP_FILE))

    condition_information = fhir_helper.find_condition_information(
        more_candidates, query_method, similarity_metric, stemmer, tokenizer, threshold)
    condition_information = condition_information[0:min(response_limit, len(condition_information))]
    return json.dumps(condition_information)

@app.route('/fetch', methods=['POST'])
def fetch_information():
    '''
        The fetch endpoint
    '''
    user_candidate = request.form.get('candidate')

    return json.dumps(fhir_helper.display_matching_information(user_candidate))

def handle_cli(cli_args):
    """
    Process the command line arguments
      
    :param cli_args: the read in command line arguments
    """
    global config_dict
    config_dict = fhir_helper.ingest_config_file(cli_args.cfile)

    #ingest "training" data from disc
    fhir_helper.ingest_output_data(OUTPUT_DATA_FILE, config_dict['STEMMER'],
                                   config_dict['TOKENIZER'], config_dict['STOPWORD'])

    #bring in test data from disc
    fhir_helper.ingest_fhir_data(FHIR_DATA_DIR)

    # send this list to disc for safe keeping
    with open(TEXT_LIST_FILE, 'w', encoding='utf-8') as fs:
        for key in test_data_dict:
            fs.write(key + '\t' + str(test_data_dict[key]) + '\n')

    # make sure our html lookup list contains only unique rows
    dedup_medfind.cleanup_html_lookup_file(HTML_LOOKUP_FILE)

# argparse parser
parser = argparse.ArgumentParser()
parser.add_argument('cfile', help='The location of a configuration file')
parser.set_defaults(func=handle_cli)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
    app.run()
