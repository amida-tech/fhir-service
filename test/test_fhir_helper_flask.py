'''
Created on Nov 18, 2019

@author: gregory
'''
from argparse import Namespace

from test.mocks.flask_mocks import app

import fhir_helper_flask

def test_handle_cli():
    """
    test the handle_cli function.
    the test is that the operation completes.
    """
    cli_args = Namespace(cfile='test/fixture/config/config.txt')
    fhir_helper_flask.handle_cli(cli_args)

def test_lookup_candidates(client):
    """
    test lookup candidates
    """
    query = 'Tinnitus'
    response = client.post("/suggest",
                           query_string={'query': query})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json == query

def test_fetch_information(client):
    """
    test fetch information
    """
    candidate = 'thrombosis, brain'
    response = client.post("/fetch",
                           query_string={'candidate': candidate})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json == candidate
