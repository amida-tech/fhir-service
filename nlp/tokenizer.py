'''
Created on Oct 11, 2019

@author: gregory
'''

from nltk.tokenize import word_tokenize

from nlp import stemming_lemmatization

def whitespace_tokenize(document, stemmer):
    """
    using a whitespace tokenizer, tokenize a document and possibly apply a stemmer

    @param: document: a string of text
    @param: stemmer: the name of a stemmer (or possibly None for no stemmer)
    @type: document: str
    @type: stemmer: str
    @return: a list of tokens from the document
    @rtype: list of str
    """
    if not document:
        return []
    tokens = document.split(' ')
    if stemmer not in ['Porter', 'Snowball']:
        return tokens
    stemmed_tokens = []
    for token in tokens:
        if 'Porter' == stemmer:
            stemmed_tokens.append(stemming_lemmatization.apply_nltk_porter_stemmer(token))
        elif 'Snowball' == stemmer:
            stemmed_tokens.append(stemming_lemmatization.apply_nltk_snowball_stemmer(token))
    return stemmed_tokens

def nltk_tokenize(document):
    """
    using the nlp tokenizer, tokenize a document

    @param: document: a string of text
    @type: document: str
    @return: a list of tokens from the document
    @rtype: list of str
    """
    return [] if not document else word_tokenize(document)
