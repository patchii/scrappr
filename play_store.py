import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://apps.shopify.com/kit/reviews'
uClient = uReq(my_url)
page=""

# le contenu de la page dans une variable page_html
page_html = uClient.read()
uClient.close()

#parser la variable page_html avec beautifulsoup et indiquer comment parser html.parser
#placer le resulatat de parsing dans page_soup
page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("div", {"class" : "review-content"}
for container in containers:
	review=container.text.strip()
	page =page+review
print(page)




