import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.jossandmain.com/lighting/pdp/barnwell-20-table-lamp-bchh7573.html'

#opening connection, grabbing the page
uClient = uReq(my_url)

# le contenu de la page dans une variable page_html
page_html = uClient.read()
uClient.close()

#parser la variable page_html avec beautifulsoup et indiquer comment parser html.parser
#placer le resulatat de parsing dans page_soup
page_soup = soup(page_html, "lxml.parser")

#monter le header de page soup

containers = page_soup.findAll("div", {"class" : "ProductCardList-item"})

len(containers)


