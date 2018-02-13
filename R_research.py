import pickle
from pprint import pprint
import json
import matplotlib.pyplot as plt

from M_boolean_treebuilder import Lexer, Parser, Interpreter
from M_vectorial import vect_search

with open('clean_data/CACM_collection_docs', 'rb') as f :
    u = pickle.Unpickler(f)
    DOCUMENTS = u.load()

def boolean_research(query, rappel = 10):
    """ boolean search function. Returns the first 10 documents (default value) that matches the request terms.
    Prints a list of documents and returns the doc numbers.
    :param query: str, boolean reaquest made of words, AND, OR and parenthesis
    :return: list of doc numbers
    """

    tokens = Lexer(query)
    tree = Parser(tokens).parse()
    docIDs = Interpreter(tree).interpret()

    print("{} documents found.\n\nList of the first {} docs corresponding to the query:\n".format(len(docIDs), rappel))
    for i in range(rappel-1):
        doc = DOCUMENTS[docIDs[i]]
        print(doc)

    return docIDs[:rappel]

def vectorial_search(query, rappel = 10):
    """ vectorial search function. Returns the first 10 documents (default value) that are the closest to the request.
    Prints list of documents (doc number # title) and returns a list of doc numbers.
    :param query: str, full text query
    :return: list of doc numbers
    """

    doc_list = vect_search(query)[:rappel]
    for elt in doc_list :
        print(DOCUMENTS[int(elt)])
    
    return doc_list

if __name__ == "__main__":
    # --- to test the boolean search function
    # q = "(document or master) and not (data or access)"
    # boolean_research(q)

    # --- to test the vectorial search fct
    t = " code optimization for space efficiency"
    vectorial_search(t)

