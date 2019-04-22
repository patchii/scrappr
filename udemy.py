import sys
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import bs4
import urllib.request
import bs4 as bs


class Client(QWebPage):

	def __init__(self, url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self.on_page_load)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()

	def on_page_load(self):
		self.app.quit()



url = 'https://steamcommunity.com/app/770240/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=english'
client_reponse = Client(url)
source = client_reponse.mainFrame().toHtml()
soup = bs.BeautifulSoup(source, 'lxml')
containers = soup.findAll("div", {"class" : "apphub_Card modalContentLink interactable"}) 
print(len(containers))



