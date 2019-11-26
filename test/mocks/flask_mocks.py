'''
Created on Nov 22, 2019

@author: gregory
'''
from flask import Flask, jsonify, request
import pytest

@pytest.fixture
def app():
    app = Flask('fhir_helper_flask')

    @app.route('/suggest', methods=['POST'])
    def index():
        user_query = request.args.get('query')
        return jsonify(user_query)

    @app.route('/fetch', methods=['POST'])
    def ping():
        user_candidate = request.args.get('candidate')
        return jsonify(user_candidate)

    return app
