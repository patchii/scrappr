from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://www.amazon.fr/Apple-iPhone-64-GO-Sid%C3%A9ral/product-reviews/B075LXNK24/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
#opent connex an grab  
uClient = uReq(my_url)
page_html= uClient.read()
uClient.close()
page_soup=soup(page_html,"html.parser")
containers = page_soup.findAll("div",{"class": "a-section celwidget"})

filename="review.csv"
f= open(filename,"w")
headers="title\trating\treview\n"
f.write(headers)

for container in containers:    
    
    title_container=container.findAll("a",{"class":"a-size-base a-link-normal review-title a-color-base a-text-bold"})
    review_title=title_container[0].text
    
    rating_container=container.findAll("a",{"class":"a-link-normal"})
    rating=rating_container[0]["title"]
    
    review_container=container.findAll("span",{"class":"a-size-base review-text"})
    review=review_container[0].text
    
    
    
    f.write(review_title.replace(",","|") + "\t" + rating + "\t" + review.replace(",","|") + "\n")

f.close()