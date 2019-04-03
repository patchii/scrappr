
from flaskblog.models import User, Post, Review,Graph
import pygal
from pygal.style import DarkColorizedStyle



def generate_graph(post_id):
	post = Post.query.get_or_404(post_id)
	graph=Graph.query.filter_by(gg=post).first()
	sommpos=graph.pos
	sommneu=graph.neu
	sommneg=graph.neg
	sommtot=graph.total
	y=(sommneg/sommtot)*100
	x=(sommpos/sommtot)*100
	z=100-x-y
	graph = pygal.Pie(fill=True, interpolate='cubic', print_values=True, style=DarkColorizedStyle(
                  value_font_family='googlefont:Raleway',
                  value_font_size=30,
                  value_colors=('white')))
	graph.title = ' How people are reacting on by analysing '+  str(sommtot) +' reviews in( %)'
	graph.add('Positive',round(x,2))
	graph.add('Negative',round(y,2))
	graph.add('Neutral',round(z,2))
	graph_data = graph.render_data_uri()
	return graph_data
    
    
    
    
	
    
    
    
    
    
   
    
    
    
    
    

	