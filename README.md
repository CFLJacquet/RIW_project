# Recherche d'information

Programme d'indexation de fichiers textes et de recherche d'information dans ces fichiers.

Modèles de recherche utilisés:
* modèle de recherche booléen
* modèle de recherche vectoriel (tf-idf)


## Prérequis

* python 3.5+
* librairie nltk
* matplotlib
* numpy

## Comment utiliser les fonctions de recherche sur CACM

Ouvrez le module ```R_research.py``` et décommentez les lignes souhaitées pour tester les modèles
Le premier modèle est booléen, le deuxième est un TF-IDF standard

```
if __name__ == "__main__":
    # --- to test the boolean search function
    q = "(document or master) and not (data or access)"
    boolean_research(q)

    # --- to test the vectorial search fct
    t = " code optimization for space efficiency"
    vectorial_search(t)
```
