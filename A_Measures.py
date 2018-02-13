
import matplotlib.pyplot as plt
import json
from math import log
import numpy as np
from pprint import pprint
import pandas

from M_vectorial import vect_search


def F_measure(precision, rappel, b=1) :
    try :
        return ( (b ** 2 + 1) * precision * rappel / (b**2 * precision + rappel) )
    except ZeroDivisionError:
        return 0

def measures(rang_max = 10, pas = 1):

    with open('clean_data/CACM_questions.json', 'r') as f:
        q = json.load(f)
    with open('clean_data/CACM_answers.json', 'r') as f:
        a = json.load(f)

    precision = []
    rappel = []
    f_m = []
    e_m = []
    r_m = []

    for num, question in q.items():
        
        # Code to evaluate relevance performance
        v = vect_search(question)
        nv_rappel = 0
        rel = 0

        p_score = []
        r_score = []
        f_score = []
        e_score = []
        no_answer = False

        while nv_rappel <= rang_max:
            results = v[:nv_rappel]
            if not results :
                r_score.append(0)
                p_score.append(1)
                f_score.append(0)
                e_score.append(1)
            else:
                rel = len([i for i in a[num] if i in results])
                # rappel : nb of relevant docs retrieved /  nb of relevant docs
                # equals to the R-Measure
                try:
                    r = rel / len(a[num])                
                except ZeroDivisionError: 
                    no_answer = True
                    r = 0
                r_score.append( r )
                # precision : nb of relevant docs retrieved /  nb of docs retrieved
                p = rel / len(results)
                p_score.append( p )

                # F-measure & E-measure
                f_temp =  F_measure(p, r) 
                f_score.append(f_temp)
                e_score.append( 1 - f_temp )

            nv_rappel += 1

        # Calculation of mean average precision
        local_average_precision = [1]
        for i in range(pas, rang_max+1, pas):
            local_average_precision.append( np.mean(p_score[:i]) )

        precision.append(local_average_precision)
        rappel.append(r_score[0::pas])
        f_m.append(f_score[0::pas])
        e_m.append(e_score[0::pas])

        if no_answer:
            no_answer =False
            print("WARNING: no good answer for question ", num)

    average_precision = np.mean( np.array(precision), 0 )
    average_rappel = np.mean( np.array(rappel), 0 )
    average_f_measure = np.mean( np.array(f_m), 0 )
    average_e_measure = np.mean( np.array(e_m), 0 )
    
    rang = range(0, rang_max+1, pas)

    print(average_precision)

    plt.plot(rang, average_precision,  "-", label='précision moyenne',  color = "b")
    plt.plot(rang, average_rappel,  "-", label='rappel moyen (ou R-mesure)',  color = "red")
    plt.plot(rang, average_f_measure,  "--", label='F1-mesure moyenne',  color = "green")
    plt.plot(rang, average_e_measure,  "+-", label='E1-mesure moyenne',  color = "purple")
    plt.ylabel("mesure")
    plt.xlabel("rang")
    plt.legend()
    plt.show()
    

if __name__ == "__main__":
    measures(rang_max = 50,pas = 5)
