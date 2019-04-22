import bs4
from urllib.request import Request,urlopen as uReq
from bs4 import BeautifulSoup as soup
import unidecode

def rottens_parse(keywords="the sun"):
	mots_cles=keywords.split()
	my_url = 'https://www.rottentomatoes.com/search/?search='
	for mot in mots_cles:
		my_url=my_url+mot+"%20"
	my_url = my_url[:-3]

	i=0
	page=''
	tab=[]
	string=''
	my_url=unidecode.unidecode(my_url)
	req = Request(my_url, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2526.73 Safari/537.36'},{'Accept-Language' : 'en-US,en;q=0.8'})
	print(req)
	uClient = uReq(req)
	page_html = uClient.read()
	uClient.close()
	page_soup=soup(page_html,"html.parser")
	containers=page_soup.find_all("div",{"class":"details"})
	print(len(containers))
    
   
    
   
    
   
    
    
    
   
   
   


rottens_parse(keywords="the sun")


        
    
    


#uClient = uReq(my_url)


#page_html = uClient.read()
#uClient.close()


#page_soup = soup(page_html, "html.parser")



#containers = page_soup.findAll("div", {"class" : "the_review"})
#print(len(containers))




