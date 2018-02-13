"""
Mesures de performance:
- Temps de calcul indexation =

- Temps de réponse à une requête booléenne = 
- Temps de réponse à une requête vectorielle = 

- Taille index inversé = 
- Taille index documents = 

"""
import matplotlib.pyplot as plt
import json
from math import log
import numpy as np

from M_vectorial import vect_search

def vectorial_evaluation(pas = 1):

    with open('clean_data/CACM_questions.json', 'r') as f:
        q = json.load(f)
    with open('clean_data/CACM_answers.json', 'r') as f:
        a = json.load(f)

    for num, question in q.items():
        
        # Code to evaluate relevance performance
        v = vect_search(question)
        nv_rappel = 0
        results = []
        precision = []
        rappel = []
        pr_curve = []
        rel = 0
        while rel != len(a[num]):
           
            results = v[:nv_rappel]
            if not results :
                rappel.append(0)
                precision.append(1)
            else:
                rel = len([i for i in a[num] if i in results])
                # rappel : nb of relevant docs retrieved /  nb of relevant docs
                try:
                    r_score = rel / len(a[num])
                except ZeroDivisionError: 
                    print("WARNING : no good answer for this question")
                    r_score = 0
                # precision : nb of relevant docs retrieved /  nb of docs retrieved
                p_score = rel / len(results)

                if r_score not in rappel:
                    rappel.append(r_score)
                    precision.append(p_score)
                    pr_curve.append([r_score, p_score])
            nv_rappel += pas
        # to get best precision for a level of recall or greater
        i=0
        j=0
        curve_pr = list(precision)
        while i < len(curve_pr)-1:
            if curve_pr[i+1] >= curve_pr[i]:
                while j < len(curve_pr[:i+1]) :
                    if curve_pr[i+1] >= curve_pr[j]:
                        curve_pr[j] = curve_pr[i+1]
                    j += 1
                j=0
            i += 1
        
        plt.plot(rappel, precision,  "o", label='meilleure précision pour chaque rappel',  color = "b")
        plt.step(rappel, curve_pr,  "-", label='PR curve',  color = "red")
        plt.title("Question {}".format(num))
        plt.ylabel("précision")
        plt.xlabel("rappel")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    vectorial_evaluation()
