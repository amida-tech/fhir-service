# fhir-service
Python service to return VASDR information for general (or official) medical conditions

# Modes of Operation
1. REST API - Run FHIR_Helper_Flask.py.  Use your favorite method (such as Postman) to make POST requests on the specified URL and POST.
    1. The endpoint "suggest".  A medical phrases is given and a list of candidates is returned with their similarity scores in descending order.  4 parameters may be supplied
        1. query (required) - The user query to lookup
        2. limit (optional, defalut no limit) - Limit the number of candidates to be the top n
        3. threshold (optional, default 0.0) - Only return candidates with a similarity score which exceeds threshold
        4. similairty (optional, default 'harmonic') - The similarity metric to use.  The choices are 'harmonic', 'cosine', 'jaccard'.
        5. stemmer (optional, default 'Porter') - The stemmer or lemmatizer to use.  The choices are 'Porter' and 'Snowball'.
    2. The endpoint "fetch".  Given a candidate (as fetched from "suggest" or chosen from the output.tsv spreadsheet), find all the relevant information for that candidate.  1 parameter may be given
        1. candidate - The candidate to get the full information from
		
2. Report Test Query - Run FHIR_Helper.py with --test True argument.  This will iterate through the currently 137 test queries and report back which queries have at least 1 match in regards to exceeding the threshold (which is 0 by default, or does the query match anything at all).  It is configured by the config/config_test.txt file.

3. Main Loop - Run FHIR_Helper.py *without* --test True argument.  The user can enter a query and then after candidates are returned enter in one of the candidates to see the full information for it.  It is configured by the config/config.txt file.

# Under the Hood
There are 3 separate query lookup methods which are provided and one must be chosen within the code to see its operation.  The 3 are as follows:

1. Subset matching.  How many of the words present in a query are also present in a potential candidate.

2. Tokenized.  Tokenize the query and compare it against a tokenized version of the candidates.  In each case, apply the Porter stemmer to each of the tokens.  Compare much as in subset matching

3. TF-IDF.  Fit and transform the output.tsv spreadsheet as the training set and pickle the vectorizer to disk.  For each query, transform using the vectorizer from training set.  Use cosine similarity to pick out the best results.

# NLP Variations
There are other NLP tools available.  These are either configurable to override a default choice or not available to configuration and hence need to be changed directly in code.

1. Stemming/Lemmatization - The Porter and Snowball stemmers are both available for usage.  The current and default choice is the Porter stemmer.

# Synonmys and the Need for Synonyms
Our training and test sets are hopelessly lacking in information.  There are different names for many of the medical conditions we wish to consider and sometimes the common parlance is completely different from the official medical term.  Therefore, we need to gain access to these mapping as much as possible to enhance our query methods.  There are 3 ways we do this currently.

1. https://medlineplus.gov/
2. https://www.icd10data.com/
3. Manual entry

In all three cases, the data winds up in medfind.txt.  It is safe to add information without worrying about destroying information.
