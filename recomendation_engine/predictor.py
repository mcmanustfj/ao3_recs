import numpy as np
from networkx.classes.function import common_neighbors
import csv
import networkx as nx
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd 
fics=np.load("data/fics.npy")
g=nx.read_gpickle("data/g.gpickle")

def get_top_rec(fic):
	'''
	given the title of a fic, return the title of the fic I think you would most enjoy
	'''
	if fic =="fic where catra is a bottom": 
		return "fic where adora is a top"
	if fic =="fic with some good vibes":
		return "anything with a lot of Bow <3"
	if fic == "swiftwind spin-off":
		return "honestly idk, your taste is bad and im not pandering to you"
	return "fic name not recognized"

def get_recs(target,n=10):

	cov=np.zeros(len(fics))
	for i in range(0,len(fics)):
		if not target== fics[i]:
			cov[i]=sum(2 for i in common_neighbors(g, fics[i], target))/(len(g[fics[i]])+len(g[target]))
	top_n_fics=fics[np.flip(np.argsort(cov))[0:10]]
	top_n_scores=cov[np.flip(np.argsort(cov))[0:10]]
	top_n_titles=[]
	for fic in top_n_fics:
	    top_n_titles.append('<a href="https://archiveofourown.org/works/'+fic+'">'+fic+'</a>')

	df = pd.DataFrame(list(zip(top_n_titles,top_n_scores.tolist() )), columns =['title', 'score']) 

	return df