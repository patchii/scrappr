from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
my_url = 'https://www.amazon.co.uk/Apple-iPhone-64-GB-Silver/product-reviews/B076GV5GXF/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
#opent connex an grab  
uClient = uReq(my_url)
page_html= uClient.read()
uClient.close()
page_soup=soup(page_html,"html.parser")
containers = page_soup.findAll("div",{"class": "a-section celwidget"})

#preparer les stop_words
stop_words = set(stopwords.words("english"))
for container in containers:    
    
    
    review_container=container.findAll("span",{"class":"a-size-base review-text"})
    review=review_container[0].text
    words = word_tokenize(review)
    filtered_review = []
    for w in words:
        if w not in stop_words:
            filtered_review.append(w)
    print(filtered_review) 
    