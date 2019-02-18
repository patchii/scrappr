import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from py_translator import Translator

my_url = 'https://www.cdiscount.com/electromenager/refrigerateur-congelateur/continental-edison-cefc262ds-refrigerateur-combi/f-11003090635-cefc262ds.html#rating'

#opening connection, grabbing the page
uClient = uReq(my_url)

# le contenu de la page dans une variable page_html
page_html = uClient.read()
uClient.close()

#parser la variable page_html avec beautifulsoup et indiquer comment parser html.parser
#placer le resulatat de parsing dans page_soup
page_soup = soup(page_html, "html.parser")

#monter le header de page soup


containers = page_soup.findAll("div", {"class" : "infoCli"})



for container in containers:
	commentaire = container.p.text.strip()
	translated_commentaire = Translator().translate(text=commentaire, dest='en').text
	print(commentaire)
	print(translated_commentaire + '\n')
	




