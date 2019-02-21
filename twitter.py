from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json






#consumer key, consumer secret, access token, access secret.
ckey="ocyEvIv7PZa1s6uMSCankk8mQ"
csecret="pFXAqAOVMBooETWVPFCJWp7a3tUFd64uFJ3hnS94HsmAb2TDVc"
atoken="431572166-17MkK35mgL0sveWF81s87qpqXkT9q51jBegyBuB5"
asecret="AihEMJNboEBFwu9fRNbjH0JoF3hhzmyBaMC5fTOe6IbiF"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
                


        print((tweet))
        
        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])