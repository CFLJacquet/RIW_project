"""
Q1: 
il y a 192,032 tokens dans la collection

Q2: 
nombre de mots significatifs: 106,507 mots
sans doublons dans chaque doc: 76,654 mots
taille du vocabulaire (sans nombres): 8,780 mots

Q3:
collection entière - 192,032 tokens / 8,780 mots
demi collection - 55,133 tokens / 4,823 mots
=> M = kT^b
=> M = 25.534601029258393 * math.pow(T, 0.48006550908028656)

Q4 : 
Pour T = 1,000,000
M = 19,387 mots dans le vocabulaire

Q5 : voir code ci-dessous
"""
import matplotlib.pyplot as plt
import json
from math import log
import numpy as np

with open("clean_data/CACM_index_inverse.json", "r") as f:
    data = json.load(f)

freq = [x[1] for x in data]
freq.sort(reverse=True)
log_freq = [log(x) for x in freq]
log_rang = [log(x) for x in np.arange(1, len(freq)+1, 1) ]

plt.subplot(1,2,1)
plt.plot(freq, np.arange(1, len(freq)+1, 1), "red")
plt.title("freq vs rang")

plt.subplot(1,2,2)
plt.plot(log_freq,log_rang, "green")
plt.title("log(freq) vs log(rang)")
plt.show()

