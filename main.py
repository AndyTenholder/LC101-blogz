from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Post, User

def validate_signup(password, verify, username):

    validate = True
    
    # Check password is not empty
    if password == "":
        validate = False
        flash("Need password", "error")
    
    # Check username is not empty
    if username == "":
        validate = False
        flash("Need username", "error")
    
    # Check password is valid
    if len(password)<3 or len(password)>20 or  (" " in password):
        validate = False
        flash("Enter valid password: 2>password<20 & no spaces", "error")
    
    # Check passwords match
    if not password==verify:
        validate = False
        flash("passwords do not match", "error")
    
    # Check username is not already used
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        validate = False
        flash("The username <strong>{0}</strong> is already registered".format(username), 'error')

    return validate

    
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        password = request.form['password']
        verify = request.form['verify']
        username = request.form['username']

        if validate_signup(password, verify, username):
            new_user = User(password, username)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')

    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and password == user.password:
            session['username'] = username
            flash("Logged in", 'info')
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/')

#@app.route('/user', methods=['GET'])
#def singleUser():

@app.route('/blog', methods=['GET'])
def blog():

    if request.args.get('user'):
        username = request.args.get('user')
        user = User.query.filter_by(username=username).first()
        posts = Post.query.filter_by(owner_id=user.id)

        return render_template('posts.html', 
            title = "It's a blog!", 
            posts=posts)

    if request.args.get('post_id'):
        post_id = request.args.get('post_id')
        post = Post.query.filter_by(id=post_id)

        return render_template('posts.html', 
            title = "It's a blog!", 
            posts=post)

    posts = Post.query.all()
    
    return render_template('posts.html',
        title="It's a Blog!", 
        posts=posts)

@app.route('/newpost', methods=['GET','POST'])
def newpost():

    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        contents = request.form['contents']
        post = Post(title, contents, user)
        db.session.add(post)
        db.session.commit()
        return render_template('post.html', 
            title = "It's a blog!", 
            post_title = post.title, 
            content = post.content)

    return render_template('add.html', 
        title = "Add a Blog Entry!") 

@app.route('/', methods=['GET','POST'])
def index():

    users = User.query.all()

    return render_template('index.html',
        title="It's a Blog!", 
        users=users)

if __name__ == '__main__':
    app.run()