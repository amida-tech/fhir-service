'''
Created on Oct 10, 2019

@author: gregory
'''

from bs4 import BeautifulSoup
import json
from nlp import Metrics, Stopword, Tokenizer
from os import listdir
from os.path import isfile, join
from urllib.request import urlopen

test_data_dict = dict()

output_dict = dict()

output_token_dict = dict()

# this is a tsv file
def ingest_output_data(output_file):
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
                                          , 'Porter'))

def ingest_fhir_data(fhir_data_dir):
    onlyfiles = [f for f in listdir(fhir_data_dir) if isfile(join(fhir_data_dir, f))]
    
    for onlyfile in onlyfiles:
        with open(join(fhir_data_dir, onlyfile)) as f:
            data = json.load(f)
        entry = data['entry']
        for ent in entry:
            resource = ent['resource']
            resourceType = resource['resourceType']
            if 'Condition' == resourceType:
                code = resource['code']
                text_field = code['text'].strip()
                if text_field not in test_data_dict:
                    test_data_dict[text_field] = 0
                test_data_dict[text_field] += 1

def lookup_from_medfind(query, html_lookup_file):
    alts = []
    lower_query = query.lower()
    
    with open(html_lookup_file, 'r', encoding='utf-8') as fs:
        lines = fs.readlines()
    for line in lines:
        parts = line.split('\t')
        comparison = parts[0].lower()
        synonym = parts[1].strip(' \n')
        if comparison == lower_query:
            alts.append(synonym)
    return alts

def cleanup_html_lookup_file(filename):
    with open(filename, 'r', encoding='utf-8') as fs:
        lines = set(fs.readlines())
    with open(filename, 'w', encoding='utf-8') as fs:
        for line in list(lines):
            fs.write(line)
            
            
def find_subset_variety(conditions):
    total_set = set()
    for condition in conditions:
        condition = condition.strip().lower()
        matches = [item for item in output_dict if condition in item]
        total_set |= set(matches)
    return list(total_set)
              
def find_tokenized_variety(conditions):
    total_set = set()
    threshold = 0.0
    for condition in conditions:
        condition = condition.strip().lower()
        tokens = Tokenizer.whitespace_tokenize(condition, 'Porter')
        for item in output_token_dict:
            item_tokens = output_token_dict[item]
            # here we compare tokens and item_tokens
            similarity = Metrics.harmonic_similarity(tokens, item_tokens)
            if similarity > threshold:
                # add the similarity so that we can rank descending
                total_set.add((item, similarity))
    
    sorted_by_similarity = sorted(total_set, key=lambda tup: tup[1], reverse=True)
    sorted_by_similarity = [x[0] for x in sorted_by_similarity]
    
    return sorted_by_similarity
              
def find_condition_information(conditions):
    # right now, test data and output_data needs to be in memory to work
    # we would like to expand this for
    #    1) partial matches
    #    2) synonyms
    #    3) case differences
    
    # this is the subset solution
    #return find_subset_variety(conditions)
    # this is a slight more sophisticated token based matching solution
    return find_tokenized_variety(conditions)

def lookup_medlineplus(user_query, html_lookups_file):
    # need the lowercase version of the query to have any shot
    URL = 'https://medlineplus.gov/' + user_query.lower().replace(' ','') + '.html'
    alts = []
    try:
        f = urlopen(URL)
        myfile = f.read()
        soup = BeautifulSoup(myfile, 'html.parser')
        alsocalled = soup.findAll("span", {"class": "alsocalled"})[0].text
        alsocalled = alsocalled[13:]
        alts = alsocalled.split(',')
        #print("HTML found " + str(alts))
        with open (html_lookups_file, 'a', encoding='utf-8') as fs:
            for alt in alts:
                fs.write(user_query + '\t'  + alt + '\n')
    except:
        #print('HTML Lookup failed')
        pass
    
    # this should contain medfind stuff just found + pre-exisiting synonyms
    alts += lookup_from_medfind(user_query, html_lookups_file)
    
    return alts
    
def get_console_input(mode):
    if mode:
        choice = input('Which condition do you wish to look up?\n\n')
    else:
        choice = input('Which of these makes sense to you?\n\n')
    return choice;
    
def display_matching_information(choice):
    print(output_dict[choice])
    return output_dict[choice]
    
def main(output_data_file, fhir_data_dir, text_list_file, html_lookup_file):
    #ingest "training" data from disc
    ingest_output_data(output_data_file)
    
    #bring in test data from disc
    ingest_fhir_data(fhir_data_dir)
    
    # send this list to disc for safe keeping
    with open(text_list_file, 'w', encoding='utf-8') as fs:
        for key in test_data_dict.keys():
            fs.write(key + '\t' + str(test_data_dict[key]) + '\n')
    
    # make sure our html lookup list contains only unique rows
    cleanup_html_lookup_file(html_lookup_file)
    
    # now let us try to do the main event.  We should choose from test_data really
    # this will be converted to service, but we can simulate with a loop
    user_query = ''
    user_candidate = ''
    while user_query != 'quit':
        user_query = get_console_input(True)

        # we will now try to augment this by "database" lookup
        # "Stroke" is a good test to assure that this works
        more_candidates = lookup_medlineplus(user_query, html_lookup_file)
        if user_query not in more_candidates:
            more_candidates.append(user_query.lower())
        
        candidates = find_condition_information(more_candidates)   
                
        print(candidates)
                
        # then we will mock the user selecting an item
        user_candidate = get_console_input(False)
        if user_candidate in candidates:
            display_matching_information(user_candidate)

def main_test(output_data_file, fhir_data_dir, text_list_file, html_lookup_file, test_results_file):
    #ingest "training" data from disc
    ingest_output_data(output_data_file)
    
    #bring in test data from disc
    ingest_fhir_data(fhir_data_dir)
    
    # send this list to disc for safe keeping
    with open(text_list_file, 'w', encoding='utf-8') as fs:
        for key in test_data_dict.keys():
            fs.write(key + '\t' + str(test_data_dict[key]) + '\n')
    
    # make sure our html lookup list contains only unique rows
    cleanup_html_lookup_file(html_lookup_file)
    
    non_empties = 0
    total = 0
    
    with open(test_results_file, 'w', encoding='utf-8') as fs:        
            
        # now let us try to do the main event.  We should choose from test_data really
        # this will be converted to service, but we can simulate with a loop
        for test_key in test_data_dict.keys():
            user_query = test_key
    
            # we will now try to augment this by "database" lookup
            # "Stroke" is a good test to assure that this works
            more_candidates = lookup_medlineplus(user_query, html_lookup_file)
            if user_query not in more_candidates:
                more_candidates.append(user_query.lower())
            
            candidates = find_condition_information(more_candidates)   
                    
            # only printing to disc now, not console
            fs.write(test_key + '\t' + str(candidates) + '\n')
            
            total += 1
            if len(candidates) > 0:
                non_empties += 1
            
    print(str(non_empties) + ' of ' + str(total))
                    
if __name__ == '__main__':
    output_data_file = 'data/output.tsv';
    fhir_data_dir = 'data/fhir_stu3'
    text_list_file = 'output/text_list.tsv'
    html_lookup_file = 'data/medfind.txt'
    test_results_file = 'output/candidate_results.txt'
    #main(output_data_file, fhir_data_dir, text_list_file, html_lookup_file)
    main_test(output_data_file, fhir_data_dir, text_list_file, html_lookup_file, test_results_file)