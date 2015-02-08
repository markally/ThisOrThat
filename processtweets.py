import pymongo
from pymongo import MongoClient

"""initialize mongoDB connection"""
db = MongoClient().ThisOrThatSearch

"""set keywords to analyze"""
keywords = ["nike", "reebok", "adidas"]

def incrementcount(word):
    if wordcounts.get(word):
        wordcounts[word] += 1
    else:
        wordcounts[word] = 1

def processtweets(keyword):
	"queries MongoDB for all tweets tied to keyword, returns a dictionary of {word: count} pairs"
	global wordcounts
	wordcounts = {}
	for tweet in db.cleantext.find(spec={"keyword": keyword}, fields={"_id": False, "text": True}):
		tweetwords = tweet["text"].split()
		for word in tweetwords:
			incrementcount(word)
	return wordcounts

def main():
	for keyword in keywords:
		db.wordcounts.insert({"keyword": keyword, "wordcounts": processtweets(keyword)})

if __name__ == "__main__":
	main()