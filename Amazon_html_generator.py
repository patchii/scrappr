from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup
mots_cles=["huawei","mate","20"]
my_url="https://www.amazon.com/s?url=search-alias%3Daps&field-keywords="
for mot in mots_cles:
    my_url=my_url+mot+"+"
my_url = my_url[:-1]
my_url= my_url + "&sort=review-rank"
#open connex and grab  
#uClient = uReq(my_url)
#page_html= uClient.read()
#uClient.close()
req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close() 
page_soup=soup(page_html,"html.parser")
print(my_url)



