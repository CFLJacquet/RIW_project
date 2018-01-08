import json
import pickle
from math import log10, sqrt
from R_indexation import tokenizer_tf
from M_boolean_treebuilder import get_postings
from pprint import pprint

with open('CACM_index_inverse.json', 'r') as f:
    INDEX_DATA = json.load(f)
    
with open('CACM_doc_index.json', 'r') as f:
    DOC_LENGTH = json.load(f)

with open('CACM_collection_docs', 'rb') as f:
    u = pickle.Unpickler(f)
    COLLECTION = u.load()
COLLECTION_IDS = range(1, len(COLLECTION))

def vect_search(query, rappel=10):

    # Calculates (1+log10(tf)) for each word in the query
    q = tokenizer_tf(query, 0)
    n_q = 0
    sim = [ [i, 0] for i in COLLECTION_IDS]

    for i in range(len(q)):
        postings = get_postings(q[i][0])[0]
        try:
            w_q = q[i][1][1] * log10( len(COLLECTION)+1 / len(postings) )
        except ZeroDivisionError:
            w_q = 0
        #print("mot: {} - in {} docs - poids: {}".format(q[i], len(postings), w_q))
    
        n_q += w_q ** 2
        for doc in postings:
            w_doc = doc[1]      # calculation (tf-idf) already done during indexation
            sim[doc[0]-1][1] += w_doc * w_q

    for j, elt in enumerate(sim):
        n_d = DOC_LENGTH[str(j+1)]
        if elt[1] != 0:
            elt[1] = elt[1] / ( sqrt( n_q * n_d ) ) 

    s = sorted(sim, key=lambda x:x[1], reverse=True)[:rappel]

    result = []
    for elt in s :
        result.append((COLLECTION[elt[0]], "weight: {}".format(round(elt[1], 2))))
    
    return result
    

if __name__ == "__main__":
    t = " code optimization for space efficiency"
    pprint(vect_search(t))