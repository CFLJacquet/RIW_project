import re
import pickle
import json
from math import log10
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from M_document import Document

tokenizer = RegexpTokenizer(r'\w+')

def create_collection(name_of_source):
    """ Pre-treatment of document. Creates a doc collection and a text collection """
    with open(name_of_source, 'r') as fp:
        collection = {}
        write = ""
        ID = 0
        collection[ID] = Document(ID)
        txt = {}
        
        for line in fp:
            if write == "" or line[:2] in (".I", ".W", ".K", ".T"):
                if re.match(r"^.I", line):
                    txt[ID] = collection[ID].concat()
                    ID = int(line[3:-1])
                    collection[ID] = Document(ID)
                elif re.match(r"^.T", line):
                    write = 'title'
                elif re.match(r"^.W", line):
                    write = 'summary'
                elif re.match(r"^.K", line): 
                    write = 'keywords'
            elif write != "" and line[0] != ".":
                if write == 'title':   
                    collection[ID].title = collection[ID].title + line[:-1] + " "
                elif write == 'summary':
                    collection[ID].summary = collection[ID].summary + line[:-1] + " "
                else :
                    collection[ID].keywords = collection[ID].keywords + line[:-1] + " "
            else:
                write = ""

    del txt[0]
    del collection[0]

    with open('CACM_collection_docs', 'wb') as fichier:
        p = pickle.Pickler(fichier)
        p.dump(collection)
    
    with open('CACM_collection_txt.json', 'w') as outfile :
        json.dump(txt, outfile)


def tokenizer_tf(text, docID):
    """ Map - treatment of tokens (to significant unique words for each doc). 
    Returns a list of filtered terms: (term, (docID, term_freq)) """

    stop = open("data/common_words", 'r').read()
    keywords =[]
    fdist = FreqDist()
    lemmatizer = WordNetLemmatizer()

    # Tokenizes the doc, and the lemma of meaningful words are added.
    tokens = tokenizer.tokenize(text)
    for elt in tokens:
        w = elt.lower()
        if w not in stop and not re.match(r"[0-9]+", w):
            keywords.append(lemmatizer.lemmatize(w))

    fdist = FreqDist(keywords)
    result = [(x[0],(docID, 1+log10(x[1]))) for x in fdist.items()]
    
    return result

def aggregate_idf(full_word_list):
    """ Creates the reverse index: list of (term, collection_freq, [posting_list: (docID, tf-idf)]) """
    
    term = [(x[0], 1, [x[1]]) for x in full_word_list]
    
    # Adds word to reverse index if it is different from the last entry in the index, 
    # otherwise, it appends the (docID, tf) and increases the df
    d =[term[0]]
    for i in range (1, len(term)):
        if term[i][0] != term[i-1][0]:
            d.append(term[i])
        else:
            print()
            d[len(d)-1] = (d[len(d)-1][0], d[len(d)-1][1] + 1, d[len(d)-1][2] + term[i][2])

    # Calculates the df for each doc and replaces tf by tf*idf for each docID
    result = []
    for elt in d:
        term = [elt[0], elt[1], []]
        for posting in elt[2]:
            r = posting[0], posting[1] * log10( len(d) / elt[1] )
            term[2].append(r)
        result.append(term)

    return result


def create_index(source):
    """ Creates the reverse index file (json) """
    
    words = []
    with open(source, 'r') as f:
        collection = json.load(f)
    
    for key, value in collection.items():
        tokens = tokenizer_tf(value, int(key))
        words += tokens
    
    s_list = sorted(words)
    
    reverse_index = aggregate_idf(s_list)

    with open('CACM_index_inverse.json', 'w') as outfile :
        json.dump(reverse_index, outfile)
    print("the index contains {} words".format(len(reverse_index)))



def doc_vector_length():
    """ Create json file with doc vector lengths = sum( (tf-idf)² ) """

    with open('CACM_index_inverse.json', 'r') as f:
        index = json.load(f)

    with open('CACM_collection_txt.json', 'r') as f:
        txts = json.load(f)
    
    doc_index = {}
    for elt in txts.keys() :
        doc_index[elt] = 0

    for word in index:
        postings = word[2]
        for doc in postings:
            doc_index[str(doc[0])] += doc[1] ** 2            

# Super heavy --> vecteurs creux
        # for docID in doc_index.keys():
        #     print("doc #{}".format(docID))
        #     try: 
        #         if int(docID) == postings[0][0] :
        #             doc_index[docID].append(postings[0][1])
        #             del postings[0]
        #         else:
        #             doc_index[docID].append(0)
        #     except IndexError:
        #         doc_index[docID].append(0)

    
    with open('CACM_doc_index.json', 'w') as outfile :
        json.dump(doc_index, outfile)
        

if __name__ == "__main__":
    # --- Create documents collection file (both as doc object and txt for further processing)
    # create_collection("data/cacm.all")
    
    # --- Create reverse index
    # create_index('CACM_collection_txt.json')
    
    # --- Create doc vector length : sum(tf-idf)²
    doc_vector_length()