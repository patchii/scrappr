from textblob import TextBlob
from flaskblog.models import User, Post, Review,Graph
from flaskblog import db




def analyse(reviews,post):

    sommtot=0
    sommneg=0
    sommpos=0
    sommneu=0
    review_nb=0
    for item in reviews:
    	sommtot=sommtot+1
    	analysis = TextBlob(item)
    	if (analysis.sentiment.polarity < 0.00):
    		sommneg=sommneg+1
    	if (analysis.sentiment.polarity == 0):
    		sommneu=sommneu+1
    	if (analysis.sentiment.polarity > 0.00):
    		sommpos=sommpos+1
    	review_nb = review_nb+1
    	review= Review(title='review '+str(review_nb),content=item,origin=post)
    	db.session.add(review)
	    
	    
	    
	    	
	    
        	  
        
        	                
        
        
        

    graph=Graph(neg=sommneg,neu=sommneu,pos=sommpos,total=sommtot,gg=post)
    db.session.add(graph)
    db.session.commit()



 
