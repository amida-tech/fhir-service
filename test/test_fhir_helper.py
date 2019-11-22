'''
Created on Nov 18, 2019

@author: gregory
'''

import os
from shutil import copyfile
from unittest import mock
import fhir_helper
from mocks import url_mocks

def test_ingest_output_data():
    """
    test the ingest_output_data function for correct production of data structures
    """
    output_file = 'test/fixture/output.tsv'
    stemmer = 'Porter'
    tokenizer_str = 'whitespace'
    stopword_str = 'aggressive'
    fhir_helper.ingest_output_data(output_file, stemmer, tokenizer_str, stopword_str)

    condition = 'Abdominal pain, etiology unknown'.lower()
    #unknown is on the stoplist
    expected_tokens = ['abdomin', 'pain', 'etiolog']

    # output_dict, output_token_dict are all populated
    assert len(fhir_helper.output_dict) == 17
    assert condition in fhir_helper.output_dict
    assert fhir_helper.output_dict[condition] == [
        '7399-7319', 'GI Stomach & duodenum', 'Stomach', 'Digestive (Digestive Conditions, Misc.)']
    assert fhir_helper.output_token_dict[condition] == expected_tokens

def test_ingest_fhir_data():
    """
    test the ingest_fhir_data function for correct production of data structures
    """
    fhir_data_dir = 'test/fixture/fhir_stu3'

    fhir_helper.ingest_fhir_data(fhir_data_dir)

    condition = 'Viral sinusitis (disorder)'

    #test_data_dict are populated
    assert 11 == len(fhir_helper.test_data_dict)
    assert 4 == fhir_helper.test_data_dict[condition]

def test_lookup_from_synonym_file():
    """
    test the lookup_from_synonym_file function and it's returned value
    """
    query = 'Diabetes'
    html_lookup_file = 'test/fixture/html_lookup_file.txt'
    expected_results = {'Diabetes insipidus, partial', 'DM', 'Partial diabetes insipidus',
                        'Diabetes mellitus', 'Neurohypophyseal diabetes insipidus',
                        'Diabetes insipidus, central'}

    result_set = fhir_helper.lookup_from_synonym_file(query, html_lookup_file)

    assert 6 == len(result_set)
    assert expected_results == result_set

def test_find_condition_information_tokenized():
    """
    test the results of the find_condition_information function with the tokenized method

    ingest_fhir_data and ingest_output_data are prerequisites for this to work correctly
    """

    #run prereqs
    fhir_data_dir = 'test/fixture/fhir_stu3'
    fhir_helper.ingest_fhir_data(fhir_data_dir)
    output_file = 'test/fixture/output.tsv'
    stemmer = 'Porter'
    tokenizer = 'whitespace'
    stopword = 'aggressive'
    fhir_helper.ingest_output_data(output_file, stemmer, tokenizer, stopword)

    # now test this functionality
    conditions = ['abscess']
    query_method = 'tokenized'
    similarity_metric = 'cosine'
    stemmer = 'Porter'
    tokenizer = 'whitespace'
    threshold = 0.0

    expected_results = [('abscess, brain', 0.707), ('abscess, kidney', 0.707),
                        ('abscess, liver', 0.707), ('abscess, lung, chronic', 0.707),
                        ('abscess, periurethral', 0.707)]

    results = fhir_helper.find_condition_information(conditions, query_method, similarity_metric,
                                                     stemmer, tokenizer, threshold)

    assert 5 == len(results)
    assert expected_results == results

def test_find_condition_information_tfidf():
    """
    test the results of the find_condition_information function with the tfidf method
    """

    conditions = ['abscess']
    query_method = 'tfidf'
    similarity_metric = 'cosine'
    stemmer = 'Porter'
    tokenizer = 'whitespace'
    threshold = 0.0

    expected_results = [('abscess, brain', 0.5487356969084024),
                        ('abscess, kidney', 0.5487356969084024),
                        ('abscess, liver', 0.5487356969084024),
                        ('abscess, periurethral', 0.5487356969084024),
                        ('abscess, lung, chronic', 0.42099864092607153)]

    results = fhir_helper.find_condition_information(conditions, query_method, similarity_metric,
                                                     stemmer, tokenizer, threshold)
    assert 5 == len(results)
    assert expected_results == results

def test_find_condition_information_subset():
    """
    test the results of find_condition_information function with the subset method
    """

    conditions = ['abscess']
    query_method = 'subset'
    similarity_metric = 'cosine'
    stemmer = 'Porter'
    tokenizer = 'whitespace'
    threshold = 0.0

    expected_results = {'abscess, lung, chronic', 'abscess, liver', 'abscess, kidney',
                        'abscess, periurethral', 'abscess, brain'}

    results = fhir_helper.find_condition_information(conditions, query_method, similarity_metric,
                                                     stemmer, tokenizer, threshold)

    assert 5 == len(results)
    assert expected_results == set(results)

def test_find_condition_information_none():
    """
    test the results of find_condition_information function with None as the method
    """

    conditions = ['abscess']
    query_method = None
    similarity_metric = 'cosine'
    stemmer = 'Porter'
    tokenizer = 'whitespace'
    threshold = 0.0

    results = fhir_helper.find_condition_information(conditions, query_method, similarity_metric,
                                                     stemmer, tokenizer, threshold)

    assert [] == results

@mock.patch('fhir_helper.urlopen', url_mocks.offline_medline_plus)
def test_lookup_medlineplus():

    base_url = 'https://medlineplus.gov/'
    user_query = 'Cancer'

    #original location
    html_lookup_file = 'test/fixture/html_lookup_file.txt'
    #create a copy to maintain integrity of file
    test_filename_working = 'test/fixture/html_lookup_file_copy.txt'
    copyfile(html_lookup_file, test_filename_working)

    result = fhir_helper.lookup_medlineplus(base_url, user_query, test_filename_working)
    with open(test_filename_working, 'r', encoding='utf-8') as fs:
        lines = [line.strip().split('\t')[1].strip() for line in fs.readlines()]

    # delete our working copy before performing asserts
    os.remove(test_filename_working)

    expected_results = {'Carcinoma', 'Malignancy', 'Neoplasms', 'Tumor'}

    assert 4 == len(result)
    assert expected_results == result
    # now check the file
    assert set(expected_results) <= set(lines)

@mock.patch('fhir_helper.urlopen', url_mocks.offline_icd10data)
def test_lookup_icd10data():

    base_url = 'https://www.icd10data.com/'
    user_query = 'Cancer'

    #original location
    html_lookup_file = 'test/fixture/html_lookup_file.txt'
    #create a copy to maintain integrity of file
    test_filename_working = 'test/fixture/html_lookup_file_copy.txt'
    copyfile(html_lookup_file, test_filename_working)

    result = fhir_helper.lookup_icd10data(base_url, user_query, test_filename_working)
    with open(test_filename_working, 'r', encoding='utf-8') as fs:
        lines = [line.strip().split('\t')[1].strip() for line in fs.readlines()]

    # delete our working copy before performing asserts
    os.remove(test_filename_working)

    expected_results = {'Agranulocytosis due to cancer chemotherapy',
                        'Chemotherapy-induced neutropenia',
                        'Neutropenia due to chemotherapy'}

    assert 3 == len(result)
    assert expected_results == result
    # now check the file
    assert set(expected_results) <= set(lines)

def test_get_console_input_true():
    with mock.patch('builtins.input', return_value='dew'):
        assert fhir_helper.get_console_input(True) == 'dew'

def test_get_console_input_false():
    with mock.patch('builtins.input', return_value='dew'):
        assert fhir_helper.get_console_input(False) == 'dew'
