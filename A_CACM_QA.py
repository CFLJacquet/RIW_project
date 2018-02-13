from pprint import pprint
import re
import json

def get_questions():

    """ Pre-treatment of document. Creates a doc collection and a text collection """
    with open('data/query.text', 'r') as fp:
        collection = {}
        write = ""
        ID = 0
        
        for line in fp:
            if write == "" or line[:2] in (".I", ".W"):
                if re.match(r"^.I", line):
                    ID = int(line[3:-1])
                    collection[ID] = ""
                elif re.match(r"^.W", line):
                    write = 'summary'
            elif write != "" and line[0] != ".":
                if write == 'summary':
                    collection[ID] = collection[ID] + line[:-1] + " "
            else:
                write = ""
    
    with open('clean_data/CACM_questions.json', 'w') as outfile :
        json.dump(collection, outfile)

def get_answers():

    a_file = open('data/qrels.text', 'r').readlines()
    answer = {} 
    
    for line in a_file:
        try: 
            line = line.split()
            qID = int(line[0])
            docID = str(int(line[1]))

            if qID in answer.keys():
                answer[qID].append(docID)
            else: 
                answer[qID] = [docID]
        except:
            qID = int(line[0])
            docID = str(int(line[1]))
            answer[qID] = [docID]
    
    for i in range(1, 64):
        if i not in answer.keys():
            answer[i] = []

    with open('clean_data/CACM_answers.json', 'w') as outfile :
        json.dump(answer, outfile)

if __name__ == "__main__":
    get_questions()
    get_answers()