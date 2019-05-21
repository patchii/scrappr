import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from py_translator import Translator
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/home1")
def home():
	return render_template('index.html')


if __name__=='__main__':
	app.run(debug=True)
		



