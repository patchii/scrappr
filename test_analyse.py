from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
my_url = 'https://www.amazon.co.uk/Apple-iPhone-64-GB-Silver/product-reviews/B076GV5GXF/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
#opent connex an grab  
uClient = uReq(my_url)
page_html= uClient.read()
uClient.close()
page_soup=soup(page_html,"html.parser")
containers = page_soup.findAll("div",{"class": "a-section celwidget"})
sid = SentimentIntensityAnalyzer()


for container in containers:    
    
    
    review_container=container.findAll("span",{"class":"a-size-base review-text"})
    review=review_container[0].text
    #sentences=[]
    #lines_list = tokenize.sent_tokenize(review)
    #len(lines_list)
    #sentences.extend(review)
    
    print(review)
    ss = sid.polarity_scores(review)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()
    print('\n' + '\n')

    