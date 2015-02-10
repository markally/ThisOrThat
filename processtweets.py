from pymongo import MongoClient

# Initialize Mongo DB connection.
db = MongoClient().ThisOrThatSearch

# Set keywords to analyze.
keywords = ["nike", "reebok", "adidas"]

def processtweets(keyword):
	"""
	Query MongoDB for all tweets tied to keyword.
	Return a dictionary of {word: count} pairs.
	"""
	wordcounts = {}
	for tweet in db.cleantext.find(
		spec={"keyword": keyword}, 
		fields={"_id": False, "text": True}
		):
		tweetwords = tweet["text"].split()
		for word in tweetwords:
			wordcounts[word] = wordcounts.get(word, 0) + 1
	return wordcounts

def main():
	for keyword in keywords:
		db.wordcounts.insert(
			{"keyword": keyword, "wordcounts": processtweets(keyword)})

if __name__ == "__main__":
	main()