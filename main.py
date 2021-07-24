import difflib
import json
from fuzzywuzzy import fuzz

def find_misspelled(first, second, ratio):
    '''Find misspelled words which cross SequenceMatcher threshold '''
    return difflib.SequenceMatcher(None, first, second).ratio() > ratio

def sentence_compare(request):
    request_json = request.get_json()
    if request_json and ('given_answer' in request_json) and ('correct_answer' in request_json):
        given_answer = request_json["given_answer"]
        correct_answer = request_json["correct_answer"]
    else:
        return f'Please send proper JSON with given_answer and correct_answer'

    first = given_answer.split()      # Split by space
    second = correct_answer.split()   # Split by space

    ## 1. extra words
    extra = [entry for entry in first if entry not in second]

    ## 2. missed words using difflib
    missed = [entry for entry in second if entry not in first]

    ## 3. Misspelled words
    misspelled = [(f,s) for f in first for s in second if find_misspelled(f,s, 0.4)]
    misspelled = [(val, key) for (val, key) in misspelled if key != val] # remove same key and values tuples.

    ## 4. Similarity score
    similarity = float(fuzz.ratio(given_answer, correct_answer))

    ## 5. The output JSON
    output = {
        "extra" : extra,
        "missed" : missed,
        "misspelled" : misspelled,
        "similarity" : similarity
    }

    return json.dumps(output)

