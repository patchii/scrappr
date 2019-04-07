import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://steamcommunity.com/app/770240/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=english'

uClient = uReq(my_url)
page=""

# le contenu de la page dans une variable page_html
page_html = uClient.read()
uClient.close()

#parser la variable page_html avec beautifulsoup et indiquer comment parser html.parser
#placer le resulatat de parsing dans page_soup
for j in range(0,7):
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("div", {"id" : "page"+str(j)})
	for container in containers:
		review=container.text.strip()
		page =page+review
print(page)




