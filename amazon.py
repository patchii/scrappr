from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup
from py_translator import Translator


import unidecode

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

my_url=unidecode.unidecode(my_url)
req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close() 
page_soup=soup(page_html,"lxml")
containers=page_soup.find_all("div",{"class":"s-item-container"})
print(len(containers))
j=1
page=""
string=""
for container in containers:


    url_container=container.findAll("a",{"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
    if (len(url_container)!=0):
        url=url_container[0]["href"]
        url =unidecode.unidecode(url)
        
        if "picassoRedirect.html" not in url: 
            print("link number "+ str(j)+"\n")
            j=j+1   
            print(url)
            print('\n')
            req1 = Request(url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
            uClient1 = uReq(req1)
            page_html = uClient1.read()
            uClient1.close() 
            page_soup=soup(page_html,"lxml")
            containers=page_soup.find_all("a",{"data-hook":"see-all-reviews-link-foot"})
            if len(containers) != 0 :
                review_url="https://www.amazon.fr"+containers[0]["href"]
                number_of_reviews_container= containers[0].text
                number_of_reviews=[int(s) for s in number_of_reviews_container.split() if s.isdigit()]
                if (len(number_of_reviews)==0):
                    number_of_reviews=1
                else:
                    number_of_reviews=number_of_reviews[0]
                number_of_review_pages=(number_of_reviews//10)+1

            #f.close()
                for i in range(1,min(6,number_of_review_pages+1)):
                    print("page Number "+str(i) +"\n")
                    r=review_url+"&pageNumber="+str(i)
                    r =unidecode.unidecode(r)

                    try:
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
                            if len(review_container)!=0:
                                review=review_container[0].text                     
                                try:

                                    string= unidecode.unidecode(review_title + "\t" + rating + "\t" + review + "\n")
                                    translated_string = Translator().translate(text=string, dest='en').text
                                    string= unidecode.unidecode(translated_string)
                                    if string not in page:
                                        page=page+translated_string
                                except:
                                    print("something went wrong\n")
                    except:
                        print("encode error")
print(page)
f.write(page)
f.close()