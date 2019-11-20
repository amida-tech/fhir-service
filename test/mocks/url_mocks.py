'''
Created on Nov 19, 2019

@author: gregory
'''

from unittest import mock

def _mock_response(self, status=200, content="CONTENT", json_data=None, raise_for_status=None):
    """
        since we typically test a bunch of different
        requests calls for a service, we are going to do
        a lot of mock responses, so its usually a good idea
        to have a helper function that builds these things
    """
    mock_resp = mock.Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
    if json_data:
        mock_resp.json = mock.Mock(return_value=json_data)

    mock_resp.read = lambda: content
    
    return mock_resp

def offline_medline_plus(url):
    print('Mocking opening the url ' + url)
    if 'https://medlineplus.gov/cancer.html' == url:
        with open('test/fixture/medline_plus/cancer_content.txt', 'r', encoding='utf-8') as fs:
            lines = fs.readlines()
        content =  '\n'.join(lines)
    else:
        content = ''
    response = _mock_response('', status = 200, content = content)
    return response

def offline_icd10data(url):
    print('Mocking opening the url ' + url)
    if 'https://www.icd10data.com/search?s=Cancer' == url:
        with open('test/fixture/icd10data/cancer_initial_results.txt', 'r', encoding='utf-8') as fs:
            lines = fs.readlines()
        content =  '\n'.join(lines)
    elif 'https://www.icd10data.com/ICD10CM/Codes/D50-D89/D70-D77/D70-/D70.1' == url:
        with open('test/fixture/icd10data/cancer_content.txt', 'r', encoding='utf-8') as fs:
            lines = fs.readlines()
        content =  '\n'.join(lines)
    else:
        content = ''
    response = _mock_response('', status = 200, content = content)
    return response