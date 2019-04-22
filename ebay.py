from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup

import unidecode
mots_cles=["sone","xperia","z5"]
my_url = "https://www.ebay.co.uk/sch/"
for mot in mots_cles:
    my_url=my_url+mot+"+"
my_url = my_url[:-1]
#print(my_url)

page=""
string=""
filename="review.txt"
f= open(filename,"w+")
headers=""
f.write(headers)
my_url=unidecode.unidecode(my_url)
req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close() 
page_soup=soup(page_html,"lxml")
containers=page_soup.find_all("a",{"class":"star-ratings__review-num"})
#print(len(containers))
for container in containers:
    try:
        url=container["href"]
        url =unidecode.unidecode(url)
        req1 = Request(url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
        uClient1 = uReq(req1)
        page_html = uClient1.read()
        uClient1.close() 
        page_soup=soup(page_html,"lxml")
        l_containers=page_soup.find_all("a",{"class":"see--all--reviews-link"})
    	#print(l_containers[0]["href"])
        if len(l_containers) != 0 :
            review_url=l_containers[0]["href"]
            #print(review_url)
            number_of_reviews_container= l_containers[0].text
            number_of_reviews=[int(s) for s in number_of_reviews_container.split() if s.isdigit()]
            if (len(number_of_reviews)==0):
                number_of_reviews=1
            else:
                number_of_reviews=number_of_reviews[0]
                number_of_review_pages=(number_of_reviews//10)+1
            #print(number_of_review_pages)
            for i in range(1,number_of_review_pages):
                r=review_url+"?pgn="+str(i)
                r =unidecode.unidecode(r)
                r_uClient = uReq(r)
                r_page_html= r_uClient.read()
                r_uClient.close()
                r_page_soup=soup(r_page_html,"lxml")
                
                commentaires=r_page_soup.findAll("div",{"class": " ebay-review-section"})
                for commentaire in commentaires:
                    
                    title_container=commentaire.findAll("h3",{"itemprop":"name"})
                    review_title=title_container[0].text
                    
                    rating_container=commentaire.findAll("span",{"class":"star-rating"})
                    rating=rating_container[0]["aria-label"]
                    
                    review_container=commentaire.findAll("p",{"class": "review-item-content rvw-wrap-spaces"})
                    review=review_container[0].text  
                    string= unidecode.unidecode(review + "\n")
                    if string not in page:
                        page=page+string+"\n"
    except:
        pass
f.write(page)
f.close()

