from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup
import unidecode
from time import sleep


my_url="https://www.amazon.fr/iPhone-Silicone-Case-Midnight-Blue/dp/B075KY3W4P/ref=sr_1_10/257-1047781-2776734?ie=UTF8&qid=1550676863&sr=8-10&keywords=iphone+x"
my_url=unidecode.unidecode(my_url)
req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close() 
page_soup=soup(page_html,"lxml")

#file1="index.html"
#f1=open(file1,"w")
#f1.write(unidecode.unidecode(str(page_soup)))
#f1.close()



containers=page_soup.find_all("a",{"data-hook":"see-all-reviews-link-foot"})


sleep(0.4)
filename="review.csv"
f= open(filename,"w")
headers="title\trating\treview\n"
f.write(headers)


if len(containers) != 0 :
    review_url="https://www.amazon.fr"+containers[0]["href"]
    number_of_reviews_container= containers[0].text
    number_of_reviews=[int(s) for s in number_of_reviews_container.split() if s.isdigit()]
    if (len(number_of_reviews)==0):
        number_of_reviews=1
    else:
        number_of_reviews=number_of_reviews[0]
        
    print(number_of_reviews)
    number_of_review_pages=(number_of_reviews//10)+1

    for i in range(1,number_of_review_pages+1):
        print("page Number "+str(i) +"\n")
        r=review_url+"&pageNumber="+str(i)
        r=unidecode.unidecode(r)
        r_uClient = uReq(r)
        r_page_html= r_uClient.read()
        r_uClient.close()
        r_page_soup=soup(r_page_html,"lxml")
        containers = r_page_soup.findAll("div",{"class": "a-section celwidget"})
    
    
        for container in containers:    
        
            title_container=container.findAll("a",{"class":"a-size-base a-link-normal review-title a-color-base a-text-bold"})
            review_title=title_container[0].text
            
            rating_container=container.findAll("a",{"class":"a-link-normal"})
            rating=rating_container[0]["title"]
            
            review_container=container.findAll("span",{"class":"a-size-base review-text"})
            review=review_container[0].text
            s= unidecode.unidecode(review_title + "\t" + rating + "\t" + review + "\n")
            
            try:
                f.write(s)
            except:
              print("Something went wrong")
            finally:
              sleep(0.4)

f.close()