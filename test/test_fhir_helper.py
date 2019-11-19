'''
Created on Nov 18, 2019

@author: gregory
'''

import fhir_helper

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

    conditions = ['Stroke']
    query_method = None
    similarity_metric = 'cosine'
    stemmer = 'Porter'
    tokenizer = 'whitespace'
    threshold = 0.0

    results = fhir_helper.find_condition_information(conditions, query_method, similarity_metric,
                                                     stemmer, tokenizer, threshold)

    assert [] == results
