import itertools
import numpy as np

from pymongo import MongoClient

db = MongoClient().ThisOrThatSearch
collection = db.wordcounts

# Set keywords to analyze.
keywords = ["nike", "reebok", "adidas"]

def CosSim(cat1, cat2):
	"""
	Calculate cosine similarity between two vectors denoting word counts.

	Cat1 and cat2 are dictionaries of word-count pairs.
	Word-count pairs are unbinned and unparameterized.
	"""
	wordset = set(cat1.keys() + cat2.keys())
	countmatrix = [[cat1.get(x, 0), cat2.get(x, 0)] for x in wordset]
	a = np.array(countmatrix)
	v1 = a[:, 1]
	v2 = a[:, 2]
	CosSim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
	return CosSim

def RMS(cat1, cat2):
	"""
	Calculate Root-Mean-Square between cat1 and cat2.

	Cat1 and cat2 are dictionaries of word-count pairs.
	Word-count pairs are unbinned and unparameterized.
	Why RMS: http://cims.nyu.edu/~tygert/abbreviated.pdf
	"""
	wordset = set(cat1.keys() + cat2.keys())
	setsize = len(wordset)
	sumsquare = 0
	for word in wordset:
		diffsquared = (cat1.get(word, 0) - cat2.get(word, 0)) ** 2
		sumsquare += diffsquared
	RMS = (sumsquare / setsize) ** 0.5
	return RMS

def ColSim(cat1, cat2):
	"""
	Calculate column similarity between cat1 and cat2.

	cat1 and cat2 are dicitonaries of word-count pairs.
	"""
	union = union(cat1.keys(), cat2.keys())
	intersect = intersection(cat1.keys(), cat2.keys())
	ColSim = intersect / union
	return ColSim

def calculate(keywords, metric):
	"""
	calculate, print and store metric for each combination of 2 keywords.
	Takes list of keywords and a metric name.
	keywords must contain > 2 keywords
	metric name must be a string
	Possible metrics: CosSim, RMS, ColSim.
	"""
	combinations = itertools.combinations(keywords, 2)
	for combo in combinations:
		words1 = collection.find_one({"keyword": combo[0]})["wordcounts"]
		words2 = collection.find_one({"keyword": combo[1]})["wordcounts"]
		result = eval(metric + "(words1, words2)")
		db[metric].insert({"keywords": list(combo), metric: result})
		print combo, metric, result