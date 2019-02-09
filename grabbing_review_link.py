from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup
from time import sleep


my_url="https://www.amazon.co.uk/Apple-iPhone-Silver-Certified-Refurbished/dp/B0798G4Z19/ref=sr_1_9/261-1246156-8049016?ie=UTF8&qid=1549673314&sr=8-9&keywords=iphone+x"

req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close() 
page_soup=soup(page_html,"html.parser")
containers=page_soup.find_all("a",{"data-hook":"see-all-reviews-link-foot"})

if len(containers) != 0 :
    review_url="https://www.amazon.co.uk"+containers[0]["href"]
    number_of_reviews_container= containers[0].text
    number_of_reviews=[int(s) for s in number_of_reviews_container.split() if s.isdigit()][0]
    print(number_of_reviews)
    number_of_review_pages=(number_of_reviews//10)+1
    filename="review.csv"
    f= open(filename,"a+")
    headers="title\trating\treview\n"
    f.write(headers)
#f.close()
    for i in range(1,number_of_review_pages+1):
        print("page Number "+str(i) +"\n")
        r=review_url+"&pageNumber="+str(i)
        r_uClient = uReq(r)
        r_page_html= r_uClient.read()
        r_uClient.close()
        r_page_soup=soup(r_page_html,"html.parser")
        containers = page_soup.findAll("div",{"class": "a-section celwidget"})
    
    
        for container in containers:    
        
            title_container=container.findAll("a",{"class":"a-size-base a-link-normal review-title a-color-base a-text-bold"})
            review_title=title_container[0].text
            
            rating_container=container.findAll("a",{"class":"a-link-normal"})
            rating=rating_container[0]["title"]
            
            review_container=container.findAll("span",{"class":"a-size-base review-text"})
            review=review_container[0].text
            
            
            
            f.write(review_title.replace(",","|") + "\t" + rating + "\t" + review.replace(",","|") + "\n")
            sleep(0.2)
f.close()