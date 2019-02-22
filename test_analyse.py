from IPython import display
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')

from urllib.request import urlopen as uReq
import pandas as pd
from bs4 import BeautifulSoup as soup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
my_url = 'https://www.amazon.co.uk/Apple-iPhone-64-GB-Silver/product-reviews/B076GV5GXF/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
#opent connex an grab  
uClient = uReq(my_url)
page_html= uClient.read()
uClient.close()
page_soup=soup(page_html,"html.parser")
containers = page_soup.findAll("div",{"class": "a-section celwidget"})
sid = SentimentIntensityAnalyzer()
results = []


for container in containers:    
    
    
    review_container=container.findAll("span",{"class":"a-size-base review-text"})
    review=review_container[0].text

    

    ss = sid.polarity_scores(review)

    results.append(ss)

#pprint(results)
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
plt.show()