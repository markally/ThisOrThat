from pymongo import MongoClient
import itertools
db = MongoClient().ThisOrThatSearch
collection = db.wordcounts

"""set keywords to analyze"""
keywords = ["nike", "reebok", "adidas"]

combinations = itertools.combinations(keywords, 2)

def calcRMS(cat1, cat2):
	"""
	Calculate Root-Mean-Square for unbinned unparameterized data between cat 1 and 2
	why RMS: http://cims.nyu.edu/~tygert/abbreviated.pdf
	cat1 and cat2 are dictionaries of word-count pairs
	"""
	wordset = set(cat1.keys() + cat2.keys())
	setsize = len(wordset)
	sumsquare = 0
	for word in wordset:
		diffsquared = (cat1.get(word, 0) - cat2.get(word, 0)) ** 2
		sumsquare += diffsquared
	RMS = (sumsquare / setsize) ** 0.5
	return RMS

def main():
	"""calcs, prints and stores RMS for each combination of 2 keywords"""
	for combo in combinations:
		words1 = collection.find_one({"keyword": combo[0]})["wordcounts"]
		words2 = collection.find_one({"keyword": combo[1]})["wordcounts"]
		RMS = calcRMS(words1, words2)
		db.RMS.insert({"keywords": list(combo), "RMS": RMS})
		print combo, "has an RMS of", RMS

if __name__ == "__main__":
	main()