import sched
import time
import string

import twitter
from pymongo import MongoClient

from twitterkeys import *

# Initialize Mongo Database.
client = MongoClient()
db = client.ThisOrThatSearch

# Initialize Twitter API with credentials.
api = twitter.Api(
	consumer_key=consumer_key,
	consumer_secret=consumer_secret,
	access_token_key=access_key,
	access_token_secret=access_secret
	)

since_id = "563432865505882112" # Randomly taken from Twitter website

# Initialize scheduler.
s = sched.scheduler(time.time, time.sleep)

# Get keywords.
keywords = ["nike", "reebok", "adidas"]

def cleantweet(tweet):
	"""Strip unicode and punctuation from tweet text."""
	asciitweet = tweet.encode(encoding="ascii", errors="ignore")
	cleanedtweet = ""
	for letter in asciitweet:
		if letter not in string.punctuation:
			cleanedtweet += letter
	return cleanedtweet
	
def tweetsearch(keyword):
	"""
	Search Twitter for a keyword and store the cleaned tweet in MongoDB.
	Recycle tweet id_str as since_id to avoid duplicate tweets.
	"""
	global since_id
	search = api.GetSearch(
	    term=keyword, lang="en", count=100, since_id=since_id)
	for tweet in search:
	    if since_id < tweet.id_str:
	        since_id = tweet.id_str
	    db.cleantext.insert(
	        {"keyword": keyword, "text": cleantweet(tweet.text)})

def scheduler(keywords):
	"""
	Calls tweetsearch for each keyword.
	Schedules searches to fit Twitter API rate delays. 
	180 searches per 15 minutes.
	"""
	keylist = iter(keywords)
	delaypercycle = 1/(180.0/15/60)
	while True:
		try:
			s.enter(delaypercycle, 1, tweetsearch,(keylist.next()))
	        s.run()
	    except StopIteration:
	    	keylist = iter(keywords)

if __name__ == "__main__":
	scheduler(keywords)