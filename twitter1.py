 
import tweepy
import unidecode
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns

def twitter_parse(keywords):
	tab=[]
	page=''
	string=''
	mots_cle=keywords.split()

	consumerKey="ocyEvIv7PZa1s6uMSCankk8mQ"
	consumerSecret="pFXAqAOVMBooETWVPFCJWp7a3tUFd64uFJ3hnS94HsmAb2TDVc"
	accessToken="431572166-17MkK35mgL0sveWF81s87qpqXkT9q51jBegyBuB5"
	accessTokenSecret="AihEMJNboEBFwu9fRNbjH0JoF3hhzmyBaMC5fTOe6IbiF"

	auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessToken, accessTokenSecret)
	api = tweepy.API(auth)
	noOfSearchTerms = 100
	tweets = tweepy.Cursor(api.search, q=mots_cle).items(noOfSearchTerms)
	for tweet in tweets:
	   # tweet_review = tweet.text
		#translated_tweet = Translator().translate(text=tweet_review, dest='en').text
		review=tweet.text
	    string= unidecode.unidecode(review)
	    if string not in page:
		    page=page+string+"\n"
		    tab.append(string)
	                             
	return tab






