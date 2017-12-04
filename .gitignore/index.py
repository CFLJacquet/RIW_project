import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')

def get_docs(name):
    with open(name, 'r') as fp:
        IDdoc = 0
        doc = {}
        write = 0
    
        for line in fp:
            if write == 1 :
                if line[0] == '.':
                    write = 0
                else : 
                    doc[IDdoc]=doc[IDdoc]+line[:-1]+" "
            if write == 0:
                if re.match(".I", line) :
                    IDdoc +=1
                    doc[IDdoc]=""
                if re.match('.T', line) or re.match('.W', line) or re.match('.K', line):
                    write = 1
    return doc

def tok_filter_collection(collection):
    dictionary= []
    
    stop = open("data/common_words", 'r').read()

    for i in range (1, len(collection)+1): 
        tokens = tokenizer.tokenize(collection[i])
        for elt in tokens:
            if elt.lower() not in stop :
                dictionary.append((elt.lower(), i))
   
    no_duplicates = list(set(dictionary))
    
    return no_duplicates

def sort_ag(tokens):

    s_list = sorted(tokens)

    for i in range(0, len(s_list)): 
        s_list[i]=(s_list[i][0],[s_list[i][1]])
    
    with open("CACM_sorted.txt", "w") as f:
        f.write(str(s_list))
    
    dictionary =[s_list[0]]
    for i in range (1, len(s_list)):
        if s_list[i][0] != s_list[i-1][0]:
            dictionary.append(s_list[i])
        else:
            dictionary[len(dictionary)-1] = (dictionary[len(dictionary)-1][0], dictionary[len(dictionary)-1][1]+s_list[i][1])
    
    with open("dictionnaire.txt", "w") as f:
        f.write(str(dictionary))

    return dictionary

if __name__ == "__main__":
    collection = get_docs("data/cacm.all")
    tokens = tok_filter_collection(collection)
    
    dictionary = sort_ag(tokens)
    print(len(dictionary))
