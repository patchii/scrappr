import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
def shopy_parse(keywords,nb):
    mots_cles=keywords
    my_url = 'https://apps.shopify.com/'
    my_url = my_url + re.sub('\s+', '-', mots_cles) + "/reviews?page="
    page=""
    for j in range(2,10):
        my_url = my_url + str(j)
        print(my_url)
        uClient = uReq(my_url)
        my_url = my_url[:-1]



# le contenu de la page dans une variable page_html
        page_html = uClient.read()
        uClient.close()

#parser la variable page_html avec beautifulsoup et indiquer comment parser html.parser
#placer le resulatat de parsing dans page_soup
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("div", {"class" : "truncate-content-copy"})
        print(len(containers))
        for container in containers:
	        review=container.text.strip()
	        page =page+review
print(page)




