import difflib
import json
from fuzzywuzzy import fuzz
import contractions
import nltk

import os

os.environ['NLTK_DATA'] = 'nltk_data'

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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

    # the API should not be case sensitive
    given_answer = given_answer.lower()
    correct_answer = correct_answer.lower()

    # Expand contractions. Example: can't => cannot
    given_answer = contractions.fix(given_answer)
    correct_answer = contractions.fix(correct_answer)

    # API should ignore punctuations
    given_answer = given_answer.translate(str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))
    correct_answer = correct_answer.translate(str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))

    # Split by space
    first = given_answer.split()      # Split by space
    second = correct_answer.split()   # Split by space

    ## 1. extra words
    extra = [entry for entry in first if entry not in second]

    ## 2. missed words using difflib
    missed = [entry for entry in second if entry not in first]

    ## 3. Misspelled words
    STOPWORDS = set(stopwords.words('english'))
    first = [word for word in first if not word in STOPWORDS]   # remove stopwords
    second = [word for word in second if not word in STOPWORDS] # remove stopwords
    misspelled = [(f,s) for f in first for s in second if find_misspelled(f,s, 0.4)]
    misspelled = [(val, key) for (val, key) in misspelled if key != val] # remove same key and values tuples.

    ## 4. Similarity score with stopwords.
    similarity_with_stopwords = float(fuzz.ratio(given_answer, correct_answer))
    similarity_without_stopwords = float(fuzz.ratio(" ".join(first), " ".join(second)))
    similarity = min(similarity_with_stopwords, similarity_without_stopwords)

    ## 5. The output JSON
    output = {
        "extra" : extra,
        "missed" : missed,
        "misspelled" : misspelled,
        "similarity" : similarity
    }

    return json.dumps(output)

