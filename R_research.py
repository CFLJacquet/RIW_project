import pickle
from pprint import pprint
import json

from M_boolean_treebuilder import Lexer, Parser, Interpreter
from M_vectorial import vect_search

with open('CACM_collection_docs', 'rb') as f :
    u = pickle.Unpickler(f)
    DOCUMENTS = u.load()

def boolean_research(query, rappel = 10):

    tokens = Lexer(query)
    tree = Parser(tokens).parse()
    docIDs = Interpreter(tree).interpret()

    results = []
    for elt in docIDs:
        doc = DOCUMENTS[elt]
        results.append(doc)

    return "{} documents found.\n\nList of the first {} docs corresponding to the query: {}".format(len(results), rappel, results[:rappel])


def vectorial_search(rappel = 10):

    with open('CACM_questions.json', 'r') as f:
        q = json.load(f)
    with open('CACM_answers.json', 'r') as f:
        a = json.load(f)

    for num, question in q.items():
        
        results = vect_search(question, rappel)

        print(question)
        print(a[num])
        print(results[0])
        print("matching results: {}\n".format([i for i in a[num] if i in results[0]]))

        print(results[1])
        input()
        


if __name__ == "__main__":
    # --- to test the boolean search function
    # q = "(document or master) and not (data or access)"
    # r = boolean_research(q)
    # print(r)

    # --- to test the vectorial search fct
    vectorial_search(20)


