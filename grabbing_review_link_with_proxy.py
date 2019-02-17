import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import shuffle


def get_proxies(link):  
    response = requests.get(link)
    soup = BeautifulSoup(response.text,"lxml")
    https_proxies = filter(lambda item: "yes" in item.text,
                           soup.select("table.table tr"))
    for item in https_proxies:
        yield "{}:{}".format(item.select_one("td").text,
                             item.select_one("td:nth-of-type(2)").text)

def get_random_proxies_iter():
    proxies = list(get_proxies('https://www.sslproxies.org/'))
    shuffle(proxies)
    return iter(proxies)  # iter so we can call next on it to get the next proxy


def get_proxy(session, proxies, validated=False):
    session.proxies = {'https': 'https://{}'.format(next(proxies))}
    if validated:
        while True:
            try:
                return session.get('https://httpbin.org/ip').json()
            except Exception:
                session.proxies = {'https': 'https://{}'.format(next(proxies))}


def get_response(url):
    session = requests.Session()
    ua = UserAgent()
    proxies = get_random_proxies_iter()
    while True:
        try:
            session.headers = {'User-Agent': ua.random}
            print(get_proxy(session, proxies, validated=True))  #collect a working proxy to be used to fetch a valid response
            return session.get(url) # as soon as it fetches a valid response, it will break out of the while loop
        except StopIteration:
            raise  # No more proxies left to try
        except Exception:
            pass  # Other errors: try again


def parse_content(url):
    response = get_response(url)
    page_html=response.text
    return BeautifulSoup(page_html,"html.parser")




if __name__ == '__main__':
    url = 'https://www.amazon.co.uk/Apple-iPhone-64-SIM-Free-Smartphone-Silver/dp/B076GV5GXF/ref=sr_1_3/258-1363206-6339406?ie=UTF8&qid=1550080986&sr=8-3&keywords=iphone+x'
    page_soup=parse_content(url)
    containers=page_soup.find_all("a",{"data-hook":"see-all-reviews-link-foot"})
    filename="review.csv"
    f= open(filename,"w+")
    headers="title\trating\treview\n"
    f.write(headers)
    print(len(containers))
    
    if len(containers) != 0 :
        review_url="https://www.amazon.co.uk"+containers[0]["href"]
        number_of_reviews_container= containers[0].text
        number_of_reviews=[int(s) for s in number_of_reviews_container.split() if s.isdigit()][0]
        print(number_of_reviews)
        number_of_review_pages=(number_of_reviews//10)+1
        for i in range(1,number_of_review_pages+1):
            print("page Number "+str(i) +"\n")
            r=review_url+"&pageNumber="+str(i)
            r_page_soup=parse_content(r)
            containers = r_page_soup.findAll("div",{"class": "a-section celwidget"})
            for container in containers: 
                title_container=container.findAll("a",{"class":"a-size-base a-link-normal review-title a-color-base a-text-bold"})
                review_title=title_container[0].text
                
                rating_container=container.findAll("a",{"class":"a-link-normal"})
                rating=rating_container[0]["title"]
                
                review_container=container.findAll("span",{"class":"a-size-base review-text"})
                review=review_container[0].text     
                try:
                    f.write(review_title.replace(",","|") + "\t" + rating + "\t" + review.replace(",","|") + "\n")
                except:
                  print("Something went wrong")
                  
f.close()