import textblob 
import tweepy
import sys
import pandas as pd
import matplotlib.pyplot as plt
from py_translator import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')


#def percentage (part, whole):
	#return 100 * float(part)/float(whole)

consumerKey="ocyEvIv7PZa1s6uMSCankk8mQ"
consumerSecret="pFXAqAOVMBooETWVPFCJWp7a3tUFd64uFJ3hnS94HsmAb2TDVc"
accessToken="431572166-17MkK35mgL0sveWF81s87qpqXkT9q51jBegyBuB5"
accessTokenSecret="AihEMJNboEBFwu9fRNbjH0JoF3hhzmyBaMC5fTOe6IbiF"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

searchTerm = input("Enter keyword/hashtag to search about: ")
noOfSearchTerms = int(input("Enter how many tweets to analyse: "))



tweets = tweepy.Cursor(api.search, q=searchTerm).items(noOfSearchTerms)
sid = SentimentIntensityAnalyzer()
results=[]

for tweet in tweets:
   # tweet_review = tweet.text
	#translated_tweet = Translator().translate(text=tweet_review, dest='en').text
	ss = sid.polarity_scores(tweet.text)
	results.append(ss)





df = pd.DataFrame.from_records(results)
df['label'] = 0
df.loc[df['compound'] > 0.2, 'label'] = 1
df.loc[df['compound'] < -0.2, 'label'] = -1
df.head()



fig, ax = plt.subplots(figsize=(8, 4))

counts = df.label.value_counts(normalize=True) * 100

sns.barplot(x=counts.index, y=counts, ax=ax)

ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")
plt.title("How people are reacting on " + searchTerm + " by analysing " + str(noOfSearchTerms) + " Tweets ")
plt.show()