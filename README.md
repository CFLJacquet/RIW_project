# Recherche d'information

Programme d'indexation de fichiers textes et de recherche d'information dans ces fichiers.

Modèles de recherche utilisés:
* modèle de recherche booléen
* modèle de recherche vectoriel (tf-idf)


## Prérequis

* python 3.5+
* librairie nltk

## Utiliser l'outil

Ouvrez le module R_research.py et décommentez les lignes pour tester les deux types de modèle

```
if __name__ == "__main__":
    # --- to test the boolean search function
    # q = "(document or master) and not (data or access)"
    # r = boolean_research(q)
    # print(r)

    # --- to test the vectorial search fct
    vectorial_search(20)
```
