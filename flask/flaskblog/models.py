from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='Client', lazy=True)

    def __repr__(self):
        return f"{self.username}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    keywords = db.Column(db.Text, nullable=False)
    url=db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='origin', lazy=True)
    graphs= db.relationship('Graph', backref='gg', lazy=True)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Review('{self.title}')"



class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    neg=db.Column(db.Integer, nullable=False)
    neu=db.Column(db.Integer, nullable=False)
    pos=db.Column(db.Integer, nullable=False)
    total =db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))



class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100))
    message = db.Column(db.String(100))

    def __repr__(self):
        return f"Contact('{self.name}')"    

