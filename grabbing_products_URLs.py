from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup

mots_cles=["iphone","x"]
my_url="https://www.amazon.co.uk/s?url=search-alias%3Daps&field-keywords="
for mot in mots_cles:
    my_url=my_url+mot+"+"
my_url = my_url[:-1]
my_url= my_url + "&sort=relevanceblender"
print(my_url)


req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close() 
page_soup=soup(page_html,"html.parser")
containers=page_soup.find_all("div",{"class":"a-fixed-left-grid-col a-col-right"})
for container in containers:
    url_container=container.findAll("a",{"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
    url=url_container[0]["href"]
    
    if "picassoRedirect.html" not in url: 
        print(url)
        print('\n')



