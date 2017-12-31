import pickle
from M_boolean_treebuilder import Lexer, Parser, Interpreter

with open('CACM_collection_docs', 'rb') as f :
    u = pickle.Unpickler(f)
    DOCUMENTS = u.load()

def boolean_research(query):

    tokens = Lexer(query)
    tree = Parser(tokens).parse()
    docIDs = Interpreter(tree).interpret()

    results = []
    for elt in docIDs:
        doc = DOCUMENTS[elt]
        results.append(doc)

    return "{} documents found.\n\nList of docs corresponding to the query: {}".format(len(results),results)

if __name__ == "__main__":
    q = "(document or master) and not (data or access)"
    r = boolean_research(q)

    print("Query: " + q + "\n")
    print(r)



