"""
Created on Oct 10, 2019

@author: gregory
"""

import argparse
import json
from os import listdir
from os.path import isfile, join
from urllib.request import urlopen
from bs4 import BeautifulSoup
from gensim.test import test_similarity_metrics

from nlp import Stopword, Tokenizer
from search import subset_search, tfidf_search, tokenized_search
from util import Dedup_Medfind

BASE_ICD_URL = 'https://www.icd10data.com/'
BASE_MEDLINEPLUS_URL = 'https://medlineplus.gov/'

test_data_dict = dict()

output_dict = dict()

output_token_dict = dict()

# this is a tsv file
def ingest_output_data(output_file, stemmer):
    """
    ingests the output data
    """
    with open(output_file, 'r', encoding='utf-8') as fs:
        lines = fs.readlines()

    for line in lines:
        parts = line.split('\t')
        condition = parts[0].lower()
        related_data = parts[0:]
        output_dict[condition] = related_data
        output_token_dict[condition] = Stopword.remove_agressive_stopwords(
            Tokenizer.whitespace_tokenize(condition
                                          .replace(')', '')
                                          .replace(':', '')
                                          .replace(',', '')
                                          , stemmer))

def ingest_fhir_data(fhir_data_dir):
    """
    ingests the fhir data
    """
    onlyfiles = [f for f in listdir(fhir_data_dir) if isfile(join(fhir_data_dir, f))]

    for onlyfile in onlyfiles:
        with open(join(fhir_data_dir, onlyfile)) as f:
            data = json.load(f)
        entry = data['entry']
        for ent in entry:
            resource = ent['resource']
            resource_type = resource['resourceType']
            if 'Condition' == resource_type:
                code = resource['code']
                text_field = code['text'].strip()
                if text_field not in test_data_dict:
                    test_data_dict[text_field] = 0
                test_data_dict[text_field] += 1

def lookup_from_synonym_file(query, html_lookup_file):
    """
    lookup medical synonyms from disc
    """
    alts = set()
    lower_query = query.lower()

    with open(html_lookup_file, 'r', encoding='utf-8') as fs:
        lines = fs.readlines()
    for line in lines:
        parts = line.split('\t')
        comparison = parts[0].lower()
        synonym = parts[1].strip(' \n')
        if comparison == lower_query:
            alts.add(synonym)
    return list(alts)

def find_condition_information(conditions, query_method, similarity_metric, stemmer, threshold=0.0):
    """
    find condition information
    """
    # right now, test data and output_data needs to be in memory to work
    # we would like to expand this for
    #    1) partial matches
    #    2) synonyms
    #    3) case differences

    # this is the subset solution
    if 'subset' == query_method:
        return subset_search.find_subset_variety(output_dict, conditions)
    elif 'tfidf' == query_method:
        # this is perhaps even more sophisticated
        return tfidf_search.find_tfidf_variety(output_dict, conditions, threshold)
    else:
        # this is a slight more sophisticated token based matching solution
        return tokenized_search.find_tokenized_variety(
            output_token_dict, conditions, threshold, similarity_metric, stemmer)

def lookup_medlineplus(user_query, html_lookups_file):
    """
    lookup medical information from medlineplus
    """
    # need the lowercase version of the query to have any shot
    medlineplus_url = BASE_MEDLINEPLUS_URL + user_query.lower().replace(' ', '') + '.html'
    alts = []
    try:
        f = urlopen(medlineplus_url)
        myfile = f.read()
        soup = BeautifulSoup(myfile, 'html.parser')
        alsocalled = soup.findAll("span", {"class": "alsocalled"})[0].text
        alsocalled = alsocalled[13:]
        alts = alsocalled.split(',')
        #print("HTML found " + str(alts))
        with open(html_lookups_file, 'a', encoding='utf-8') as fs:
            for alt in alts:
                fs.write(user_query + '\t'  + alt + '\n')
    except:
        #print('HTML Lookup failed')
        pass

    # this should contain medfind stuff, icd10data and pre-exisiting synonyms
    alts += lookup_from_synonym_file(user_query, html_lookups_file)

    return alts

def lookup_icd10data(user_query, html_lookups_file):
    """
    lookup icd10data from the web
    """
    url = BASE_ICD_URL + 'search?s=' + user_query
    alts = []
    try:
        f = urlopen(url)
        myfile = f.read()
        soup = BeautifulSoup(myfile, 'html.parser')
        search_lines = soup.findAll("div", {"class": "searchLine"})
        # likely we would try to follow and parse just the first link
        # however, here is how we get all the relevant top level links
        hyperlinks = []
        for search_line in search_lines:
            hyperlinks.append(BASE_ICD_URL + search_line.find('a', href=True)['href'])

        f2 = urlopen(hyperlinks[0])
        myfile2 = f2.read()
        soup2 = BeautifulSoup(myfile2, 'html.parser')

        span_lines = soup2.findAll("span")
        for span_line in span_lines:
            if 'Approximate Synonyms' == span_line.text:
                approximate_list = span_line.find_next_sibling()
                synonyms = approximate_list.find_all('li')
                for synonym in synonyms:
                    alts.append(synonym.text)

        with open(html_lookups_file, 'a', encoding='utf-8') as fs:
            for alt in alts:
                fs.write(user_query + '\t'  + alt + '\n')
    except:
        pass

    # this should contain medfind stuff, icd10data and pre-exisiting synonyms
    alts += lookup_from_synonym_file(user_query, html_lookups_file)

    return alts

def get_console_input(mode):
    """
    query the console input for console mode
    """
    if mode:
        choice = input('Which condition do you wish to look up?\n\n')
    else:
        choice = input('Which of these makes sense to you?\n\n')
    return choice

def display_matching_information(choice):
    """
    lookup output dictionary for key value
    """
    print(output_dict[choice])
    return output_dict[choice]

def main(config_dict):
    """
    the main function

    :param config_dict: the dictionary containing all necessary configuration values
    """
    #ingest "training" data from disc
    ingest_output_data(config_dict['OUTPUT_DATA_FILE'], config_dict['STEMMER'])

    #bring in test data from disc
    ingest_fhir_data(config_dict['FHIR_DATA_DIR'])

    # send this list to disc for safe keeping
    with open(config_dict['TEXT_LIST_FILE'], 'w', encoding='utf-8') as fs:
        for key in test_data_dict:
            fs.write(key + '\t' + str(test_data_dict[key]) + '\n')

    # make sure our html lookup list contains only unique rows
    Dedup_Medfind.cleanup_html_lookup_file(config_dict['HTML_LOOKUP_FILE'])

    # now let us try to do the main event.  We should choose from test_data really
    # this will be converted to service, but we can simulate with a loop
    user_query = ''
    user_candidate = ''
    while user_query != 'quit':
        user_query = get_console_input(True)

        # we will now try to augment this by "database" lookup
        # "Stroke" is a good test to assure that this works
        more_candidates = lookup_medlineplus(user_query, config_dict['HTML_LOOKUP_FILE'])
        if user_query not in more_candidates:
            more_candidates.append(user_query.lower())

        more_candidates += lookup_icd10data(user_query, config_dict['HTML_LOOKUP_FILE'])

        candidates = find_condition_information(
            more_candidates, config_dict['QUERY_METHOD'],
            config_dict['SIMILARITY_METRIC'], config_dict['STEMMER'])

        print(candidates)

        # then we will mock the user selecting an item
        user_candidate = get_console_input(False)
        if user_candidate in [i[0] for i in candidates]:
            display_matching_information(user_candidate)

def main_test(config_dict):    
    """
    the main function for testing purposes
    
    :param config_dict: the dictionary containing all necessary configuration values
    """
    
    #ingest "training" data from disc
    ingest_output_data(config_dict['OUTPUT_DATA_FILE'])

    #bring in test data from disc
    ingest_fhir_data(config_dict['FHIR_DATA_DIR'])

    # send this list to disc for safe keeping
    with open(config_dict['TEXT_LIST_FILE'], 'w', encoding='utf-8') as fs:
        for key in test_data_dict:
            fs.write(key + '\t' + str(test_data_dict[key]) + '\n')

    # make sure our html lookup list contains only unique rows
    Dedup_Medfind.cleanup_html_lookup_file(config_dict['HTML_LOOKUP_FILE'])

    non_empties = 0
    total = 0

    with open(config_dict['TEST_RESULTS_FILE'], 'w', encoding='utf-8') as fs:

        # now let us try to do the main event.  We should choose from test_data really
        # this will be converted to service, but we can simulate with a loop
        for test_key in test_data_dict:
            user_query = test_key

            # we will now try to augment this by "database" lookup
            # "Stroke" is a good test to assure that this works
            more_candidates = lookup_medlineplus(user_query, config_dict['HTML_LOOKUP_FILE'])
            if user_query not in more_candidates:
                more_candidates.append(user_query.lower())

            more_candidates += lookup_icd10data(user_query, config_dict['HTML_LOOKUP_FILE'])

            candidates = find_condition_information(
                more_candidates, config_dict['QUERY_METHOD'],
                config_dict['SIMILARITY_METRIC'], config_dict['STEMMER'])

            # only printing to disc now, not console
            fs.write(test_key)
            for single_candidate in candidates:
                fs.write('\t' + str(single_candidate))
            fs.write('\n')

            total += 1
            if len(candidates) > 0:
                non_empties += 1

    print(str(non_empties) + ' of ' + str(total) + ' test queries matched')

def ingest_config_file(config_file):
    config_dict = {}
    
    with open(config_file, 'r', encoding='utf-8') as fs:
        lines = fs.readlines()
    for line in lines:
        line = line.strip()
        if len(line) < 2:
            continue
        if line.startswith('#'):
            continue
        parts = line.split('\t')
        config_dict[parts[0]] = parts[1]
    
    return config_dict

def handle_cli(args):
    config_dict = ingest_config_file(args.cfile)

    if bool(args.test) == True:
        main_test(config_dict)
    else:
        main(config_dict)

# argparse parser
parser = argparse.ArgumentParser()
parser.add_argument('cfile', help='The location of a configuration file')
parser.add_argument('--test', default=False, help='Are we running the test mode')
parser.set_defaults(func=handle_cli)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)