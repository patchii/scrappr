import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.rottentomatoes.com/m/pet_sematary_2019/reviews/'

uClient = uReq(my_url)
page=""

# le contenu de la page dans une variable page_html
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")



