import json

import networkx as nx
import numpy as np
import pandas as pd
from networkx.classes.function import common_neighbors

fics = np.load("data/fics.npy")
g = nx.read_gpickle("data/g.gpickle")
with open('data/fic_dict.json') as fin:
    fic_dict = json.load(fin)


def get_recs(target, n=10):
    cov = np.zeros(len(fics))
    for i in range(0, len(fics)):
        if not target == fics[i]:
            cov[i] = sum(2 for i in common_neighbors(g, fics[i], target)) / (len(g[fics[i]]) + len(g[target]))
    top_n_fics = fics[np.flip(np.argsort(cov))[0:n]]
    top_n_scores = cov[np.flip(np.argsort(cov))[0:n]]
    top_n_titles = []
    for fic in top_n_fics:
        top_n_titles.append('<a href="https://archiveofourown.org/works/' + fic + '">' + fic_dict[fic] + '</a>')

    df = pd.DataFrame(list(zip(top_n_titles, top_n_scores.tolist())), columns=['title', 'score'])
    df.index += 1
    try:
        fic_name = fic_dict[target]
    except KeyError:
        fic_name = "No recommendations for that fic, it is probably too recent.  Sorry!"
    return fic_name, df
