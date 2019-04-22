from textblob import TextBlob

g = open("resultat.txt","w")
f = open("review.txt", "r")
for x in f:
	if (x!="\n"):
		x.replace('(','')
		x.replace(')','')
		x.replace(',','')
		x.replace('.','')
		analysis = TextBlob(x)
		if (analysis.sentiment.polarity < 0.00):
			x= "(\'"+ x +"\'"+ ",\'neg\')"
		if (analysis.sentiment.polarity >= 0.00):
			x= "(\'"+ x +"\'"+ ",\'pos\')"
		g.write(x + "\n")
g.close()
f.close()

