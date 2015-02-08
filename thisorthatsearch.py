"""fetches tweets matching a set of keywords using Twitter Search API, cleans the text and and stores it in MongoDB."""

import twitter, sched, time, string
from twitterkeys import *
from pymongo import MongoClient

"""initialize Mongo Client and Database"""
client = MongoClient()
db = client.ThisOrThatSearch

"""initialize twitter API"""
api = twitter.Api(consumer_key=consumer_key,
consumer_secret=consumer_secret,
access_token_key=access_token,
access_token_secret=access_secret)

since_id = "563432865505882112" #Randomly taken from webserver

"""initialize scheduler"""
s = sched.scheduler(time.time, time.sleep)

"""get 3 keywords"""
#mainword = raw_input("Enter the keyword you're checking: ")
#thisword = raw_input("Enter the first keyword comparison: ")
#thatword = raw_input("Enter the second keyword comparison: ")

#keywords = [mainword, thisword, thatword]

keywords = ["nike", "reebok", "adidas"]

def cleantweet(tweet):
	"""strips unicode and punctuation from tweet text"""
	asciitweet = tweet.encode(encoding="ascii", errors="ignore")
	cleanedtweet = ""
	for letter in asciitweet:
		if letter not in string.punctuation:
			cleanedtweet += letter
	return cleanedtweet
	
def main():
	"""searches twitter for each keyword and stores the cleaned tweet in MongoDB. Keeps since_id to avoid duplicate tweets."""
	global since_id
	for keyword in keywords:
		tweetsearch = api.GetSearch(term=keyword, lang="en", count=100, since_id=since_id)
		for tweet in tweetsearch:
		    if since_id < tweet.id_str:
		        since_id = tweet.id_str
		    db.cleantext.insert({"keyword": keyword, "text": cleantweet(tweet.text)})

def scheduler():
	"""Schedules searches to fit Twitter API rate delays. 180 searches per 15 minutes, and main() executes 1 search per keyword"""
	delaypercycle = 1/(180.0/15/60)*len(keywords)+1
	while True:
	    s.enter(delaypercycle, 1, main,())
	    s.run()

if __name__ == "__main__":
	scheduler()