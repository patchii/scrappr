from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup
from time import sleep

mots_cles=["iphone+x"]
my_url="https://www.amazon.fr/s?url=search-alias%3Daps&field-keywords="
for mot in mots_cles:
    my_url=my_url+mot+"+"
my_url = my_url[:-1]
my_url= my_url + "&sort=relevanceblender"
print(my_url)
filename="review.csv"

f= open(filename,"w")
headers="title\trating\treview\n"
f.write(headers)

req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close() 
page_soup=soup(page_html,"html.parser")
containers=page_soup.find_all("div",{"class":"a-fixed-left-grid-col a-col-right"})
j=1
page=""
string=""
for container in containers:

    print("link number "+ str(j)+"\n")
    j=j+1
    url_container=container.findAll("a",{"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
    url=url_container[0]["href"]
    
    if "picassoRedirect.html" not in url: 
        print(url)
        print('\n')
        my_url=url    
        req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
        uClient = uReq(req)
        page_html = uClient.read()
        uClient.close() 
        page_soup=soup(page_html,"html.parser")
        containers=page_soup.find_all("a",{"data-hook":"see-all-reviews-link-foot"})
        if len(containers) != 0 :
            review_url="https://www.amazon.fr"+containers[0]["href"]
            number_of_reviews_container= containers[0].text
            number_of_reviews=[int(s) for s in number_of_reviews_container.split() if s.isdigit()][0]
            number_of_review_pages=(number_of_reviews//10)+1

        #f.close()
            for i in range(1,5):
                print("page Number "+str(i) +"\n")
                r=review_url+"&pageNumber="+str(i)
                try:
                    r_uClient = uReq(r)
                    r_page_html= r_uClient.read()
                    r_uClient.close()
                    r_page_soup=soup(r_page_html,"html.parser")
                    containers = r_page_soup.findAll("div",{"class": "a-section celwidget"})
                
                
                    for container in containers:    
                    
                        title_container=container.findAll("a",{"class":"a-size-base a-link-normal review-title a-color-base a-text-bold"})
                        review_title=title_container[0].text
                        
                        rating_container=container.findAll("a",{"class":"a-link-normal"})
                        rating=rating_container[0]["title"]
                        
                        review_container=container.findAll("span",{"class":"a-size-base review-text"})
                        if len(review_container)!=0:
                            review=review_container[0].text
                        
                            try:
                                string=review_title + "\t" + rating + "\t" + review + "\n"
                                
                                if string not in page:
                                    page=page+string
                            except:
                                print("something went wrong\n")
                except:
                    print("encode error")
print(page)
f.write(page)
f.close()