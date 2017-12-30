import re
import pickle
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from M_document import Document

tokenizer = RegexpTokenizer(r'\w+')

def get_docs(name):
    """ Pre-treatment of document """
    with open(name, 'r') as fp:
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

    with open('CACM_collection_txt', 'wb') as fichier:
        p = pickle.Pickler(fichier)
        p.dump(txt)
    with open('CACM_collection_docs', 'wb') as fichier:
        p = pickle.Pickler(fichier)
        p.dump(collection)

def tok_filter_collection(collection):
    """ Map - treatment of tokens (to significant unique words for each doc)"""

    dictionary= []
    nb_tokens = 0 
    stop = open("data/common_words", 'r').read()

    for i in range (1, len(collection)+1): 
        tokens = tokenizer.tokenize(collection[i])
        nb_tokens += len(tokens)
        for elt in tokens:
            w = elt.lower()
            if w not in stop and not re.match(r"[0-9]+", w):
                #lemmetization ou racinisation
                dictionary.append((w, i))
    print("nb tokens: " + str(nb_tokens))

    no_duplicates = list(set(dictionary))
    
    return no_duplicates

def sort_ag(tokens):
    """ Shuffle - sort & reduce """
    s_list = sorted(tokens)

    s_list = [(x[0], 1, x[1]) for x in s_list]
    
    d =[s_list[0]]
    for i in range (1, len(s_list)):
        if s_list[i][0] != s_list[i-1][0]:
            d.append(s_list[i])
        else:
            d[len(d)-1] = (d[len(d)-1][0], d[len(d)-1][1] + 1,d[len(d)-1][2]+s_list[i][2])

    with open('CACM_index_inverse', 'wb') as fichier:
        p = pickle.Pickler(fichier)
        p.dump(d)

    return d

if __name__ == "__main__":
    # --- Create documents collection file (both as doc object and txt for further processing)
    get_docs("data/cacm.all")
    
    # --- Create reverse index
    # with open('CACM_collection_txt', 'rb') as fichier:
    #     d = pickle.Unpickler(fichier)
    #     txt = d.load()
    
    # tokens = tok_filter_collection(txt)
    
    # dictionary = sort_ag(tokens)
    
    # print(len(dictionary))