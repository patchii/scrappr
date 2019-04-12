import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt

from flaskblog.forms import RegistrationForm, LoginForm,ContactForm, UpdateAccountForm, PostForm, LoginAdminForm
from flaskblog.models import User, Post, Review,Graph,Contact, Admin

from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.ebay import ebay_parse
from flaskblog.twitter1 import twitter_parse
from textblob import TextBlob
import pygal
from pygal.style import DarkColorizedStyle
from flaskblog.analyse import analyse
from flaskblog.graph import generate_graph
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask_admin import BaseView, expose

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, keywords=form.keywords.data,url=form.url.data, author=current_user)
        db.session.add(post)
        if form.url.data == 'Ebay.com':
            reviews= ebay_parse(form.keywords.data,form.number_of_reviews.data)
            analyse(reviews,post)
            


        if form.url.data == 'Twitter.com':
            reviews= twitter_parse(form.keywords.data,form.number_of_reviews.data)
            analyse(reviews,post)

        flash('Your Request has been created!', 'success')
        return redirect(url_for('user_posts', username=post.author.username))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/reviews")
def reviews(post_id):
    page=request.args.get('page',1,type=int)
    post = Post.query.get_or_404(post_id)
    reviews=Review.query.filter_by(origin=post).paginate(page=page,per_page=5)
    return render_template('reviews.html', title=post.title, post=post,reviews=reviews)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.keywords = form.keywords.data
        post.url=form.url.data
        db.session.commit()
        flash('Your Request has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.keywords.data = post.keywords
        form.url.data=post.url
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Request has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



@app.route("/post/<int:post_id>/graph")
def graph(post_id):
    graph_data = generate_graph(post_id)

    return render_template( 'graph.html', graph_data = graph_data)



@app.route("/login_admin", methods=['GET', 'POST'])
def login_admin():
    form = LoginAdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.cin.data).first()
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check id and password', 'danger')
    return render_template('login_admin.html', form=form)

class UserView(ModelView):
    can_edit = False
    can_view_details = True
    column_exclude_list = ['password','image_file' ]
    column_searchable_list = ['username','email']




class PostView(ModelView):
    can_edit = False
    can_create = False
    can_view_details = True
    column_exclude_list = ['date_posted','keywords','url']
    column_searchable_list = ['title']
    column_filters = ['Client']
     


class logoutView(BaseView):
    @expose('/')
    def logout1(self):
        logout_user()
        return self.render('home.html')


admin = Admin(app, name='Administration', template_mode='bootstrap3')
admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(logoutView(name='Log Out'))




@app.route("/contact", methods=['GET', 'POST'])
def contact():
    
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, email=form.email.data,subject=form.subject.data, message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been successfully sent!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html',form=form)

@app.route('/admin')
def index():
    return '<a href="/admin/"</a>'