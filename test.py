import pickle


with open('CACM_collection_docs', 'rb') as f:
    u = pickle.Unpickler(f)
    COLLECTION = u.load()

print((COLLECTION))
