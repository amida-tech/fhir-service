'''
Created on Nov 18, 2019

@author: gregory
'''

import fhir_helper

def test_ingest_output_data():
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
    assert  fhir_helper.output_dict[condition]  == [
        '7399-7319', 'GI Stomach & duodenum', 'Stomach', 'Digestive (Digestive Conditions, Misc.)']
    assert fhir_helper.output_token_dict[condition] == expected_tokens