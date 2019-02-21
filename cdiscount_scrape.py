import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.cdiscount.com/electromenager/refrigerateur-congelateur/continental-edison-cefc262db-refrigerateur-combi/f-11003090635-cefc262db.html#cm_rr=FP:7583423:SP:CAR'

#opening connection, grabbing the page
uClient = uReq(my_url)

# le contenu de la page dans une variable page_html
page_html = uClient.read()
uClient.close()

#parser la variable page_html avec beautifulsoup et indiquer comment parser html.parser
#placer le resulatat de parsing dans page_soup
page_soup = soup(page_html, "html.parser")

#monter le header de page soup


containers = page_soup.findAll("div", {"class" : "detRating jsDetRating"})

filename = "reviews.csv"
f = open(filename, "w")

headers = "titre, commentaire\n"

f.write("headers")

for container in containers:
	titre = container.div.div.span.text
	commentaire = container.div.p.text.strip()
	print("titre: " + titre)
	print("commentaire: " + commentaire )

	f.write(titre + "," + commentaire.replace(",","|") + "\n")

f.close()



