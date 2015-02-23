import itertools
import numpy as np

from pymongo import MongoClient

db = MongoClient().ThisOrThatSearch
collection = db.wordcounts

# Set keywords to analyze.
keywords = ["nike", "reebok", "adidas"]

combinations = itertools.combinations(keywords, 2)

def calcCosSim(cat1, cat2):
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
	cosinesim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
	return cosinesim

def main():
	"""Calculate, print and store CosSim for each combination of 2 keywords"""
	for combo in combinations:
		words1 = collection.find_one({"keyword": combo[0]})["wordcounts"]
		words2 = collection.find_one({"keyword": combo[1]})["wordcounts"]
		CosSim = calcCosSim(words1, words2)
		db.RMS.insert({"keywords": list(combo), "CosSim": CosSim})
		print combo, "has a CosSim of", CosSim

if __name__ == "__main__":
	main() 